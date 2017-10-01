from pijemont.types import VALUES_TYPES


class PijemontException(Exception):
    """ Base exception for the Pijemont package """
    def _name(self, name):
        if name.startswith("."):
            name = name[1:]
        if name.startswith("input."):
            name = name[6:]
        return name


class PijemontKeyError(PijemontException):
    def __init__(self, name, key):
        name = self._name(name)
        super(PijemontKeyError, self).__init__("{} is missing required key {}".format(name, key))


class PijemontTypeError(PijemontException):
    def __init__(self, name, obj, types):
        name = self._name(name)
        if isinstance(types, list):
            oneof = "one of"
            types = ", ".join(types)
        else:
            oneof = "a"
        super(PijemontException, self).__init__("{} is wrong type: expected {} {}, got {}".format(name, oneof, types, type(obj)))


class PijemontInvalidType(PijemontException):
    def __init__(self, name, typ):
        name = self._name(name)
        valid_types = ", ".join(VALUES_TYPES)
        super(PijemontException, self).__init__("{} is invalid pijemont type {}, Must be one of: {}".format(name, typ, valid_types))


class PijemontArgError(PijemontException):
    def __init__(self, name, args, valid_args):
        name = self._name(name)
        if not isinstance(args, str):
            args = ", ".join(args)
        if not isinstance(valid_args, str):
            valid_args = ", ".join(valid_args)
        super(PijemontException, self).__init__(
            "{} has extra keys: {}. Valid keys are: {}".format(name, args, valid_args))


class PijemontCastError(PijemontException):
    def __init__(self, name, typ, message):
        name = self._name(name)
        super(PijemontException, self).__init__("could not cast {} as {}: {}".format(name, typ, message))


class PijemontOneOfError(PijemontException):
    def __init__(self, name):
        name = self._name(name)
        super(PijemontException, self).__init__("more than one argument supplied for argument of type 'oneof': {}".format(name))