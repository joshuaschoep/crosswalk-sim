from enum import Enum
from events.event import Event, EventType

GREEN_TIMER_LENGTH = 35
YELLOW_TIMER_LENGTH = 8
RED_TIMER_LENGTH = 18

class SignalState(Enum):
    GREEN_UNPRESSED = 0
    GREEN_PRESSED = 1
    GREEN_TIMED_OUT = 2
    YELLOW = 3
    RED = 4

class TrafficSignal:
    def __init__(self, event_queue):
        self.event_queue = event_queue
        self.current_state = SignalState.GREEN_UNPRESSED
        self.red_expire = 0
        self.event_queue.push(Event(EventType.GREEN_EXPIRES, GREEN_TIMER_LENGTH, {}))
    
    def handle_event(self, event: Event):
        if event.type == EventType.GREEN_EXPIRES:
            if self.current_state == SignalState.GREEN_PRESSED:
                at = event.at + YELLOW_TIMER_LENGTH
                self.event_queue.push(Event(EventType.YELLOW_EXPIRES, at, {}))
                self.current_state = SignalState.YELLOW
            elif self.current_state == SignalState.GREEN_UNPRESSED:
                self.current_state = SignalState.GREEN_TIMED_OUT                     
        elif event.type == EventType.YELLOW_EXPIRES:
            at = event.at + RED_TIMER_LENGTH
            self.event_queue.push(Event(EventType.RED_EXPIRES, at, {}))
            self.current_state = SignalState.RED
            self.red_expire = event.at + RED_TIMER_LENGTH
        elif event.type == EventType.RED_EXPIRES:
            at = event.at + GREEN_TIMER_LENGTH
            self.event_queue.push(Event(EventType.GREEN_EXPIRES, at, {}))
            self.current_state = SignalState.GREEN_UNPRESSED

    
    def press_button(self, time: float):
        if self.current_state == SignalState.GREEN_UNPRESSED:
            self.current_state = SignalState.GREEN_PRESSED
        elif self.current_state == SignalState.GREEN_TIMED_OUT:
            at = time + YELLOW_TIMER_LENGTH
            self.event_queue.push(Event(EventType.YELLOW_EXPIRES, at, {}))
            self.current_state = SignalState.YELLOW