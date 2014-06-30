"""Resources used in declaring Ventilomatic rules."""

__author__ = "Stephan Sokolow (deitarion/SSokolow)"
__license__ = "GNU GPL 2 or later"

CM17A_PORT = '/dev/ttyS0'

import subprocess

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
