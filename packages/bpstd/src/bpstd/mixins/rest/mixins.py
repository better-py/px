from collections import OrderedDict

from rest_framework import exceptions, mixins, status
from rest_framework.response import Response


class DoTaskHookMixin:
    # 钩子
    serializer_class_list = None
    serializer_class_create = None
    serializer_class_update = None
    serializer_class_destroy = None

    @property
    def response_result(self):
        result = {
            "code": status.HTTP_200_OK,
            "detail": "ok",
            "data": {},
        }
        return result

    def _do_serializer(self, *args, func_type: str = "list", **kwargs):
        """覆盖 get_serializer() 方法, 实现灵活选择自定义的 serializer class

        :param args:
        :param func_type:
        :param kwargs:
        :return:
        """
        _func_types = {
            "list": self.serializer_class_list,
            "create": self.serializer_class_create,
            "update": self.serializer_class_update,
            "destroy": self.serializer_class_destroy,
            "retrieve": self.serializer_class_list,
        }
        serializer_class = (
            _func_types.get(func_type.lower()) or self.get_serializer_class()
        )
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def do_create(self, request, serializer, instance, *args, **kwargs):
        """钩子方法: 请覆盖此方法, 实现业务逻辑

        :param request:
        :param serializer:
        :param instance:
        :param args:
        :param kwargs:
        :return:
        """
        return self.response_result

    def do_list(self, request, serializer, *args, **kwargs):
        """钩子方法: GET-BATCH

        :param request:
        :param serializer:
        :param args:
        :param kwargs:
        :return:
        """
        result = self.response_result
        result.update(data=serializer.data)
        return result

    def do_retrieve(self, request, serializer, instance, *args, **kwargs):
        return self.response_result

    def do_update(self, request, serializer, instance, *args, **kwargs):
        return self.response_result

    def do_partial_update(self, request, serializer, instance, *args, **kwargs):
        return self.response_result

    def do_destroy(self, request, *args, **kwargs):
        """钩子方法: 支持软删除

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return self.response_result


class BetterCreateModelMixin(DoTaskHookMixin, mixins.CreateModelMixin):
    """rest_framework 实现有些蠢, 重构一下"""

    # TODO: 需要指定要不要执行save()操作
    # TODO: 禁用此选项, 自主控制 ojb.save() 操作.
    create_save_required = False

    def create(self, request, *args, **kwargs):
        serializer = self._do_serializer(func_type="create", data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.APIException as e:
            result = self.response_result
            result.update(
                code=e.status_code,
                detail=", ".join("{}: {}".format(k, v) for k, v in e.detail.items())
                if isinstance(e.detail, dict)
                else e.detail,
            )
            return Response(
                result, status=status.HTTP_200_OK
            )  # TODO: 考虑统一改成 400, 需要变更 validate() 部分.

        # obj:
        # instance = self.perform_create(serializer) if self.create_save_required else None
        # instance = serializer.save() if self.create_save_required else None
        instance = None
        # hook
        result = self.do_create(request, serializer, instance)
        #
        # headers = self.get_success_headers(serializer.data)
        return Response(result, status=status.HTTP_201_CREATED)


class BetterListModelMixin(DoTaskHookMixin, mixins.ListModelMixin):
    def list(self, request, *args, **kwargs):
        """自定义钩子

        :ref:
            - rest_framework.pagination.LimitOffsetPagination#paginate_queryset()

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())
        except Exception as e:
            result = self.response_result
            result.update(code=449, detail="invalid filter params: [{}]".format(e))
            return Response(result)

        page = self.paginate_queryset(queryset)
        if page:
            result = self.do_pagination(page, request, *args, **kwargs)
            return Response(result)

        serializer = self._do_serializer(queryset, many=True, func_type="list")
        #
        # hook for task:
        result = self.do_list(request, serializer, *args, **kwargs)

        return Response(result)

    def do_pagination(self, page, request, *args, **kwargs):
        serializer = self._do_serializer(page, many=True, func_type="list")
        #
        # hook for task:
        result = self.do_list(request, serializer, *args, **kwargs)

        if result.get("code") == 200:
            result.update(
                data=OrderedDict([
                    ("count", self.paginator.count),
                    ("next", self.paginator.get_next_link()),
                    ("previous", self.paginator.get_previous_link()),
                    ("results", serializer.data),
                ])
            )
        return result


class BetterRetrieveModelMixin(DoTaskHookMixin, mixins.RetrieveModelMixin):
    def retrieve(self, request, *args, **kwargs):
        """自定义钩子

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        serializer = self._do_serializer(instance, func_type="retrieve")
        # hook for task:
        result = self.do_retrieve(request, serializer, instance, *args, **kwargs)

        if result.get("data", None):
            result["data"] = serializer.data
        return Response(result)


class BetterUpdateModelMixin(DoTaskHookMixin, mixins.UpdateModelMixin):
    # TODO: 需要指定要不要执行save()操作
    update_save_required = False

    def partial_update(self, request, *args, **kwargs):
        """增量修改

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """全量修改

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self._do_serializer(
            instance, data=request.data, partial=partial, func_type="update"
        )
        #
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.APIException as e:
            result = self.response_result
            result.update(
                code=e.status_code,
                detail=", ".join("{}: {}".format(k, v) for k, v in e.detail.items()),
            )
            return Response(
                result, status=status.HTTP_200_OK
            )  # TODO: 考虑统一改成 400, 需要变更 validate() 部分.
        #
        # obj = self.perform_update(serializer) if self.update_save_required else None
        obj = serializer.save() if self.update_save_required else None
        #
        # hook:
        #
        if partial:
            result = self.do_partial_update(request, serializer, obj, *args, **kwargs)
        else:
            result = self.do_update(request, serializer, obj, *args, **kwargs)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        if result.get("data", None):
            result["data"] = serializer.data
        return Response(result)


class BetterDestroyMixin(DoTaskHookMixin, mixins.DestroyModelMixin):
    """支持软删除"""

    def destroy(self, request, *args, **kwargs):
        """支持软删除

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        #
        # hook:
        #
        result = self.do_destroy(request, *args, **kwargs)
        return Response(result, status=status.HTTP_200_OK)
