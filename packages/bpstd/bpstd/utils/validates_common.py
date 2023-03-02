# -*- coding: utf-8 -*-
import uuid

from maneki.apps.common.utils.format_timestamp import format_timestamp
from maneki.apps.error_code import ErrorsCommon
from maneki.apps.user.models import User


def validate_timestamp_start(timestamp_start):
    if timestamp_start and not str(timestamp_start).isdigit():
        return False, ErrorsCommon.time_start_error
    return True, format_timestamp(timestamp=timestamp_start)


def validate_timestamp_end(timestamp_end):
    if timestamp_end and not str(timestamp_end).isdigit():
        return False, ErrorsCommon.time_end_error
    return True, format_timestamp(timestamp_end, timedelta_day=0)


def validate_limit(limit):
    if isinstance(limit, str) and limit.isdigit():
        return True, int(limit)
    if isinstance(limit, int):
        return True, limit
    return False, ErrorsCommon.limit_error


def validate_offset(offset):
    if isinstance(offset, str) and offset.isdigit():
        return True, int(offset)
    if isinstance(offset, int):
        return True, offset
    return False, ErrorsCommon.offset_error


def validate_email(email):
    if isinstance(email, str) and '@' in email:
        user = User.objects.filter(email=email).first()
        if user:
            return True, email
        return False, ErrorsCommon.email_error
    return False, ErrorsCommon.email_error


def validate_user_id(user_id):
    if isinstance(user_id, str):
        if '-' in user_id:
            return True, uuid.UUID(user_id).hex
        else:
            return True, user_id
    if isinstance(user_id, uuid.UUID):
        return True, user_id.hex
    return True, ErrorsCommon.user_id_error
