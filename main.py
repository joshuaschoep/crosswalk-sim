from events.event_queue import EventQueue
from events.event import Event, EventType
from variates import exponential_u, uniform_ab
import pedestrians as peds
import signal_state_machine as ssm

event_queue = EventQueue()
autos_left = 0
peds_left = 0
traffic_signal = ssm.TrafficSignal(event_queue)

autos_generator = None
peds_generator = None
button_generator = None 

def start( N: int, autos_g, pedestrians_g, button_g ):
    global event_queue, autos_left, peds_left
    global autos_generator, peds_generator, button_generator

    #Begin end conditons
    autos_left = N - 1
    peds_left = N - 1

    #Init all generators
    autos_generator = autos_g
    peds_generator = pedestrians_g
    button_generator = button_g

    #Initialize all beginning arrival events
    event_queue.push(Event(
        EventType.PED_ARRIVAL, 
        exponential_u(float(next(peds_generator)), 20), 
        {
            "Index": 0,
            "Direction": "EAST", 
            "Speed": uniform_ab(next(peds_generator), 2.6, 4.1)
        }
    ))
    '''event_queue.push(
        Event(EventType.PED_ARRIVAL, 
        exponential_1(float(next(peds_generator))), 
        {
            "Index": 1,
            "Direction": "WEST",
            "Speed": uniform_ab(next(peds_generator), 2.6, 4.1)
        }
    ))'''
    #event_queue.push(Event(EventType.AUTO_ARRIVAL, exponential_1(float(next(autos_generator))), {"Direction": "EAST"}))
    #event_queue.push(Event(EventType.AUTO_ARRIVAL, exponential_1(float(next(autos_generator))), {"Direction": "WEST"}))

    #EVENT LOOP
    while not event_queue.empty():
        nextEvent = next(event_queue)
        processEvent(nextEvent)
    
def processEvent(event: Event):
    print(event)
    if event.type == EventType.PED_ARRIVAL:
        handlePedArrival(event)
    elif event.type == EventType.PED_AT_BUTTON:
        handlePedAtButton(event)
    elif event.type == EventType.PED_IMPATIENT:
        handlePedImpatient(event)
    elif event.type == EventType.AUTO_ARRIVAL:
        handleCarArrival(event)
    elif event.type == EventType.GREEN_EXPIRES:
        traffic_signal.handle_event(event)
    elif event.type == EventType.YELLOW_EXPIRES:
        walk()
        traffic_signal.handle_event(event)
    elif event.type == EventType.RED_EXPIRES:
        traffic_signal.handle_event(event)

## PEDESTRIAN HELPERS
def ped_at_crosswalk(ped: Event):
    print(peds.crosswalk_peds)
    for element in peds.crosswalk_peds:
        if ped.metadata["Index"] == element.metadata["Index"]:
            return True
    return False

def can_walk(ped: Event):
    if traffic_signal.current_state != ssm.SignalState.RED:
        return False
    elif traffic_signal.red_expire < (46 / ped.metadata["Speed"]) + ped.at:
        return False
    return True


def walk():
    n = 20
    i = 0
    while n > 0 and len(peds.crosswalk_peds) > i:
        if can_walk(peds.crosswalk_peds[i]):
            n -= 1
            print("PEDESTRIAN", peds.crosswalk_peds[i].__repr__(), "WALKS")
            peds.crosswalk_peds.pop(i)
        else:
            i += 1


##EVENT PROCESSING
def handlePedArrival(event: Event):
    global peds_left

    if peds_left > 0:
        at = exponential_u(float(next(peds_generator)), 20) + event.at
        direction = event.metadata["Direction"]
        meta = {
            "Index": event.metadata["Index"] + 2,
            "Direction": direction,
            "Speed": uniform_ab(next(peds_generator), 2.6, 4.1)
        }
        newPed = Event(EventType.PED_ARRIVAL, at, meta)

        event_queue.push(newPed)
        peds_left -= 1
    
    ##Pedestrian gets to crosswalk
    arrivalAtCrosswalk = Event(
        EventType.PED_AT_BUTTON,
        event.at + peds.DISTANCE_TO_CROSSWALK / event.metadata["Speed"],
        event.metadata
    )
    event_queue.push(arrivalAtCrosswalk)


def handlePedAtButton(event: Event):
    if len(peds.crosswalk_peds) == 0:
        if float(next(button_generator)) < (15/16):
            traffic_signal.press_button(event.at)
    elif float(next(button_generator)) < 1 / (len(peds.crosswalk_peds) + 1):
        traffic_signal.press_button(event.at)

    peds.crosswalk_peds.append(event)
    
    ## PED_IMPATIENT handles whether the ped would actually press the button, so we don't have to here
    ## If they don't walk immediately, they plan to press the button in a minute.
    if traffic_signal.current_state != ssm.SignalState.RED:
        event_queue.push(Event(
            EventType.PED_IMPATIENT,
            event.at + 60,
            event.metadata
        ))

def handlePedImpatient(event: Event):
    if not ped_at_crosswalk(event):
        print("PEDESTRIAN NO LONGER AT CROSSWALK: EVENT DROPPED")
        return
    else:
        traffic_signal.press_button(event.at)

def handleCarArrival(event: Event):
    global autos_left

    if autos_left > 0:
        at = exponential_1(float(next(autos_generator))) + event.at
        direction = event.metadata["Direction"]
        newAuto = Event(EventType.AUTO_ARRIVAL, at, {"Direction": direction})

        event_queue.push(newAuto)
        autos_left -= 1