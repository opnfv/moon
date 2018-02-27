
class BaseException(Exception):
    def __init__(self, message):
        self._code = 500
        self._message = message
        # Call the base class constructor with the parameters it needs
        super(BaseException, self).__init__(message)

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message

    def __str__(self):
        return "Error " + self._code + " " + self.__class__.__name__ + ': ' + self.message