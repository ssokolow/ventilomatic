"""Ventilomatic rules

(As the Pythonistas say, why reinvent a domain-specific language when you
 don't need to?)
"""

__author__ = "Stephan Sokolow (deitarion/SSokolow)"
__license__ = "GNU GPL 2 or later"

from actions import call_x10

class WasteNoLight(object):
    """Turn off specified room lights when a specified sensor detects too
       much light.
    """
    def __init__(self, sensor_id, room_lights):
        self.sensor_id = sensor_id
        self.lights = room_lights
        self.brightness = 0

    #TODO: I'll probably want to separate tests from actions to allow for a
    #      smarter core system and easy logging without duplication.
    def __call__(self, model):
        corner_brightness = model.get('corner', {}).get('light', 0)
        if corner_brightness > 750:
            # Send each message twice to account for X10 bus noise
            for dev in self.lights:
                for _ in range(2):
                    call_x10(dev, False)

RULES = [
    WasteNoLight('corner', [1, 2, 6])
]
