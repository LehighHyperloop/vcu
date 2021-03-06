import json
import string
import time

class Subsystem():
    _client = None
    hw_map = None

    _prefix = "subsystem/"

    _states        = None
    _states_array  = None
    _default_state = None

    _t_state = None
    _state   = None

    def __init__(self, client, hw_map):
        self._client = client
        self.hw_map = hw_map
        self._states_array = [ k for k,v in self._states.iteritems() ]

        self._t_state = self._default_state
        self._state = self._default_state

        self._client.debug(self._name + " init to " + self._state)

    def get_topic(self):
        return None

    def get_state(self):
        return self._state

    def get_attributes(self):
        return {
            "t_state": self._t_state,
            "state": self._state
        }

    def state_transitions(self, current, target):
        func = self._states[current]
        if func:
            new = func(self, target)
            return new
        return False

    _time_in_state = None
    def set_state(self, new_state):
        self._time_in_state = time.time()
        self._client.debug("Transition " + self._name + " from " + self._state + " to " + new_state)
        self._state = new_state

    def time_in_state(self):
        return time.time() - self._time_in_state

    def update(self):
        new_state = self.state_transitions(self._state, self._t_state)
        if new_state:
            self.set_state(new_state)
        self.send_heartbeat()

    def set_target_state(self, target_state):
        if target_state in self._states:
            self._t_state = target_state
        else:
            print "Unrecognized state: " + target_state

    def send_heartbeat(self):
        # Send status updates
        self._client.publish(self._prefix + self._name, json.dumps(self.get_attributes()))

    def __repr__(self):
        return self._name + "(" + \
            string.join([ k + ": " + str(v) for k, v in self.get_attributes().iteritems() ], ", ") + \
            ")"
