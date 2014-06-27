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
__version__ = "0.1"
__license__ = "GNU GPL 2 or later"

SERIAL_INPUTS = ['/dev/ttyUSB0']
CM17A_PORT = '/dev/ttyS0'

import json, serial, subprocess, urwid

inputs = {}
for path in SERIAL_INPUTS:
    fobj = serial.Serial(path, 9600)
    inputs[fobj.fileno()] = fobj

call_x10 = lambda device, state: subprocess.call(['br', '-x', CM17A_PORT,
    "A%d" % device, 'on' if state else 'off'])

class Monitor(object):
    palette = [
        (None, 'light gray', 'black', ''),
    ]

    def __init__(self, ports):
        self.ports = ports
        self.pending_data = {x: '' for x in self.ports}
        self.widgets = {x: urwid.Text('') for x in self.ports}

        row = urwid.Pile(list(('pack', w) for w in self.widgets.values()))
        fill = urwid.Filler(row)

        self.loop = urwid.MainLoop(fill, self.palette,
                unhandled_input=self.exit_on_q)
        for fno in self.ports:
            self.loop.event_loop.watch_file(fno, self.data_ready_cb)

    def data_ready_cb(self):
        for fno, port in self.ports.items():
            while (port.readable() and
                   not '\r\n' in self.pending_data[fno]):
                self.pending_data[fno] += port.read(port.inWaiting())

            while '\r\n' in self.pending_data[fno]:
                raw, self.pending_data[fno] = (
                    self.pending_data[fno].split('\r\n', 1))

                try:
                    data = json.loads(raw)
                except ValueError:
                    print "Packet was not valid JSON: %s" % raw
                    continue

                self.widgets[fno].set_text((None, repr(data)))

    def exit_on_q(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def run(self):
        self.loop.run()

app = Monitor(inputs)
app.run()
