class InvalidConfigValue(Exception):
    def __init__(self, section: str, key: str, error: Exception) -> None:
        message: str = f'The value under key \'{key}\' in section \'{section}\' is invalid, {error}'
        super().__init__(message)
