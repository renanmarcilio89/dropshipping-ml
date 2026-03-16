class PipelineError(Exception):
    """Base exception for the project."""


class ConfigurationError(PipelineError):
    """Raised when configuration is invalid or incomplete."""


class MeliAPIError(PipelineError):
    """Raised for Mercado Livre API failures."""
