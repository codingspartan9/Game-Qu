from game_qu.base.events import Event, TimedEvent
from game_qu.library_abstraction import keys
from game_qu.library_abstraction import utility_functions


class Keyboard:
    """ A class that has key_events and key_timed_events that are used to find key states like how long a key was held in,
        if a key was released, etc. Generally it is recommended to use the functions from game_qu.base/utility_functions.py
        but the key_events and key_timed_events from this class can also be used."""

    key_events = []
    key_timed_events = []
    mouse_clicked_event = Event()

    def __init__(self):
        """Initializes all the key events"""

        for x in range(len(keys.keys)):
            self.key_events.append(Event())
            self.key_timed_events.append(TimedEvent(0))
    
    def get_key_timed_event(self, key):
        """:returns: TimedEvent; the TimedEvent associated with that key"""

        return self.key_timed_events[key]

    def get_key_event(self, key):
        """:returns: Event; the Event associated with that key"""

        return self.key_events[key]

    def run(self):
        """ Runs all the events in key_events and key_timed_events, so attributes about the keys can be viewed. This function
            SHOULD NOT be called by the user and this library automatically calls it"""

        self.mouse_clicked_event.run(utility_functions.mouse_was_pressed())

        for key in keys.keys:
            key_was_pressed = utility_functions.key_is_pressed(key)

            self.get_key_event(key).run(key_was_pressed)

            should_reset = not self.get_key_event(key).happened_last_cycle() and not key_was_pressed

            self.get_key_timed_event(key).run(should_reset, key_was_pressed)


