---
layout: post
title:  "Done (For Now)"
date:   2014-06-30 03:45:00
categories: status
---

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
