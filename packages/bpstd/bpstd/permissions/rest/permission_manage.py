import json

from rest_framework.permissions import BasePermission

from ...utils.redis.r import redis_sessions
from maneki.apps.user.models.user_profile import UserProfile
from maneki.apps.user_role.models.perms import RolePermission, Permission
from maneki.apps.user_role.utils.cache import make_key, get_permission_cache
from maneki.apps.constants import ApiPermissionType
is_permission_cached = False


method_map = {
    'GET': ApiPermissionType.List,
    'POST': ApiPermissionType.Create
}


class StrictPermissionCheck(BasePermission):

    @staticmethod
    def get_route_path(request):
        return request.path

    @staticmethod
    def get_request_method(request):
        return request.method

    # @staticmethod
    # def is_swagger_load(path):
    #     if path == '/api/debug/':
    #         return True
    #     return False

    @staticmethod
    def is_superuser(request):
        if request.user.is_superuser:
            return True
        return False

    def has_permission(self, request, view):
        path = self.get_route_path(request)

        # if self.is_swagger_load(path):
        #     return True

        if self.is_superuser(request):
            return True

        if not self._check_permission(request, path):
            return False

        return True

    def _check_permission(self, request, path):
        raw_method = self.get_request_method(request)
        method_code = method_map.get(raw_method, -1)
        role_id = self.get_user_role_id_from_db(request.user.user_id_hex)
        return self.check_role_permission_settings_from_db(path, method_code, role_id)

    @staticmethod
    def check_role_permission_settings_from_db(path, method_code, role_id):

        permission = Permission.objects.filter(route_path=path,
                                               permission_code=method_code).first()

        if not permission:
            return False

        permission_id = permission.id

        permission_setting = RolePermission.objects.filter(permission_id=permission_id, role_id=role_id).first()

        if not permission_setting:
            return False

        return True

    @staticmethod
    def check_role_permission_settings_from_cache(path, method_code, role_id):
        key = make_key(path, method_code)
        role_list = get_permission_cache(key)
        if role_id in role_list:
            return True
        return False

    @staticmethod
    def get_user_role_id_from_db(user_id: str):
        user_profile = UserProfile.objects.filter(user_id=user_id).first()
        if not user_profile:
            return -1
        return user_profile.role_id

    @staticmethod
    def get_user_role_id_from_cache(user_id: str):
        user_info = redis_sessions['UserInfo'].get(user_id)
        if not user_info:
            return -1

        user_info = json.loads(user_info)

        role_id = user_info.get('role_id', -1)

        return role_id


