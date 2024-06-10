class EmptyConfigValue(Exception):
    def __init__(self, section: str, key: str) -> None:
        message: str = f'The value under key \'{key}\' in section \'{section}\' is empty.'
        super().__init__(message)
