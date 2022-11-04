from enum import Enum


class ErrorMode(Enum):
    """Enumerated error-handling strategies"""

    RAISE = "raise"
    WARN = "warn"
