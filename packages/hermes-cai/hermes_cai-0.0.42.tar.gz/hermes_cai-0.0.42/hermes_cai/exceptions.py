"""Custom exceptions for the Hermes engine."""


class InvalidPromptError(Exception):
    """Invalid prompt error."""


class TokenLimitExceededError(Exception):
    """Token limit exceeded error."""


class TimestampStrNotFoundError(Exception):
    """Timestamp string not found error."""


class TimestampIdxNotFoundError(Exception):
    """Timestamp index not found error."""


class MessageStartIdxNotFound(Exception):
    """Message start index not found error."""


class MissingContextData(Exception):
    """Missing context data error."""


class TemplateNotFoundError(Exception):
    """Template not found error."""
