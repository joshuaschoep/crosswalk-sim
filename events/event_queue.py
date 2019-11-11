import heapq
from event import EventType, Event

class EventQueue:
    def __init__(list = []):
        if all(isinstance(item, Event) for item in list):
            self.event_list = heapq.heapify(list)
        else:
            raise TypeError("Attempted to put non-Event type in event queue")
    
    def __next__() -> Event:
        return heapq.heappop(list)
    
    def push(event: Event):
        heapq.heappush(event)

    def pop(event: Event):
        return next(self)