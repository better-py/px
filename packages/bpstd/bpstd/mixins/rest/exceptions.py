from rest_framework import exceptions
from django.utils.translation import ugettext_lazy as _

"""

自定义出错状态码

"""


class ValidationError450(exceptions.APIException):
    status_code = 450


class ValidationError451(exceptions.APIException):
    status_code = 451


class ValidationError452(exceptions.APIException):
    status_code = 452


class ValidationError453(exceptions.APIException):
    status_code = 453


class ValidationError454(exceptions.APIException):
    status_code = 454


class ValidationError455(exceptions.APIException):
    status_code = 455


class ValidationError456(exceptions.APIException):
    status_code = 456


class ValidationError457(exceptions.APIException):
    status_code = 457


class ValidationError458(exceptions.APIException):
    status_code = 458


class ValidationError459(exceptions.APIException):
    status_code = 459


class ValidationError460(exceptions.APIException):
    status_code = 460


class RateNotFound(exceptions.APIException):
    status_code = 472
    default_detail = _("The requested rate does not exist.")
