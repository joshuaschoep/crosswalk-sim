from events.event_queue import EventQueue

event_queue = EventQueue()

def start( N: int, autos_generator, pedestrians_generator, button_generator ):
    print("Hello world!", next(autos_generator))
    
