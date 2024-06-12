import logging
import multiprocessing
import threading
from collections import defaultdict
from dataclasses import dataclass, field
from enum import IntEnum
from functools import wraps
from inspect import iscoroutinefunction
from multiprocessing import Lock
from typing import Any, Callable, Optional

from blinker._utilities import make_id
from blinker.base import ANY, ANY_ID

from pi_blink.blinker.base import Signal
from pi_blink.ordered_set import OrderedSet
from pi_blink.utils.id_utils import get_full_class_name

log = logging.getLogger(__name__)


class EventPriority(IntEnum):
    """Enum class for event priorities.
    Initial will be the first to be called, Monitor will be the last.
    Monitor is used for listeners that need to monitor the event
    and shouldn't change the event.
    """

    INITIAL = 0
    EARLIEST = 10
    EARLIER = 20
    EARLY = 30
    NORMAL = 40
    LATE = 50
    LATER = 60
    LATEST = 70
    LAST = 80
    MONITOR = 90


# Define a class for the event
@dataclass
class PriorityListener:
    """Listener function with priority."""

    listener: Callable
    priority: EventPriority = field(default_factory=lambda: EventPriority.NORMAL)

    def __post_init__(self):
        if self.priority is None:
            self.priority = EventPriority.NORMAL

    def __lt__(self, other):
        return self.priority < other.priority

    def __gt__(self, other):
        return self.priority > other.priority

    def __le__(self, other):
        return self.priority <= other.priority

    def __ge__(self, other):
        return self.priority >= other.priority

    def __ne__(self, other):
        return self.priority != other.priority

    def __eq__(self, other):
        return self.priority == other.priority

    def __hash__(self):
        return hash(self.priority)

    def __repr__(self):
        return f"PL({self.listener} -[{self.priority.name} {self.priority.value}])"


class ListenerRegistry:
    """Singleton class for the listener registry."""

    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ListenerRegistry, cls).__new__(cls)
                cls._instance._initialize()
            return cls._instance

    def _initialize(self) -> None:
        self.receiver_priorities: dict[Any, dict[Any, EventPriority]] = defaultdict(dict)
        self._signals: dict[str, Signal] = {}

    def register_listener(
        self,
        signal_class: type,
        func: Callable,
        sender: Any,
        weak: bool = True,
        priority: Optional[EventPriority] = None,
    ):
        """
        Register a listener for a signal class.
        """
        sn = get_full_class_name(signal_class)
        fn = func.__module__ + "." + func.__name__
        priority = priority or EventPriority.NORMAL
        fid = make_id(func)

        ## sender_id mimics base.py
        sender_id = ANY_ID if sender is ANY else make_id(sender)
        rps = self.receiver_priorities[sn]
        rps[fid] = priority

        if sn not in self._signals:
            self._signals[sn] = Signal(sn)

        sig = self._signals[sn]

        sig.connect(func, sender=sender, weak=weak)

        ## Reorder the receivers by priority
        new_by_sender: dict[Any, set[Any]] = defaultdict(OrderedSet)
        for sender_id, receiver_set in sig._by_sender.items():
            ## sort the new receiver set by priority
            d = {k: rps.get(k, EventPriority.NORMAL) for k in receiver_set}
            sorted_items = sorted(d.items(), key=lambda i: i[1])
            new_by_sender[sender_id] = OrderedSet([k for k, _ in sorted_items])
        sig._by_sender = new_by_sender

        log.debug(
            f"Registering listener: {func} {fn} {sn} thread: {threading.get_ident()} nsig: {len(self._signals)}, process_id: {multiprocessing.current_process()}"
        )

    def send_event(self, event: Any, sender: Any = None):
        """
        Send an event to all listeners of the event.
        Args:
            event (Any): The event object.
            sender (Any): The sender of the event.
        """
        log.debug(
            f"Sending event: {event} {sender}: thread: {threading.get_ident()} nsig: {len(self._signals)}, process_id: {multiprocessing.current_process()}"
        )
        sig = self._signals.get(get_full_class_name(event))
        if not sig:
            raise ValueError(
                f"No signal found for event: {get_full_class_name(event)}, sender: {sender}"
            )
        return sig.extended_send(event)

    async def asend_event(self, event: Any, sender: Any = None):
        """
        Send an event to all listeners of the event asynchronously.
        Args:
            event (Any): The event to send.
            sender (Any): The sender of the event.

        """
        log.debug(
            f"Async sending event: {event} {sender}: thread: {threading.get_ident()} nsig: {len(self._signals)}, process_id: {multiprocessing.current_process()}"
        )

        sig = self._signals.get(get_full_class_name(event))
        if not sig:
            raise ValueError(
                f"No signal found for event: {get_full_class_name(event)}, sender: {sender}"
            )
        await sig.extended_send_async(event)

    def change_priority(self, signal_class, func, new_priority: EventPriority):
        """Change the priority of a listener.
        Args:
            signal_class (type): The signal class.
            func (Callable): The listener function.
            new_priority (EventPriority): The new priority.

        """
        sn = get_full_class_name(signal_class)
        rps = self.receiver_priorities[sn]
        fid = make_id(func)
        old_priority = rps.get(fid, None)
        if old_priority == new_priority:
            return
        rps[fid] = new_priority
        sig = self._signals[sn]
        new_by_sender: dict[Any, set[Any]] = defaultdict(OrderedSet)
        for sender_id, receiver_set in sig._by_sender.items():
            ## sort the new receiver set by priority
            d = {k: rps.get(k, EventPriority.NORMAL) for k in receiver_set}
            sorted_items = sorted(d.items(), key=lambda i: i[1])
            new_by_sender[sender_id] = OrderedSet([k for k, _ in sorted_items])
        sig._by_sender = new_by_sender

    def delete_listener(self, signal_class, func):
        """Delete a listener."""
        sn = get_full_class_name(signal_class)
        sig = self._signals.get(sn)
        if sig:
            sig.disconnect(func)
        else:
            raise ValueError(f"No signal found for event: {sn}")


