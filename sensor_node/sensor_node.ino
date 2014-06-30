/* Sensor Node for Ventilomatic
By: Stephan Sokolow

License: GNU GPL 2.0 or later

Note: You are expected to already have one or both of the following
      libraries installed in your Arduino IDE, depending on the
      hardware you intend to program with this sketch:
- https://github.com/adafruit/DHT-sensor-library
- https://github.com/jcw/ethercard

Hungarian Notation Prefixes:
- AP: Analog Pin
- AV: Analog Value (from analogRead)
- C: Constant (The value is one of several constants like DHT11)
- DP: Digtal Pin
- DV: Digital Value (from digitalRead)
- SP: Status Packet (Serial, UDP, etc.)
- T: Temperature (Celsius)
- H: Humidity (Percent)
*/

/* --== Select how the node will report to the master ==-- */
#define SERIAL 0     // Built-in USB-Serial bridge
#define ETHERNET 1   // WizNet Ethernet Shield

#define MODE SERIAL
//#define MODE ETHERNET

/* --== Configure network communication ==-- */

// These must be different for each node
//const char NODE_ID[] = "corner";
//byte MAC_ADDR[] = { 0xDF, 0x5E, 0x64, 0xD1, 0x8F, 0xBA };
//const char NODE_ID[] = "family_room";
//byte MAC_ADDR[] = { 0xDF, 0x5E, 0x64, 0xD1, 0x8F, 0xBB };
const char NODE_ID[] = "desktop";
byte MAC_ADDR[] = { 0xDF, 0x5E, 0x64, 0xD1, 0x8F, 0xBC };

// This must be the same for all nodes
const byte MASTER_NODE[] = { 192, 168, 0, 2 };
const unsigned short UDP_PORT = 51199;

/* --== Configure the hardware ==-- */

#define AP_LDRPIN 0 // Analog pin
#define DP_ALARMPIN 8

// Temperature sensor configuration
#define DP_DHTPIN 3
#define C_DHTTYPE DHT11
//#define C_DHTTYPE DHT22

/* --== Main Program Starts Here ==-- */

/* -- Code to abstract away communications -- */
// Define Serial writing routines
#if MODE == SERIAL
#define SP_WRITE(x) Serial.print(x)
void sp_begin(char header[]) { SP_WRITE(header); }
void sp_end(char footer[]) { Serial.println(footer); }

// Import WizNet library and define writing routines
#elif MODE == ETHERNET
#include <SPI.h>         // needed for Arduino versions later than 0018
#include <Ethernet.h>
#include <EthernetUdp.h>         // UDP library from: bjoern@cs.stanford.edu 12/30/2008

EthernetUDP udp;
const IPAddress IP_MASTER_NODE(MASTER_NODE[0], MASTER_NODE[1],
                               MASTER_NODE[2], MASTER_NODE[3]);

#define SP_WRITE(x) udp.print(x)
void sp_begin(char header[]) {
  // TODO: Will anything bad happen if I don't do this and the
  //       receive buffer fills up?
  udp.parsePacket();

  udp.beginPacket(IP_MASTER_NODE, UDP_PORT);
  SP_WRITE(header);
}
void sp_end(char footer[]) {
  SP_WRITE(footer);
  SP_WRITE("\n");
  udp.endPacket();
}
#endif

/* -- Code for generating status packets -- */

/** Wrapper for printing all but the first JSON key/value pair
    (floating point values) */
void json_print_if(const char key[], float val) {
  SP_WRITE(", \"");
  SP_WRITE(key);
  SP_WRITE("\": ");
  if (isnan(val)) {
    SP_WRITE("null");
  } else {

    SP_WRITE(val);
  }
}

/** Wrapper for printing all but the first JSON key/value pair
    (string values)

    @bug: This does not escape quotes **/
void json_print_if(const char key[], const char val[]) {
  SP_WRITE(", \"");
  SP_WRITE(key);
  SP_WRITE("\": \"");
  SP_WRITE(val);
  SP_WRITE("\"");
}

/* -- Common code to actually drive the node -- */

#include "DHT.h"
DHT dht(DP_DHTPIN, C_DHTTYPE);

boolean is_alarming = 0;

void setup() {
  pinMode(DP_ALARMPIN, OUTPUT);
  digitalWrite(DP_ALARMPIN, HIGH);

#if MODE == SERIAL
  Serial.begin(9600);
#elif MODE == ETHERNET
  // Make the Ethernet shield reliable without the SD card library
  pinMode(4,  OUTPUT);   // SD select pin             (required)
  digitalWrite(4, HIGH); // Explicitly disable SD     (required)

  while (Ethernet.begin(MAC_ADDR) == 0) {
    // ...if DHCP request failed, wait one minute, then retry
    delay(1000 * 60);
  }

  // Needed even if we don't intend to receive any packets
  udp.begin(UDP_PORT);
#else
#error Unrecognized Communication Mode
#endif
}

void loop() {
  float h_relative = dht.readHumidity();
  float t_ambient = dht.readTemperature();
  float av_light = analogRead(AP_LDRPIN);
  boolean dv_alarmpin = digitalRead(DP_ALARMPIN);
  
  // Calculate a simple approximation of the dewpoint
  // (accurate above 58% humidity) to control the alarm
  // independently of the master control node.
  // Source: https://en.wikipedia.org/wiki/Dewpoint
  float t_dewpoint = t_ambient - ((100 - h_relative) / 5);
  is_alarming = t_ambient < t_dewpoint;
  
  // Use the DHT's read delay as an alarm timing source
  dv_alarmpin = (is_alarming && dv_alarmpin == HIGH) ? LOW : HIGH;
  digitalWrite(DP_ALARMPIN, dv_alarmpin);

  // Output in JSON
  sp_begin("{ \"api_version\": 0");
  json_print_if("node_id", NODE_ID);
  json_print_if("humidity", h_relative);
  json_print_if("temperature", t_ambient);
  json_print_if("dewpoint", t_dewpoint);
  json_print_if("light", av_light);
  sp_end(" }");
}
