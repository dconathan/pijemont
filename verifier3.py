from utils import compare_dict_keys


class PijemontException(Exception):
    """ Base exception for the Pijemont package """
    def _name(self, name):
        name = name or "input_dict"
        if name.startswith("."):
            name = name[1:]
        return name


class PijemontKeyError(PijemontException):
    def __init__(self, name, key):
        name = self._name(name)
        super(PijemontKeyError, self).__init__("{} is missing required key {}".format(name, key))


class PijemontTypeError(PijemontException):
    def __init__(self, name, obj, typ):
        name = self._name(name)
        super(PijemontException, self).__init__("{} is wrong type: expected {}, got {}".format(name, typ, type(obj)))


class PijemontArgError(PijemontException):
    def __init__(self, name, args, valid_args):
        name = self._name(name)
        if not isinstance(args, str):
            args = ", ".join(args)
        if not isinstance(valid_args, str):
            valid_args = ", ".join(valid_args)
        super(PijemontException, self).__init__("{} has extra keys: {}. Valid keys are: {}".format(name, args, valid_args))


class PijemontHelper:
    def __init__(self, raises=False, verbose=False):
        self.errors = []
        self.verbose = verbose
        self.raises = raises

    def handle_error(self, error):
        self.errors.append(str(error))
        if self.verbose:
            print(error)
        if self.raises:
            raise error

    def _check_keys(self, name, doc, keys):
        for key in keys:
            if key not in doc:
                self.handle_error(PijemontKeyError(name, key))


DICT = {"dict", "dictionary", "map"}


class VerifyHelper(PijemontHelper):
    def _verify(self, name, input_element, reference_dict):
        if not isinstance(input_element, dict):
            self.handle_error(PijemontTypeError(name, input_element, dict))
        elif reference_dict["type"] in DICT:
            if not isinstance(reference_dict["values"], dict):
                self.handle_error(PijemontTypeError(name + ".values", reference_dict["values"], dict))
            else:
                k1, k2 = compare_dict_keys(input_element, reference_dict["values"])
                if k1:
                    self.handle_error(PijemontArgError(name, k1, reference_dict["values"].keys()))
                for key in k2:
                    if "default" in reference_dict["values"][key]:
                        pass

        return self.errors


VALID_KEYS = {"type", "descriptin", "values", "optional", "default"}


class FormatHelper(PijemontHelper):
    def _check_format(self, name, doc):

        if not isinstance(doc, dict):
            self.handle_error(PijemontTypeError(name, doc, dict))
        else:
            self._check_keys(name, doc, ["type", "values"])
            invalid_keys = set(doc.keys()) - VALID_KEYS
            if invalid_keys:
                self.handle_error(PijemontArgError(name, invalid_keys, VALID_KEYS))

        if self.errors:
            return self.errors

        if not isinstance(doc["values"], dict):
            self.handle_error(PijemontTypeError(name + ".values", doc["values"], dict))

        return self.errors


def verify(input_dict, reference_dict):
    reference_dict = {"type": "dict", "values": reference_dict}
    return VerifyHelper()._verify("", input_dict, reference_dict)


def check_format(doc, rets=True):
    return FormatHelper()._check_format("", doc)


if __name__ == "__main__":
    verify()
