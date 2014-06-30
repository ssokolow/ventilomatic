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
- T: Temperature (Celsius)
- H: Humidity (Percent)
*/

#include "DHT.h"

#define AP_LDRPIN 0 // Analog pin
#define DP_ALARMPIN 8

// Temperature sensor configuration
#define DP_DHTPIN 3
#define C_DHTTYPE DHT11
//#define C_DHTTYPE DHT22

DHT dht(DP_DHTPIN, C_DHTTYPE);

// -- For now, build on code from AdaFruit's DHTtester sketch to
//    make sure I've wired everything correctly.

boolean is_alarming = 0;

void setup() {
  pinMode(DP_ALARMPIN, OUTPUT);
  digitalWrite(DP_ALARMPIN, HIGH);

  Serial.begin(9600);
}

/** Wrapper for printing all but the first JSON key/value pair */
void json_print_if(char key[], float val) {
  Serial.print(", \"");
  Serial.print(key);
  Serial.print("\": ");
  if (isnan(val)) {
    Serial.print("null");
  } else {
    Serial.print(val);
  }
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
  Serial.print("{ \"api_version\": 0");
  json_print_if("humidity", h_relative);
  json_print_if("temperature", t_ambient);
  json_print_if("dewpoint", t_dewpoint);
  json_print_if("light", av_light);
  Serial.println(" }");
}
