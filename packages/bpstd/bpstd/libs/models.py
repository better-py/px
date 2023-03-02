# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


# 自定义基类型:
class BaseModel(models.Model):
    """
    TIMESTAMP has a range of '1970-01-01 00:00:01' UTC to '2038-01-19 03:14:07' UTC.
    """
    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated At"), auto_now=True)

    class Meta:
        abstract = True

    @property
    def created_at_s(self):
        return int(self.created_at.timestamp())

    @property
    def updated_at_s(self):
        return int(self.updated_at.timestamp())

    @property
    def pending_duration(self):
        """记录 pending 时间差

        :return:
        """
        return abs(self.updated_at_s - self.created_at_s)

    def update_with_timestamp(self, **kwargs):
        kwargs["updated_at"] = timezone.now()
        return self.objects.update(**kwargs)


def get_zero_time():
    """数据库零值时间: 1970年

    :return:
    """
    zero = datetime.fromisoformat("1970-01-01 00:00:01")
    return zero


def get_zero_timestamp():
    """默认零值 = 1970-01-01 00:00:01

    :return:
    """
    zero = datetime.fromisoformat("1970-01-01 00:00:01")
    return zero.timestamp()


def is_zero_timestamp(ts: int):
    """默认零值 = 1970-01-01 00:00:01

    :param ts:
    :return:
    """
    return ts == get_zero_timestamp()


# 软删除:
class SoftDeleteModel(BaseModel):
    """软删除:
    更改删除时间为当前时间

    """
    deleted_at = models.DateTimeField(verbose_name=_("Deleted At"), default=get_zero_time, blank=False, null=False)

    def soft_delete(self):
        """执行软删除

        :return:
        """
        self.deleted_at = timezone.now()
        self.save()

    @property
    def is_deleted(self):
        """判断是否删除

        :return:
        """
        return self.deleted_at.timestamp() - get_zero_timestamp() > 0

    class Meta:
        abstract = True


# user 相关:
class UserBaseModel(BaseModel):
    user_id = models.UUIDField(verbose_name=_("User ID"), null=False, blank=False, db_index=True)

    class Meta:
        abstract = True

    @property
    def user_id_hex(self):
        return self.user_id.hex


# user 相关:
class UserSoftDeleteModel(SoftDeleteModel):
    user_id = models.UUIDField(verbose_name=_("User ID"), null=False, blank=False, db_index=True)

    class Meta:
        abstract = True

    @property
    def user_id_hex(self):
        return self.user_id.hex
