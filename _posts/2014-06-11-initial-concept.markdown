---
layout: post
title:  "Initial Plans"
date:   2014-06-11 05:43:31
categories: design
---

Well, let's get this project started. This has two purposes:

1. First, it's my course project for [COMP444: Embedded/Robotic Programming](http://www.athabascau.ca/syllabi/comp/comp444.php).

2. More satisfyingly, it's also a chance to prototype a mixture of two
or three ideas that have been rattling around my head and notebook for a while
now.

   Basically, a mixture of an analytics system and pseudo-HVAC controller for
   the temperature, humidity, and light levels in my bedroom.

As I don't yet have the skills to truly produce the design I consider suitable
for permanent installation, this will still have a ways to go, but it should
replicate the function, if not the form, that I desire.

For records purposes, here is the napkin outline I'll be starting from as a
direct quote from the e-mail in which I sent it:

```
1.1. Connect my Arduino Uno, Ethernet Shield, a CdS photoresistor, and
     a "wall wart" power brick.
1.2. Write a simple sketch which allows the sensor to be queried via
     the LAN.
1.3. Attach the photoresistor to the window.

2.1. Connect my Arduino Leonardo, Ethernet Module, a DHT11
     temperature/humidity sensor, and a "wall wart" power brick.
2.2. Again, simple sketch to allow LAN query
2.3. Place the temperature sensor in the family room

3.1. Plug a USB X10 transmitter and Arduino Nano into my Raspberry Pi
3.2. Connect a CdS cell and DHT11 to the Arduino
3.3. Screw my (ugly scrap) alarm system door sensor onto my door frame
     and connect it to the Arduino Nano.
3.3. Write a simple sketch which sends reports to the Raspberry Pi via
     USB serial
3.4. Place the assembly on my desk where it can get a decent
     "baseline room average" reading

4.1. Write a cronjob on the Pi to retrieve sunrise and sunset times and
     exterior temperature and humidity from Yahoo! Weather.
4.2. Write some Python code on the Pi to query and collate all of the
     sensor and Yahoo! weather data and use it for both rrdtool graphs
     and a simple automated light and air quality controller.

Controller goals:
1. Turn the lights off when the sunlight becomes bright enough to
   provide equivalent illumination.
2. Turn the [two independently controlled] fans on and off to control
   humidity in the corner and to exhaust hot summer air into the rest
   of the basement to maintain temperature.
3. If the door is closed, notify the user to open it when air
   circulation is necessary.
4. If the weather forecast says the outdoor air should be a more
   desirable temperature/humidity than the air in the family room,
   notify the user to open the window.
5. If the computer is still in use when the room lighting drops below
   a specified level, turn on a suitable bias light.

(My X10 system already allows me manual control over three light sources,
two fans, a door chime, and an X10 universal module (remote 30V DC relay
and/or sounder, continuous or momentary) which I have yet to find a use for.)

Stretch Goals:
5.1. Write a tool on my desktop PC which feeds in the screensaver
     subsystem's idleness data for information about
     user presence and activity to inform decision-making.
5.2. Extend the tool to listen to output from the "motion" utility
     to detect user presence when away from keyboard via the webcam.
```
