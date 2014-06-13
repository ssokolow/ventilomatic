---
layout: post
title:  "Bill of Materials"
date:   2014-06-13 12:23:35
categories: design hardware
---

OK, let's start with the hardware design.

The system will involve three sensor modules and one central controller module
interconnected by the existing house LAN and some pre-existing X10 home
automation gear.

To keep the designs as simple as possible, all three sensors will share these
characteristics:

* One [DHTxx-family temperature/humidity sensor](https://learn.adafruit.com/dht/overview)
* One [cadmium sulphide photoresistor](https://en.wikipedia.org/wiki/Photoresistor)
* One buzzer for warning of [condensation-inducing](https://en.wikipedia.org/wiki/Dew_point)
  conditions without relying on the complex, failure-prone signalling path
  through the normal LAN-based reporting interface.

However, as this is being prototyped from supplies I already have, I'm going to
need to build three heterogeneous sensors.

**Note:** As I don't regularly assemble these things from memory, this list may
be revised as I actually do the assembly work.

## Sensor #1

This sensor gets first pick of the components, so it gets all the ones that are
easiest to work with and/or least overkill spec-wise.

* 1 x Arduino Uno or compatible ([~$11 CAD](http://www.dx.com/p/development-board-w-data-cable-for-arduino-uno-r3-deep-blue-cable-52cm-312887))
* 1 x Arduino ENC28J60 Ethernet Module ([~$4 CAD](http://www.ebay.ca/sch/i.html?_odkw=arduino+ethernet+shield+W5100+-motor&_ipg=200&_stpos=L0K+1N0&LH_BIN=1&_sop=15&_localstpos=L0K+1N0&_osacat=0&_from=R40&_mPrRngCbx=1&_trksid=p2045573.m570.l1313.TR12.TRC2.A0.H0.Xarduino+ethernet+ENC28J60&_nkw=arduino+ethernet+ENC28J60&_sacat=0))
* 1 x Arduino Prototyping Shield ([~$4 CAD](http://www.ebay.ca/sch/i.html?_odkw=arduino+prototype+shield&_ipg=200&LH_BIN=1&_stpos=L0K+1N0&_sop=15&_localstpos=L0K+1N0&_osacat=0&_from=R40&_mPrRngCbx=1&_trksid=p2045573.m570.l1313.TR6.TRC2.A0.H0.Xarduino+protoshield&_nkw=arduino+protoshield&_sacat=0))
* 1 x DHT11 temperature/humidity sensor ([~$1.50 CAD](http://www.ebay.ca/sch/i.html?_udlo=&LH_BIN=1&_sop=15&clk_rvr_id=524308330579&_sacat=&_mPrRngCbx=1&_udhi=&_nkw=dht11&_ipg=200&rt=nc&_localstpos=L0K%201N0&_stpos=L0K%201N0))
* 1 x CdS photoresistor ([5.5¢ ea.](http://www.ebay.ca/sch/i.html?_odkw=dht11&_ipg=200&_stpos=L0K+1N0&LH_BIN=1&_sop=15&_localstpos=L0K+1N0&_osacat=0&clk_rvr_id=524308330579&_mPrRngCbx=1&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.Xphotoresistor&_nkw=photoresistor&_sacat=0&_from=R40) in a 20-pack)
* 1 x 5V magnetic buzzer ([$1.5 CAD for 5 or $1.75 CAD for 10](http://www.ebay.ca/sch/i.html?_odkw=photoresistor&_ipg=200&LH_BIN=1&_stpos=L0K+1N0&_sop=15&_localstpos=L0K+1N0&_osacat=0&_from=R40&_mPrRngCbx=1&_trksid=p2045573.m570.l1313.TR10.TRC0.A0.H0.X5v+buzzer&_nkw=5v+buzzer&_sacat=0))
* 1 x breadboard hookup wire kit ([~$3.50 CAD](http://www.ebay.ca/sch/i.html?_odkw=breadboard+wire+kit+-65+-65pcs+-20cm&_sop=15&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.XU+shape+breadboard+wire+kit&_nkw=U+shape+breadboard+wire+kit&_sacat=0) shared across the whole project)
* 1 x Ethernet patch cable

...plus standoffs to keep it from electrically contacting the floor since this
is the sensor which will be used where condensation is a concern.

(Specifically, three 10mm hexagonal female-female standoffs to act as legs and
one stacked pair of shorter male-female standoffs and a twist-tie for the
remaining mounting hole since I lack a machine screw with a head small enough
to fit nicely next to the SCL header on the Arduino revision 3 layout.)

## Sensor #2

This sensor gets the remaining network-capable components.

* 1 x Freaduino Leonardo or compatible ([~$13 CAD](http://www.dx.com/p/diy-eduino-leonardo-module-blue-black-213956))
* 1 x Arduino Ethernet Shield ([~$9 CAD](http://www.ebay.ca/sch/i.html?_odkw=arduino+ethernet+W5100&_ipg=200&LH_BIN=1&_stpos=L0K+1N0&_sop=15&_localstpos=L0K+1N0&_osacat=0&_from=R40&clk_rvr_id=524308330579&_mPrRngCbx=1&_trksid=p2045573.m570.l1313.TR4.TRC2.A0.H0.Xarduino+ethernet+shield+W5100+-motor&_nkw=arduino+ethernet+shield+W5100+-motor&_sacat=0))
* 1 x Arduino Prototyping Shield ([~$4 CAD](http://www.ebay.ca/sch/i.html?_odkw=arduino+prototype+shield&_ipg=200&LH_BIN=1&_stpos=L0K+1N0&_sop=15&_localstpos=L0K+1N0&_osacat=0&_from=R40&_mPrRngCbx=1&_trksid=p2045573.m570.l1313.TR6.TRC2.A0.H0.Xarduino+protoshield&_nkw=arduino+protoshield&_sacat=0))
* 1 x Set of stacking headers (to allow the Protoshield to clear the RJ45
  connector, [~$3 CAD](http://www.ebay.ca/sch/i.html?_odkw=stackable+headers&_ipg=200&_stpos=L0K+1N0&LH_BIN=1&_sop=15&_localstpos=L0K+1N0&_osacat=0&_from=R40&_mPrRngCbx=1&_trksid=p2045573.m570.l1313.TR6.TRC2.A0.H0.Xstackable+header+%28set%2Ckit%29&_nkw=stackable+header+%28set%2Ckit%29&_sacat=0) if not bought in volume)
* 1 x DHT11 temperature/humidity sensor ([~$1.50 CAD](http://www.ebay.ca/sch/i.html?_udlo=&LH_BIN=1&_sop=15&clk_rvr_id=524308330579&_sacat=&_mPrRngCbx=1&_udhi=&_nkw=dht11&_ipg=200&rt=nc&_localstpos=L0K%201N0&_stpos=L0K%201N0))
* 1 x CdS photoresistor ([5.5¢ ea.](http://www.ebay.ca/sch/i.html?_odkw=dht11&_ipg=200&_stpos=L0K+1N0&LH_BIN=1&_sop=15&_localstpos=L0K+1N0&_osacat=0&clk_rvr_id=524308330579&_mPrRngCbx=1&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.Xphotoresistor&_nkw=photoresistor&_sacat=0&_from=R40) in a 20-pack)
* 1 x 5V magnetic buzzer ([$1.5 CAD for 5 or $1.75 CAD for 10](http://www.ebay.ca/sch/i.html?_odkw=photoresistor&_ipg=200&LH_BIN=1&_stpos=L0K+1N0&_sop=15&_localstpos=L0K+1N0&_osacat=0&_from=R40&_mPrRngCbx=1&_trksid=p2045573.m570.l1313.TR10.TRC0.A0.H0.X5v+buzzer&_nkw=5v+buzzer&_sacat=0))
* 1 x breadboard hookup wire kit ([~$3.50 CAD](http://www.ebay.ca/sch/i.html?_odkw=breadboard+wire+kit+-65+-65pcs+-20cm&_sop=15&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.XU+shape+breadboard+wire+kit&_nkw=U+shape+breadboard+wire+kit&_sacat=0) shared across the whole project)
* 1 x Ethernet patch cable

No standoffs are necessary for this sensor since it will be resting on an
unfinished wooden surface.

## Sensor #3

With no network adaptor modules left, this sensor connects to the central
controller directly via the USB serial interface. Also, having run out of DHT11
sensors, this one uses a more precise but more expensive DHT22 instead.

* 1 x SparkFun Redboard or compatible ([~$11 CAD](http://www.dx.com/p/development-board-w-data-cable-for-arduino-uno-r3-deep-blue-cable-52cm-312887))
* 1 x Breadboard
* 1 x DHT22 temperature/humidity sensor
* 1 x CdS photoresistor ([5.5¢ ea.](http://www.ebay.ca/sch/i.html?_odkw=dht11&_ipg=200&_stpos=L0K+1N0&LH_BIN=1&_sop=15&_localstpos=L0K+1N0&_osacat=0&clk_rvr_id=524308330579&_mPrRngCbx=1&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.Xphotoresistor&_nkw=photoresistor&_sacat=0&_from=R40) in a 20-pack)
* 1 x 5V magnetic buzzer ([$1.5 CAD for 5 or $1.75 CAD for 10](http://www.ebay.ca/sch/i.html?_odkw=photoresistor&_ipg=200&LH_BIN=1&_stpos=L0K+1N0&_sop=15&_localstpos=L0K+1N0&_osacat=0&_from=R40&_mPrRngCbx=1&_trksid=p2045573.m570.l1313.TR10.TRC0.A0.H0.X5v+buzzer&_nkw=5v+buzzer&_sacat=0))
* 1 x breadboard hookup wire kit ([~$3.50 CAD](http://www.ebay.ca/sch/i.html?_odkw=breadboard+wire+kit+-65+-65pcs+-20cm&_sop=15&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.XU+shape+breadboard+wire+kit&_nkw=U+shape+breadboard+wire+kit&_sacat=0) shared across the whole project)
* 1 x Short USB A-to-MiniB cable

No standoffs are necessary for this sensor since it will be resting on an
unfinished wooden surface.

## Central Controller

* 1 x Raspberry Pi
* 1 x 5V 1A USB Micro cellphone charger
* 1 x SD Card
* 1 x [CM19A](http://www.thehomeautomationstore.com/cm19a.html) USB X10 transceiver
* 1 x Ethernet patch cable

**Note:** Depending on how this project turns out, I may end up either using a
[CM17A](http://www.ebay.ca/sch/i.html?_odkw=CM19A&_ipg=200&_stpos=L0K+1N0&LH_BIN=1&_sop=15&_localstpos=L0K+1N0&_osacat=0&clk_rvr_id=524308330579&_mPrRngCbx=1&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.XCM17A&_nkw=CM17A&_sacat=0&_from=R40) with a USB-Serial adapter or just using my planned network-transparent architecture to
pipe X10 control commands to my desktop PC which already has an X10 transceiver connected.

After all, I'll probably be running a system node on my desktop anyway to log its
internal thermal sensors and the CM17A is easier to work with on the software
side... it's just unpredictable whether a given cheap Chinese USB-Serial cable
will get along with it.
