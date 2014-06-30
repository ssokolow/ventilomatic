"""Ventilomatic rules

(As the Pythonistas say, why reinvent a domain-specific language when you
 don't need to?)
"""

__author__ = "Stephan Sokolow (deitarion/SSokolow)"
__license__ = "GNU GPL 2 or later"

import logging
log = logging.getLogger(__name__)

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
            call_x10(self.lights, False)

class NoDampCorners(object):
    """Use fans to relocate humid air before it can make corners musty."""

    min_diff = 5.0     # When the fans should turn off
    max_diff = 10.0    # When the fans should turn on
    fan_state = None

    def __init__(self, baseline_sensor_id, corner_sensor_id, fans):
        self.baseline_sensor = baseline_sensor_id
        self.corner_sensor = corner_sensor_id
        self.fans = fans

    def __call__(self, model):
        rh_vals = {x: model.get(x, {}).get('humidity') for x in
                (self.baseline_sensor, self.corner_sensor)}

        for name, value in rh_vals.items():
            if value is None:
                log.error("Could not read humidity from %s", name)
                return

        humid_diff = abs(rh_vals.values()[0] - rh_vals.values()[1])

        if humid_diff > self.max_diff and not self.fan_state is True:
            call_x10(self.fans, True)
            self.fan_state = True
        elif humid_diff < self.min_diff and not self.fan_state is False:
            call_x10(self.fans, False)
            self.fan_state = False

RULES = [
    WasteNoLight('corner', [1, 2, 6]),
    NoDampCorners('desktop', 'corner', 3)
]
