from .sensor import Sensor

import collections
import copy
import time

class SuspensionAccel(Sensor):
    _name = "accel"
    _location = "suspension"
    _buffer = collections.deque(maxlen=10)

    def handle_status_update(self,msg_json):
        self._last_update = time.time()
        self._buffer.append( (float(msg_json["x"]), float(msg_json["y"]), float(msg_json["z"])) )

    def rolling_avg(self):
        total = [0,0,0]
        _temp_buffer = copy.copy(self._buffer)
        for v in _temp_buffer:
            for i in range(3):
                total[i] += float(v[i])

        return (total[0] / len(_temp_buffer),
                total[1] / len(_temp_buffer),
                total[2] / len(_temp_buffer))

    def __repr__(self):
        if len(self._buffer) > 0:
            v = self._buffer[-1]
            avg = self.rolling_avg()
            return self._location + "/" + \
                self._name + "(" + \
                "raw: ({:0.3f}, {:0.3f}, {:0.3f}) ".format(v[0],v[1],v[2]) + \
                "avg: ({:0.3f}, {:0.3f}, {:0.3f})".format(avg[0], avg[1], avg[2]) + \
                ") " + str(self.last_update()) + "s"

        return self._location + "/" + \
            self._name + "() " + str(self.last_update()) + "s"
