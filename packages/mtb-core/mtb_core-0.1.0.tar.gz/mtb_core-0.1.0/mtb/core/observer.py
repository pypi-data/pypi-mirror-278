import asyncio, weakref
from typing import Any, Callable, Set

from .log import mklog

log = mklog(__name__)


class Observable:
    """
    Base class for objects that can inform observers of changes
    Attributes:
        _observers (Set[weakref]): Weak references to observers
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes this observable object
        """
        self._observers: Set[weakref.ReferenceType[Observer]] = set()

    def cleanup(self):
        """
        Removes any garbage collected observers
        """
        self._observers = set(ref for ref in self._observers if ref() is not None)

    def subscribe(self, observer):
        """
        Adds an observer to be informed of changes
        Parameters:
            observer (types.Observer): Observer to add
        """
        ref = weakref.ref(observer)
        if ref not in self._observers:
            self._observers.add(ref)

    def unsubscribe(self, observer):
        """
        Removes an observer from being informed of changes
        Parameters:
            observer (types.Observer): Observer to remove
        """
        ref = weakref.ref(observer)
        if ref in self._observers:
            self._observers.remove(ref)
            observer.close()

    def notify(self, *args, **kwargs):
        """
        Notifies subscribed observers of a change
        """
        self.cleanup()
        current_observers = list(self._observers)
        print(current_observers)
        for ref in current_observers:
            observer = ref()
            if not asyncio.iscoroutinefunction(observer.update):
                observer.update(self, *args, **kwargs)
            else:
                log.error(
                    f"The observer's update method is a coroutine. ({observer}), please use notify_async and await it"
                )
                continue

    async def notify_async(self, *args, **kwargs):
        """
        Asynchronous notification to all observers.
        """
        self.cleanup()
        loop = asyncio.get_event_loop()

        async_tasks = []
        current_observers = list(self._observers)

        for ref in current_observers:
            observer = ref()
            if asyncio.iscoroutinefunction(observer.update):
                task = loop.create_task(observer.update(self, *args, **kwargs))
                async_tasks.append(task)
            else:
                observer.update(self, *args, **kwargs)

        await asyncio.gather(*async_tasks)


class Observer:
    """
    Interface for an object to be informed of changes in observable objects
    """

    def close(self):
        """
        Optional method to implement. Called when observer is unsubscribed.
        """
        pass

    def update(self, observable, *args, **kwargs):
        """
        Abstract method to update an observation
        Parameters:
            observable (types.Observable): Object being observed
        Raises: NotImplementedError
        """
        raise NotImplementedError


class Property(Observable):
    """
    Generic property that can be observed for changes in value
    Attributes:
        _value (Any): Property value
    """

    def __init__(self):
        """
        Initializes this property
        """
        super().__init__()
        self._value = None

    def __format__(self, format_spec: str) -> str:
        """
        Formats this object as a string
        Parameters:
            format_spec (str): Format specification
        Returns:
            str: This object formatted as a string
        """
        return format(self._value, format_spec)

    def __repr__(self) -> str:
        """
        Represents this object as a string
        Returns:
            str: This object represented as a string
        """
        return repr(self._value)

    def __str__(self) -> str:
        """
        Converts this object to a string
        Returns:
            str: This object converted to a string
        """
        return str(self._value)

    def get(self) -> Any:
        """
        Getter for the value of this property
        Returns:
            Any: Property value
        """
        return self._value

    def set(self, value: Any):
        """
        Setter for the value of this property
        Parameters:
            value (Any): Value to set
        """
        print(value)
        if value != self._value:
            self._value = value
            self.notify()
