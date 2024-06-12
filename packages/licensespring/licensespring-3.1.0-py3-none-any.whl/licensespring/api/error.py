from requests import HTTPError


class ClientError(HTTPError):
    def __init__(
        self,
        response,
    ):
        response_json = response.json()

        self.status = response_json.get("status")
        self.code = response_json.get("code")
        self.message = response_json.get("message")

        super(ClientError, self).__init__(self.message)

    def __str__(self):
        return self.message

    def __repr__(self):
        return f"{self.__class__.__name__}(status={self.status}, code={self.code}, message={self.message})"
