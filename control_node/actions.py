"""Resources used in declaring Ventilomatic rules."""

__author__ = "Stephan Sokolow (deitarion/SSokolow)"
__license__ = "GNU GPL 2 or later"

CM17A_PORT = '/dev/ttyS0'

import subprocess

def call_x10(device, state, house_code='A'):
    """API abstraction wrapper for sending X10 commands

    @param device: An X10 device code from 1 to 16
    @param state: The target state for the device

    @type device: C{int}
    @type state: C{bool}
    """
    subprocess.call(['br', '-x', CM17A_PORT, "%s%d" % (house_code, device),
                     'on' if state else 'off'])
