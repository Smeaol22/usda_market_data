class UsdaMarketRequestError(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


class UsdaMarketInternalError(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors
