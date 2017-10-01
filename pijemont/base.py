from pijemont.exceptions import PijemontKeyError


class PijemontHelper:
    def __init__(self, raise_on_error=False, verbose=False):
        self.errors = []
        self.verbose = verbose
        self.raise_on_error = raise_on_error

    def handle_error(self, error):
        self.errors.append(str(error))
        if self.verbose:
            print(error)
        if self.raise_on_error:
            raise error

    def _check_keys(self, name, doc, keys):
        for key in keys:
            if key not in doc:
                self.handle_error(PijemontKeyError(name, key))