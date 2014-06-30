#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Ventilomatic Control Node Program

Requires:
- PySerial

Copyright (C) 2014 Stephan Sokolow

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.
"""

__appname__ = "Ventilomatic Control Node"
__author__ = "Stephan Sokolow (deitarion/SSokolow)"
__version__ = "0.2"
__license__ = "GNU GPL 2 or later"

SERIAL_INPUTS = ['/dev/ttyUSB0']
UDP_ADDR = ('0.0.0.0', 51199)
CM17A_PORT = '/dev/ttyS0'

import json, serial, select, socket, subprocess

inputs, buffers = [], {}
for path in SERIAL_INPUTS:
    fobj = serial.Serial(path, 9600)
    inputs.append(fobj)

if UDP_ADDR:
    # TODO: Decide how best to handle IPv6
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(UDP_ADDR)
    inputs.append(sock)

def call_x10(device, state):
    """API abstraction wrapper for sending X10 commands

    @param device: An X10 device code from 1 to 16
    @param state: The target state for the device

    @type device: C{int}
    @type state: C{bool}
    """
    subprocess.call(['br', '-x', CM17A_PORT, "A%d" % device,
                     'on' if state else 'off'])

while inputs:
    readable, _, errored = select.select(inputs, [], inputs)
    for sck in readable:
        fno = sck.fileno()
        if hasattr(sck, 'readable') and hasattr(sck, 'inWaiting'):
            key = fno
            buffers.setdefault(key, '')
            buffers[fno] += sck.read(sck.inWaiting())
        elif hasattr(sck, 'recvfrom'):
            data, addr = sck.recvfrom(1024)
            key = (fno, addr)
            buffers.setdefault(key, '')
            buffers[key] += data
        else:
            print "ERROR: Unknown type of data source encountered!"

    for key in buffers:
        while '\n' in buffers[key]:
            raw, buffers[key] = (buffers[key].replace('\r', '').split('\n', 1))
            if not raw:
                continue

            try:
                data = json.loads(raw)
            except ValueError:
                print "Packet was not valid JSON: %r" % raw
                continue

            api_version = data.get('api_version', None)
            if not api_version == 0:
                print 'Packet had unsupported API version \"%s\": %s' % (
                    api_version, data)

            print repr(data)
