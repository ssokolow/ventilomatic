#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""Ventilomatic Control Node Program
--snip--

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

import json, serial, select, socket, time
import logging, pprint
log = logging.getLogger(__name__)

from rules import RULES

__appname__ = "Ventilomatic Control Node"
__author__ = "Stephan Sokolow (deitarion/SSokolow)"
__version__ = "0.2"
__license__ = "GNU GPL 2 or later"

SERIAL_INPUTS = ['/dev/ttyUSB0']
UDP_ADDR = ('0.0.0.0', 51199)
WARMUP_TIME = 3

inputs = []
for path in SERIAL_INPUTS:
    fobj = serial.Serial(path, 9600)
    inputs.append(fobj)

if UDP_ADDR:
    # TODO: Decide how best to handle IPv6
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(UDP_ADDR)
    inputs.append(sock)

class Monitor(object):
    """Application for keeping track of sensor state."""

    def __init__(self, inputs):
        """
        :inputs: A list of `select()`able objects.
        """
        self._inputs = inputs
        self._buffers = {}
        self._model = {}
        self.last_rule_eval = None

    def defragment_input(self, handle):
        """Given a readable socket, move data to the accumulation buffers.

        :handle: A readable object as returned by select()
        """
        fno = handle.fileno()
        if hasattr(handle, 'readable') and hasattr(handle, 'inWaiting'):
            key = fno
            self._buffers.setdefault(key, '')
            self._buffers[fno] += handle.read(handle.inWaiting())
        elif hasattr(handle, 'recvfrom'):
            data, addr = handle.recvfrom(1024)
            key = (fno, addr)
            self._buffers.setdefault(key, '')
            self._buffers[key] += data
        else:
            log.error("Unknown type of data source encountered!")

    def parse_buffers(self):
        """Extract any complete messages from the accumulation buffers and
        parse them."""

        messages = []
        for key in self._buffers:
            while '\n' in self._buffers[key]:
                raw, self._buffers[key] = self._buffers[key].replace('\r',
                                                         '').split('\n', 1)
                if not raw:
                    continue

                try:
                    data = json.loads(raw)
                except ValueError:
                    log.debug("Packet was not valid JSON: %r", raw)
                    continue

                api_version = data.get('api_version', None)
                if not api_version == 0:
                    log.error('Packet had unsupported API version \"%s\": %s',
                              api_version, data)

                log.debug(data)
                messages.append(data)
        return messages

    def update_model(self, message):
        """Update our model of the world"""
        node_id = message.get('node_id', None)
        if not node_id:
            log.error("Message has no node ID: %s" % message)
            return

        #XXX: On which layer should further format validation happen?
        self._model[node_id] = message

    def loop_iteration(self):
        """Perform one iteration of the main loop"""
        # Give data time to come in before letting rules complain
        if self.last_rule_eval is None:
            self.last_rule_eval = time.time() + WARMUP_TIME

        readable, _, errored = select.select(self._inputs, [], self._inputs)
        for sck in readable:
            self.defragment_input(sck)

        for message in self.parse_buffers():
            self.update_model(message)

        # Only run rules once per second at most
        if (time.time() - self.last_rule_eval) > 1:
            for rule in RULES:
                rule(self._model)

    def run(self):
        while self._inputs:
            self.loop_iteration()

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(version="%%prog v%s" % __version__,
            usage="%prog [options] <argument> ...",
            description=__doc__.replace('\r\n', '\n').split('\n--snip--\n')[0])
    parser.add_option('-v', '--verbose', action="count", dest="verbose",
        default=2, help="Increase the verbosity. Use twice for extra effect")
    parser.add_option('-q', '--quiet', action="count", dest="quiet",
        default=0, help="Decrease the verbosity. Use twice for extra effect")
    # Reminder: %default can be used in help strings.

    # Allow pre-formatted descriptions
    parser.formatter.format_description = lambda description: description

    opts, args = parser.parse_args()

    # Set up clean logging to stderr
    log_levels = [logging.CRITICAL, logging.ERROR, logging.WARNING,
                  logging.INFO, logging.DEBUG]
    opts.verbose = min(opts.verbose - opts.quiet, len(log_levels) - 1)
    opts.verbose = max(opts.verbose, 0)
    logging.basicConfig(level=log_levels[opts.verbose],
                        format='%(levelname)s: %(message)s')

    app = Monitor(inputs)
    app.run()
