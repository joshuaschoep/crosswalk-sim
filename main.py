from events.event_queue import EventQueue
from events.event import Event, EventType
from variates import exponential_1

event_queue = EventQueue()
autos_left = 0
peds_left = 0

autos_generator = None
peds_generator = None
button_generator = None 

def start( N: int, autos_g, pedestrians_g, button_g ):
    global event_queue, autos_left, peds_left
    global autos_generator, peds_generator, button_generator

    #Begin end conditons
    autos_left = N
    peds_left = N

    #Init all generators
    autos_generator = autos_g
    peds_generator = pedestrians_g
    button_generator = button_g

    #Initialize all beginning arrival events
    event_queue.push(Event(EventType.PED_ARRIVAL, exponential_1(float(next(peds_generator))), {"Direction": "EAST"}))
    event_queue.push(Event(EventType.PED_ARRIVAL, exponential_1(float(next(peds_generator))), {"Direction": "WEST"}))
    event_queue.push(Event(EventType.AUTO_ARRIVAL, exponential_1(float(next(autos_generator))), {"Direction": "EAST"}))
    event_queue.push(Event(EventType.AUTO_ARRIVAL, exponential_1(float(next(autos_generator))), {"Direction": "WEST"}))

    #EVENT LOOP
    while not event_queue.empty():
        nextEvent = next(event_queue)
        processEvent(nextEvent)
    
def processEvent(event: Event):
    print(event)
    if event.type == EventType.PED_ARRIVAL:
        handlePedArrival(event)
    elif event.type == EventType.AUTO_ARRIVAL:
        handleCarArrival(event)


##EVENT PROCESSING
def handlePedArrival(event: Event):
    global peds_left

    if peds_left > 0:
        at = exponential_1(float(next(peds_generator))) + event.at
        direction = event.metadata["Direction"]
        newPed = Event(EventType.PED_ARRIVAL, at, {"Direction": direction})

        event_queue.push(newPed)
        peds_left -= 1

def handleCarArrival(event: Event):
    global autos_left

    if autos_left > 0:
        at = exponential_1(float(next(autos_generator))) + event.at
        direction = event.metadata["Direction"]
        newAuto = Event(EventType.AUTO_ARRIVAL, at, {"Direction": direction})

        event_queue.push(newAuto)
        autos_left -= 1