import heapq
from events.event import EventType, Event

class EventQueue:
    def __init__(self, arr = []):
        if all(isinstance(item, Event) for item in arr):
            self.event_list = arr
            heapq.heapify(self.event_list)
        else:
            raise TypeError("Attempted to put non-Event type in event queue")
    
    def __next__(self) -> Event:
        return heapq.heappop(self.event_list)
    
    def push(self, event: Event):
        heapq.heappush(self.event_list, event)

    def pop(self, event: Event):
        return next(self)

    def empty(self):
        return len(self.event_list) == 0