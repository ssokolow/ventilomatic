---
layout: post
title:  "Done (For Now)"
date:   2014-06-30 03:45:00
categories: status
---
I have some stuff to finish up in another course, so I seriously doubt I'll be able to work on this any more before the end of today. As such, this is the final state the project will take before my course deadline.

# Results

Given the time-crunch, I definitely had to make some compromises. (For example, I'm currently running the control node on my desktop PC because it already has the CM17A set up for sending X10 messages but I used that as a blocking operation. While fast reactions may not be essential in this application, I'll still want to switch to an asynchronous design if for no other reason than making absolutely sure it's impossible for the UDP receive buffers to overflow and start losing measurements I want to log and graph.)

I also noticed that the voltage regulator on my Arduino Uno is dissipating a lot more heat than would seem reasonable when powered by [my 9V supply]({{ site.baseurl }}/img/parts/psu_2.jpg) so that's something else I'll have to investigate before producing versions for permanent installation.


### Controller Goal #1: DONE
*Turn the lights off when the sunlight becomes bright enough to
   provide equivalent illumination.*

I don't have time to properly calibrate it before my contract date, but the light sensor on the `corner` node (the one on an extension and taped to the window) will currently trigger a shut-down of all three X10-controllable lights in the room when it detects a high enough reading.

All I have to do is open the window, reach out with my high-intensity LED flashlight, and `*CLACK* ... *CLACK* ... *CLACK*`, all of the X10-controllable lights in the room turn off.

### Controller Goal #2: PARTIAL
*Turn the [two independently controlled] fans on and off to control humidity in the corner and to exhaust hot summer air into the rest of the basement to maintain temperature.*

I've implemented the rule for dealing with humidity in the corner, but the temperature part requires a sensor outside my room and I didn't have time to get the EtherCard stuff written and debugged.

### Controller Goal #3: FOILED
*If the door is closed, notify the user to open it when circulation is necessary.*

I looked everywhere and can't figure out where I stashed my magnetic reed switch. I've ordered a new five-pack, but they won't be here before my contract date. However, I *can* write master controller code for when the hardware *does* get added to one of the sensor nodes and I can write it in such a way that it assumed a missing sensor means "door closed" so it'll always ask me.

### Controller Goal #4: DONE
*If the weather forecast says the outdoor air should be a more desirable temperature/humidity than the air in the family room, notify the user to open the window.*

The system queries Yahoo! Weather once an hour to get the outside temperature and, if the desired temperature is closer to that than the indoor air temperature, it uses `notify-send` to suggest opening a window.

### Controller Goal #5: MISSED
*If the computer is still in use when the room lighting drops below a specified level, turn on a suitable bias light.*

I ran out of time before I could write the daemon to feed readings from the screensaver's idleness API into the system. As such, it has no way to detect "If the computer is still in use when..."

I'll try to make time to write this within the first week of July.
