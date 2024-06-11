"""
Main implementation for withwait
"""
from types import TracebackType
from typing import ContextManager, Union, NoReturn
from typing_extensions import Self
from time import time, sleep


class wait(ContextManager):
    """
    Withwait

    Ensure a timer always finishes, even if an exception happens for code
    inside a with statement
    """
    def __init__(self, seconds: float) -> None:
        """
        Withwait

        Ensure a timer always finishes, even if an exception happens for code
        inside a with statement

        ## Args
        * `seconds` (`float`): number of seconds to wait
        """
        self.__seconds = seconds
        # Set when entering context manager
        self.__start_time: float = 0

    def cancel(self) -> NoReturn:
        """
        Stop the timer and resume normal running at the end of the `with`
        statement

        ## Example

        ```py
        with wait(1) as timer:
            # Stop the timer
            timer.cancel()
            # Code after this point in the with statement won't be run

        # Program flow resumes normally after
        print("Ok")
        ```
        """
        raise _WithwaitCancel(self)

    def abort(self, *args) -> NoReturn:
        """
        Abort the timer and raise a WithwaitAbort exception at the end of the
        `with` statement

        ## Args

        * `*args` (`Any`): arguments to provide in the exception

        ## Example

        ```py
        try:
            with wait(1) as timer:
                # Abort the timer
                timer.abort()
                # Code after this point in the
                # with statement won't be run

            # Code after the with statement won't be run either
            print("Nope")

        # We need to catch the exception ourselves
        except WithwaitAbort:
            print("Caught")
        ```
        """
        raise _WithwaitAbortInternal(self, *args)

    def abort_all(self, *args) -> NoReturn:
        """
        Abort all running times and raise a WithwaitAbortAll exception
        """
        raise WithwaitAbortAll(*args)

    def __enter__(self) -> Self:
        self.__start_time = time()
        return self

    def __exit__(
        self,
        __exc_type: Union[type[BaseException], None],
        __exc_value: Union[BaseException, None],
        __traceback: Union[TracebackType, None],
    ) -> bool:
        # Check if the timer was cancelled
        if isinstance(__exc_value, _WithwaitCancel):
            # Only if it matches this timer
            if __exc_value.matches(self):
                # Swallow the exception
                return True

        # Or if it was aborted
        if isinstance(__exc_value, _WithwaitAbortInternal):
            # Only if it matches this timer
            if __exc_value.matches(self):
                # Raise a new exception instead
                raise WithwaitAbort(*__exc_value.args) from __exc_value

        # Or if all timers are being aborted
        if isinstance(__exc_value, WithwaitAbortAll):
            # Don't swallow the exception
            return False

        time_to_sleep = self.__seconds - (time() - self.__start_time)
        # Wait the remaining required time if needed
        if time_to_sleep > 0:
            sleep(time_to_sleep)
        return False


class _WithwaitCancel(BaseException):
    """
    Exception used to cancel waiting if required.

    Derived from BaseException so that it can't be easily caught.
    """
    def __init__(self, timer: wait) -> None:
        """
        Exception used to cancel waiting if required

        Derived from BaseException so that it can't be easily caught.

        Args:
        * `timer` (`wait`): timer to match with
        """
        self.__timer = timer

    def matches(self, timer: wait):
        """
        Returns whether the timer matches this particular exception
        """
        return self.__timer == timer


class _WithwaitAbortInternal(BaseException):
    """
    Exception used to abort waiting if required.

    Derived from BaseException so that it can't be easily caught.

    When leaving the context, this is replaced with a regular WithwaitAbort
    exception
    """
    def __init__(self, timer: wait, *args: object) -> None:
        """
        Exception used to abort waiting if required.

        Args:
        * `timer` (`wait`): timer to match with
        * `args` (`Any`): other arguments for the exception
        """
        self.__timer = timer
        super().__init__(*args)

    def matches(self, timer: wait):
        """
        Returns whether the timer matches this particular exception
        """
        return self.__timer == timer


class WithwaitAbort(Exception):
    """
    Exception used to abort waiting if required.
    """


class WithwaitAbortAll(BaseException):
    """
    Exception used to abort waiting for all timers.
    """
