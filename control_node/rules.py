"""Ventilomatic rules

(As the Pythonistas say, why reinvent a domain-specific language when you
 don't need to?)
"""

__author__ = "Stephan Sokolow (deitarion/SSokolow)"
__license__ = "GNU GPL 2 or later"

import logging, time
log = logging.getLogger(__name__)

from actions import call_x10, get_yahoo_weather, notify_user

class CheckExternalTemperature(object):
    """Use Yahoo! Weather to get the external temperature and use libnotify
    to fire off a notification if it's possible to approach a target
    temperature by opening the window.
    """
    min_interval = 30  # Minutes

    def __init__(self, sensor_id, target_temp, woeid):
        self.sensor_id = sensor_id
        self.target_temp = target_temp
        self.woeid = woeid
        self.last_notified = 0

    def __call__(self, model):
        now = time.time()
        if (now - self.last_notified) < (self.min_interval * 60):
            return
        else:
            self.last_notified = now

        int_temp = model.get(self.sensor_id, {}).get('temperature')
        ext_temp = get_yahoo_weather(self.woeid).condition.temperature

        if abs(int_temp - self.target_temp) > abs(ext_temp - self.target_temp):
            notify_user("Open the window",
                        "It's more comfortable outside")

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
    NoDampCorners('desktop', 'corner', 3),
    CheckExternalTemperature('desktop', 20, 4097)
]
