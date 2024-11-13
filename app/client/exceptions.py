class ClientException(Exception):
    pass

class ClientHTTPException(ClientException):
    pass

class ClientHTTPStatusException(ClientHTTPException):
    pass


class ClientHTTPEmptyResponseException(ClientHTTPException):
    pass
