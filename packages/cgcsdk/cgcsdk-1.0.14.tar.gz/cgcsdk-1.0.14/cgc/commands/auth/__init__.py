from cgc.commands.exceptions import ResponseException


class AuthCommandException(ResponseException):
    pass


class NoNamespaceInConfig(AuthCommandException):
    def __init__(self) -> None:
        super().__init__("Namespace not readable from config file.")


class NoConfigFileFound(AuthCommandException):
    def __init__(self) -> None:
        super().__init__("Config does not exists.")
