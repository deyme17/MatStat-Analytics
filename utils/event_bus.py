from typing import Callable, Dict, List, Any
from enum import Enum, auto


class EventType(Enum):
    """Event types"""
    # Data events
    DATA_LOADED = auto()
    DATA_TRANSFORMED = auto()
    DATA_REVERTED = auto()
    DATA_EXPORTED = auto()
    DATASET_CHANGED = auto()
    COLUMN_CHANGED = auto()
    
    # UI events
    BINS_CHANGED = auto()
    CONFIDENCE_CHANGED = auto()
    PRECISION_CHANGED = auto()
    DISTRIBUTION_CHANGED = auto()
    
    # State events
    MISSING_VALUES_DETECTED = auto()
    MISSING_VALUES_HANDLED = auto()


class Event:
    """Event with data"""
    def __init__(self, event_type: EventType, data: Any = None):
        self.type = event_type
        self.data = data


class EventBus:
    def __init__(self):
        self._subscribers: Dict[EventType, List[Callable]] = {}
    
    def subscribe(self, event_type: EventType, callback: Callable[[Event], None]) -> None:
        """Subscribe on the event"""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type: EventType, callback: Callable[[Event], None]) -> None:
        """Unsubscribe fron the event"""
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(callback)
    
    def emit(self, event: Event) -> None:
        """Calls all subscribed events"""
        if event.type in self._subscribers:
            for callback in self._subscribers[event.type]:
                try:
                    callback(event)
                except Exception as e:
                    print(f"Error in event handler for {event.type}: {e}")
    
    def emit_type(self, event_type: EventType, data: Any = None) -> None:
        """Fast call of all the subscribed events"""
        self.emit(Event(event_type, data))