"""Resources used in declaring Ventilomatic rules."""

__author__ = "Stephan Sokolow (deitarion/SSokolow)"
__license__ = "GNU GPL 2 or later"

CM17A_PORT = '/dev/ttyS0'

import datetime, subprocess
import weatherpy

weather_cache = None

def call_x10(device, state, house_code='A', noisy=True):
    """API abstraction wrapper for sending X10 commands

    :device: An X10 device code from 1 through 16
    :state: The target state for the device
    :house_code: An X10 house code from A through P
    :noisy: Send each command twice to compensate for RF or line noise

    @type device: C{int}
    @type state: C{bool}
    """
    if not isinstance(device, (tuple, list, set)):
        device = [device]

    for dev in device:
        subprocess.call(['br', '-x', CM17A_PORT,
                         '-r', str(1 + noisy),
                         "%s%d" % (house_code, dev),
                         'on' if state else 'off'])

def get_yahoo_weather(woeid, cache_duration=60):
    global weather_cache
    if weather_cache and ((
        datetime.datetime.now() - weather_cache.condition.date
    ).seconds / 60.0) < cache_duration:
        return weather_cache

    weather_cache = weatherpy.Response(
        'Ventilomatic +http://ssokolow.com/ventilomatic/', woeid)
    return weather_cache

def notify_user(title, body):
    subprocess.call(['notify-send', title, body])
