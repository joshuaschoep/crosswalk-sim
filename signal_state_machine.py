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
    def __init__():
        self.currentState = GREEN_UNPRESSED
        self.greenTimer = GREEN_TIMER_LENGTH
        self.event_queue = global event_queue
    
    def handle_event(event: Event)
    
    def press_button():
        if self.current_state == SignalState.GREEN_UNPRESSED:
            self.current_state = SignalState.GREEN_PRESSED
        elif self.current_state SignalState.