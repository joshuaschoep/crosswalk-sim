from enum import Enum

class EventType(Enum):
    AUTO_ARRIVAL = 0
    PED_ARRIVAL = 1
    PED_AT_BUTTON = 2
    PED_IMPATIENT = 3
    GREEN_EXPIRES = 4
    YELLOW_EXPIRES = 5
    RED_EXPIRES = 6
    AUTO_EXIT = 7
    PED_EXIT = 8

class Event:
    def __init__(type: EventType, at: float, metadata: dict):
        this.type = type
        this.at = at
        this.metadata = metadata