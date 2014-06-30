---
layout: post
title:  "Tentative Architecture"
date:   2014-06-15 08:24:42
categories: design software
---

Here is my first draft for how information will flow in the system's network-transparent design.
(I'll fix the bad kerning once I have a build scripting system in place to make
use of the more complicated commands needed.)

**Update:** At present, due to time constraints, I've had to go for **push-based design** with raw **newline-terminated JSON packets over UDP**. I still hope to switch to a pull-based HTTP design in the future.

![Graph Diagram]({{ site.baseurl }}/design_docs/network_architecture.dot.png)
[[source]({{ site.baseurl}}/design_docs/network_architecture.dot)]

I'm not yet 100% certain that I will use HTTP as the transport for the sensors instead
of UDP but, as the Pythonistas say, premature optimization is the root of all
evil and I definitely want to have JSON-over-HTTP as an option for receiving
sensor data from full-fledged Linux devices.
