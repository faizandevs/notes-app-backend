# app/exceptions.py
class NotFoundError(Exception):
    """Raised when an item is not found."""
    pass

class ForbiddenError(Exception):
    """Raised when access is forbidden (ownership/permission)."""
    pass

class BadRequestError(Exception):
    """Raised for controlled bad requests."""
    pass
