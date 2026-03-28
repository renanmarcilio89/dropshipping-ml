class PipelineError(Exception):
    """Base exception for the project."""


class ConfigurationError(PipelineError):
    """Raised when configuration is invalid or incomplete."""


class MeliAPIError(Exception):
    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
