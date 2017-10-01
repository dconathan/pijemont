from pijemont.base import PijemontHelper
from pijemont.exceptions import PijemontTypeError, PijemontKeyError, PijemontArgError, PijemontInvalidType, PijemontException
from pijemont.types import VALID_KEYS, ALL_TYPES, VALUES_TYPES, DICT, ONEOF, TUPLE, LIST


class FormatHelper(PijemontHelper):
    def _check_format(self, name, doc):

        if not isinstance(doc, dict):
            self.handle_error(PijemontTypeError(name, doc, dict))
        else:
            if "type" not in doc:
                self.handle_error(PijemontKeyError(name, "type"))
            invalid_keys = set(doc.keys()) - VALID_KEYS
            if invalid_keys:
                self.handle_error(PijemontArgError(name, invalid_keys, VALID_KEYS))

        if self.errors:
            return self.errors

        if doc["type"] not in ALL_TYPES:
            self.handle_error(PijemontInvalidType(name, doc["type"]))

        if doc["type"] in VALUES_TYPES:
            if "values" not in doc:
                self.handle_error(PijemontKeyError(name, "values"))
            elif not isinstance(doc["values"], dict):
                self.handle_error(PijemontTypeError(name + ".values", doc["values"], dict))

        if self.errors:
            return self.errors

        if doc["type"] in DICT | ONEOF | TUPLE:
            for k, v in doc["values"].items():
                self._check_format("{}.{}".format(name, k), v)
        elif doc["type"] in LIST:
            self._check_format("{}.{}".format(name, "values"), doc["values"])

        return self.errors


def check_format(doc, rets=True, raise_on_error=True):
    format_helper = FormatHelper()
    if rets:
        for k, v in doc.items():
            if not isinstance(v, dict):
                format_helper.handle_error(PijemontTypeError(k, v, dict))
            elif "args" in v:
                format_helper._check_format("args.{}".format(k), {"type": "dict", "values": v["args"]})
            elif "rets" in v:
                format_helper._check_format("rets.{}".format(k), {v["rets"]})
    else:
        for k, v in doc.items():
            format_helper._check_format(k, v)

    if format_helper.errors and raise_on_error:
        if len(format_helper.errors) == 1:
            message = "There was 1 error in format of reference_dict: "
        else:
            message = "There were {} errors in format of reference_dict:\n  - ".format(len(format_helper.errors))
        message += "\n  - ".join(format_helper.errors)
        raise PijemontException(message)

    return format_helper.errors