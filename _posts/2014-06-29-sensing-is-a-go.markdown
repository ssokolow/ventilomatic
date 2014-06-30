---
layout: post
title:  "Sensing Is A Go"
date:   2014-06-29 23:38:00
categories: design hardware software
---

Well, a lack of time has necessitated some corner-cutting, but basic network support is now working. I've got two sensors (one serial and one ethernet) and a basic `main.py` which listens to them.

```python
{u'temperature': 27.4, u'dewpoint': 19.02, u'light': 289.0, u'humidity': 58.1, u'node_id': u'desktop', u'api_version': 0}
{u'temperature': 29.0, u'dewpoint': 20.6, u'light': 274.0, u'humidity': 58.0, u'node_id': u'corner', u'api_version': 0}
{u'temperature': 27.4, u'dewpoint': 19.02, u'light': 273.0, u'humidity': 58.1, u'node_id': u'desktop', u'api_version': 0}
{u'temperature': 29.0, u'dewpoint': 20.6, u'light': 286.0, u'humidity': 58.0, u'node_id': u'corner', u'api_version': 0}
{u'temperature': 27.4, u'dewpoint': 19.02, u'light': 284.0, u'humidity': 58.1, u'node_id': u'desktop', u'api_version': 0}
{u'temperature': 29.0, u'dewpoint': 20.6, u'light': 289.0, u'humidity': 58.0, u'node_id': u'corner', u'api_version': 0}

```

(Eagle-eyed readers may notice that's not valid JSON. It's Python `repr()` debugging output which indicates that `main.py` successfully received, defragmented, and parsed valid JSON, then confirmed the correct value for the `api_version` field.)

### Caveats

At the moment, the sensors still have a single point of failure in that their communication is a blocking operation, so a dead serial or network link will prevent the internal alarm from going off. I doubt I'll have time to fix that before my course contract date so the dewpoint alarm will have to be purely for alerting when the network or serial link is up but there's a failure between `main.py` and whatever notification GUI I've configured.

I'm still having trouble with the third sensor (the one using the cheap ENC28J60-based network module) but that could be a driver issue since it's failing on the DHCP request. 

### From Here...

Aside from trying the ENC28J60 module with hard-coded IP settings, I don't expect I'll be doing any more work in the Arduino IDE before my contract date.

Given that my hardware is very heterogeneous, I never had time to set up EEPROM storage of the MAC address and node ID, and I don't know how to use Makefiles with Arduino, I specifically designed this project so that I could get the nodes programmed and the IDE closed as soon as possible. Making sure I've flashed each Arduino with the right config constants is just too much hassle to keep doing.

That means that, aside from getting that last node configured, everything else before the contract date will either be master node coding or simple hardware adjustments (like pulling the Light-Dependent Resistor from the corner sensor and sticking it on the end of a length of twisted pair wire so I can tape it to the window.