# Singleton instance of the registry
_listener_registry = ListenerRegistry()


def listener(signal_class: Any, sender: Any = ANY, priority: Optional[EventPriority] = None):
    """
    Decorator for registering a listener.
    Args:
        signal_class (type): The signal class.
        sender (Any): The sender of the signal.
        priority (EventPriority): The priority of the listener.
    Example:
        class MyEvent:
            pass
        @listener(MyEvent)
        def my_func(event : MyEvent):
            pass
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        _listener_registry.register_listener(
            signal_class, sender=sender, func=wrapper, priority=priority
        )
        return wrapper

    return decorator


def alistener(signal_class: Any, sender: Any = ANY, priority: EventPriority | None = None):
    """
    Decorator for registering an async listener.
    Args:
        signal_class (type): The signal class.
        sender (Any): The sender of the signal.
        priority (EventPriority): The priority of the listener.
    Example:
        class MyEvent:
            pass
        @alistener(MyEvent)
        async def my_func(event : MyEvent):
            pass
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        ## check if is coroutine
        if not iscoroutinefunction(func):
            raise ValueError(
                f"Function {func} is not a coroutine.\n"
                f"Use @listener instead of @alistener, or async def {func}."
            )
        _listener_registry.register_listener(
            signal_class, sender=sender, func=wrapper, priority=priority
        )
        return wrapper

    return decorator


class Blink:
    """
    Class to interface with listeners and events.
    """

    @staticmethod
    def send(event: Any, sender: Any = None):
        """Send an event.
        Args:
            event (Any): The event to send.
            sender (Any): The sender of the event.
        """
        return _listener_registry.send_event(event, sender)

    @staticmethod
    async def asend(event: Any, sender: Any = None):
        """Send an event asynchronously.
        Args:
            event (Any): The event to send.
            sender (Any): The sender of the event.
        """
        return await _listener_registry.asend_event(event, sender)

    @staticmethod
    def change_listener_priority(event: Any, func: Callable, new_priority: EventPriority):
        """Change the priority of a listener.
        Args:
            event (Any): The event class.
            func (Callable): The listener function.
            new_priority (EventPriority): The new priority."""
        _listener_registry.change_priority(event, func, new_priority)

    @staticmethod
    def delete_listener(event: Any, func: Callable):
        """Delete a listener.
        Args:
            event (Any): The event class.
            func (Callable): The listener function.
        """
        _listener_registry.delete_listener(event, func)

    @staticmethod
    def listener(signal_class, sender: Any = ANY, priority: EventPriority | None = None):
        """Register a listener.
        Args:
            signal_class (type): The signal class.
            sender (Any): The sender of the signal.
            priority (EventPriority): The priority of the listener.
        Returns:
            Callable: The listener function.
        """
        return listener(signal_class=signal_class, sender=sender, priority=priority)

    @staticmethod
    def alistener(signal_class: Any, sender: Any = ANY, priority: EventPriority | None = None):
        """Register an async listener.
        Args:
            signal_class (type): The signal class.
            sender (Any): The sender of the signal.
            priority (EventPriority): The priority of the listener.
        Returns:
            Callable: The listener function.
        """
        return alistener(signal_class=signal_class, sender=sender, priority=priority)


blink = Blink  # Alias for Blink class
