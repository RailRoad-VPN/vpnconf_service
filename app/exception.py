class VPNError(object):
    UNKNOWN_ERROR_CODE = 'VPN-000000'


class VPNException(Exception):
    __version__ = 1

    code = None
    message = None
    data = None

    def __init__(self, message: str, code: int, data: dict = None, *args, **kwargs):
        super().__init__(*args)

        self.code = code
        self.message = message
        self.data = data


class APIException(VPNException):
    __version__ = 1

    http_code = None

    def __init__(self, message: str, code: int, http_code: int, data: dict = None, *args, **kwargs):
        super().__init__(message, code, *args, **kwargs)

        self.http_code = http_code
        self.data = data