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
    def __init__(self, type: EventType, at: float, metadata: dict):
        self.type = type
        self.at = at
        self.metadata = metadata
    
    def __lt__(self, other):
        if not isinstance(other, Event):
            raise TypeError("Error: comparison of Event type with", type(other))
        return self.at < other.at
    
    def __str__(self):
        base = '\n' + str(self.type) + " event at: " + str(self.at)
        if len(self.metadata) != 0:
            base += "\nData:"
            for key, value in self.metadata.items():
                base += "\n\t" + str(key) + ": " + str(value)
        return base
    
    def __repr__(self):
        string = str(self.type) + " at time " + str(self.at)
        if "Index" in self.metadata:
            string += " with index " + str(self.metadata["Index"])
        return string