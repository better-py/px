from datetime import datetime
from time import mktime

from django.db import models


#
# Custom field types in here.
#
class UnixTimestampField(models.DateTimeField):
    """UnixTimestampField: creates a DateTimeField that is represented on the
    database as a TIMESTAMP field rather than the usual DATETIME field.
    """

    models.TimeField

    def __init__(self, null=False, blank=False, **kwargs):
        super(UnixTimestampField, self).__init__(**kwargs)
        # default for TIMESTAMP is NOT NULL unlike most fields, so we have to
        # cheat a little:
        self.blank, self.isnull = blank, null
        self.null = True  # To prevent the framework from shoving in "not null".

    def db_type(self, connection):
        typ = ["TIMESTAMP"]
        # See above!
        if self.isnull:
            typ += ["NULL"]
        if self.auto_created:
            typ += ["default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP"]
        return " ".join(typ)

    def to_python(self, value):
        return datetime.fromtimestamp(value)

    def get_prep_value(self, value):
        if value == None:
            return None
        return mktime(value.timetuple())

    def get_db_prep_value(self, value):
        if value == None:
            return None
        return value


class UserRoleField(models.CharField):
    description = "user role"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 20
        super(UserRoleField, self).__init__(*args, **kwargs)


class IDField(models.CharField):
    description = "common id field"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 50
        super(IDField, self).__init__(*args, **kwargs)


class UIDField(models.CharField):
    description = "ID of User"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 50
        super(UIDField, self).__init__(*args, **kwargs)


class LabelCodeField(models.CharField):
    description = "Label Code"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 50
        super(LabelCodeField, self).__init__(*args, **kwargs)


class BIDField(models.CharField):
    description = "ID of QuestionBundle"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 50
        super(BIDField, self).__init__(*args, **kwargs)


class CityCodeField(models.CharField):
    description = "Code of City"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 10
        super(CityCodeField, self).__init__(*args, **kwargs)


class CodeField(models.CharField):
    description = "Code"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 50
        super(CodeField, self).__init__(*args, **kwargs)


class ScopeField(models.CharField):
    description = "Scope"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 100
        super(ScopeField, self).__init__(*args, **kwargs)


class StaffNameField(models.CharField):
    description = "staff name"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 30
        super(StaffNameField, self).__init__(*args, **kwargs)
