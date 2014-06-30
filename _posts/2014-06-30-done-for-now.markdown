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

However, given my goals, the obstacles I faced, and the time I had, I think I did pretty well for a first sprint. Here is an overview of the status of the ["end result" goals]({{ site.baseurl }}{% post_url 2014-06-11-initial-concept %}) as of my course's contract date:

### Controller Goal #1: DONE
*Turn the lights off when the sunlight becomes bright enough to
   provide equivalent illumination.*

I don't have time to properly calibrate it before my contract date, but the light sensor on the `corner` node (the one on an extension and taped to the window) will currently trigger a shut-down of all three X10-controllable lights in the room when it detects a high enough reading.

All I have to do is open the window, reach out with my high-intensity LED flashlight, and `*CLACK* ... *CLACK* ... *CLACK*`, all of the X10-controllable lights in the room turn off.

