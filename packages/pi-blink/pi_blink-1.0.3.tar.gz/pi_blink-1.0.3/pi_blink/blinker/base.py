import collections.abc as c
import typing as t
from inspect import iscoroutinefunction
from typing import Any, Optional

from blinker.base import Signal as BlinkerSignal
from pydantic import BaseModel, ConfigDict, Field

from pi_blink.events import StopEvent
from pi_blink.utils.id_utils import get_full_class_name


class SignalReturn(BaseModel):
    listeners: list[Any] = Field(
        default_factory=list, description="The listeners that were called."
    )
    results: list[Any] = Field(default_factory=list, description="The results from the listeners.")
    stopped: bool = Field(default=False, description="Whether the signal was stopped.")
    stop_event: Optional[StopEvent] = Field(
        default=None, description="The stop event that stopped the signal."
    )
    errors: list[Exception] = Field(
        default_factory=list, description="The errors that occurred during the signal."
    )
    error_listeners: list[Any] = Field(
        default_factory=list, description="The listeners that had errors."
    )

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Signal(BlinkerSignal):

    def extended_send(
        self,
        sender: t.Any | None = None,
        ignore_errors: bool = False,
        *,
        _async_wrapper: (
            c.Callable[[c.Callable[..., c.Coroutine[t.Any, t.Any, t.Any]]], c.Callable[..., t.Any]]
            | None
        ) = None,
        **kwargs: t.Any,
    ) -> SignalReturn:
        """Extends blinker.send to support cancelling receivers.\n
        Returns has also been modified to return a SignalReturn object.\n

        \n{0}""".format(
            BlinkerSignal.send.__doc__
        )

        sr = SignalReturn()
        if self.is_muted:
            return sr

        for receiver in self.receivers_for(sender):

            try:
                if iscoroutinefunction(receiver):
                    if _async_wrapper is None:
                        raise RuntimeError("Cannot send to a coroutine function.")
                    result = _async_wrapper(receiver)(sender, **kwargs)
                else:
                    result = receiver(sender, **kwargs)
            except Exception as e:
                if ignore_errors:
                    sr.errors.append(e)
                    sr.error_listeners.append(receiver)
                    continue
                raise e
            ## Last element of the result tuple is a potential stop event
            potential_stop = result
            if isinstance(result, tuple):
                result, potential_stop = result[:-1], result[-1]
                if len(result) == 1:
                    result = result[0]

            if isinstance(potential_stop, StopEvent):

                if result != potential_stop:  ## They want to add a result and stop
                    sr.results.append(result)
                    sr.listeners.append(receiver)

                sr.stopped = True
                sr.stop_event = potential_stop
                sr.stop_event.stopped_by = get_full_class_name(receiver)
                return sr
            sr.listeners.append(receiver)
            sr.results.append(result)

        return sr

    async def extended_send_async(
        self,
        sender: t.Any | None = None,
        ignore_errors: bool = False,
        *,
        _sync_wrapper: (
            c.Callable[[c.Callable[..., t.Any]], c.Callable[..., c.Coroutine[t.Any, t.Any, t.Any]]]
            | None
        ) = None,
        **kwargs: t.Any,
    ) -> SignalReturn:
        """Extends blinker.send_async to support cancelling receivers.\n
        Returns has also been modified to return a SignalReturn object.\n
        
        \n{0}""".format(
            BlinkerSignal.send_async.__doc__
        )

        sr = SignalReturn()
        if self.is_muted:
            return sr

        for receiver in self.receivers_for(sender):
            try:
                if not iscoroutinefunction(receiver):
                    if _sync_wrapper is None:
                        raise RuntimeError("Cannot send to a non-coroutine function.")
                    result = await _sync_wrapper(receiver)(sender, **kwargs)
                else:
                    result = await receiver(sender, **kwargs)
            except Exception as e:
                if ignore_errors:
                    sr.errors.append(e)
                    sr.error_listeners.append(receiver)
                    continue
                raise e
            ## Last element of the result tuple is a potential stop event
            potential_stop = result
            if isinstance(result, tuple):
                result, potential_stop = result[:-1], result[-1]
                if len(result) == 1:
                    result = result[0]

            if isinstance(potential_stop, StopEvent):
                if result != potential_stop:  ## They want to add a result and stop
                    sr.results.append(result)
                    sr.listeners.append(receiver)
                sr.stopped = True
                sr.stop_event = potential_stop
                sr.stop_event.stopped_by = get_full_class_name(receiver)
                return sr
            sr.listeners.append(receiver)
            sr.results.append(result)

        return sr
