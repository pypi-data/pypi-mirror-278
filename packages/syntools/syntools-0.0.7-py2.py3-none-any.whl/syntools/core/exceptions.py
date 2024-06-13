import os
import traceback


class SynToolsError(Exception):
    """Generic exception."""

    def __init__(self, message, can_retry=False, retry_modifier=2, retry_max=10, child_error=None):
        self.original_message = message
        self.can_retry = can_retry
        self.retry_modifier = retry_modifier
        self.retry_max = retry_max
        self.child_error = child_error
        if child_error is not None:
            if isinstance(child_error, Exception):
                message = '{0}{1}{2}'.format(message, os.linesep, self.__class__.format_exception(child_error))
                if isinstance(child_error, SynToolsError):
                    self.can_retry = child_error.can_retry
                    self.retry_modifier = child_error.retry_modifier
                    self.retry_max = child_error.retry_max
            else:
                raise Exception('child_error must be an Exception class.')
        super().__init__(message)

    @classmethod
    def format_exception(cls, e):
        ex_message = str(e)
        ex_stack_trace = traceback.format_exc()
        return '{0}{1}{2}'.format(ex_message, os.linesep, ex_stack_trace)


class FileSizeMismatchError(SynToolsError, IOError):
    """Error raised when the size for a download file fails to match the size of its file handle."""

    def __init__(self, message, can_retry=False, retry_modifier=2, retry_max=10, child_error=None):
        super().__init__(
            message,
            can_retry=can_retry,
            retry_modifier=retry_modifier,
            retry_max=retry_max,
            child_error=child_error
        )


class Md5MismatchError(SynToolsError, IOError):
    """Error raised when MD5 computed for a download file fails to match the MD5 of its file handle."""

    def __init__(self, message, can_retry=False, retry_modifier=2, retry_max=10, child_error=None):
        super().__init__(
            message,
            can_retry=can_retry,
            retry_modifier=retry_modifier,
            retry_max=retry_max,
            child_error=child_error
        )
