from typing import Optional


class InputError(Exception):
    """Custom exception class used internally in the controller for handling
    errors related to user input."""

    def __init__(
        self,
        reason: str = "An error occurred while processing the input",
        parent_exception: Optional[Exception] = None,
        stack_trace: Optional[str] = None,
    ):
        super().__init__(reason, parent_exception, stack_trace)
        self.reason = reason
        self.parent_exception = parent_exception
        self.stack_trace = stack_trace

    def __str__(self):
        result = self.reason
        if self.parent_exception and str(self.parent_exception) != "":
            result += f": {str(self.parent_exception)}"
        return result
