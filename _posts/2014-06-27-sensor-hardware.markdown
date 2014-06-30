---
layout: post
title:  "Sensor Hardware"
date:   2014-06-27 01:20:00
categories: design hardware
---

Sorry for the wait (life got **very** distracting and stressful), but here we are. The sensor nodes are done and the Fritzing schematic is in the repository.

**Update:** Incomplete documentation led me to incorrectly believe Pin 10 was free when using the Arduino Ethernet shield. I've relocated the buzzer to pin 8 and updated both the photos and Fritzing files. The originals are available via the git history.

Here are the three different prototype sensor designs:

![Arduino Uno + Ethernet Shield]({{ site.baseurl }}img/assembled/uno_node.jpg)
![Arduino Leonardo + EtherCard]({{ site.baseurl }}img/assembled/leonardo_node.jpg)
![Sparkfun RedBoard]({{ site.baseurl }}img/assembled/redboard_node.jpg)

They all look quite different but, aside from the method of communication (Ethernet shield, EtherCard, and USB serial), they all follow this exact same schematic (Fritzing source files available in the repository, though the non-Breadboard views are a bit of a mess because the DHT22 part for Fritzing is a bit broken):

![Fritzing Breadboard View]({{ site.baseurl }}img/assembled/sensor_node_bb.png)

Sorry about how messy it is. I'm too short on time to find a better way to populate the breadboard and that's the most useful of several ugly options for laying out the Fritzing render.

I haven't yet written the network code, but the draft code for version 1 of the serial interaction model is done (and streams line-by-line JSON in this format):

```json
{ "api_version": 0, "humidity": 56.20, "temperature": 25.10, "dewpoint": 16.34, "light": 295.00 }
```

Two tips for working on this sort of project:

1. Work with familiar hardware. I don't know what it was, but the Redboard was giving me trouble at first and it was a lot easier to iron out the design and code on my old reliable Arduino Uno (the tallest node pictured), then assemble the design on the Redboard once I was sure that any issues wouldn't be software bugs.
2. Make sure you remember to unplug any other Arduinos before programming. My Uno uses a USB A-B cable while my Leonardo and Redboard use USB A-MiniB and, for a few minutes, I was very frustrated when the serial monitor output wasn't showing changes I'd made to how the board was wired up. Turns out, I was monitoring the wrong Arduino.
