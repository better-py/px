import validators


class ParamValidator:
    def __init__(self):
        self.validator = validators

    def uuid_validator(self, uuid_param):
        if not uuid_param:
            return False
        if self.validator.uuid(uuid_param):
            return True
        else:
            return False
