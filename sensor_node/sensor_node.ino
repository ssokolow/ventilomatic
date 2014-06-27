/*

Hungarian Notation Prefixes:
- AP: Analog Pin
- AV: Analog Value (from analogRead)
- DP: Digtal Pin
- DV: Digital Value (from digitalRead)
- C: Constant (The value is one of several constants like DHT11)

*/

#include "DHT.h"

#define AP_LDRPIN 0 // Analog pin
#define DP_ALARMPIN 11

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
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float av_l = analogRead(AP_LDRPIN);
  boolean dv_a = digitalRead(DP_ALARMPIN);
  
  // Calculate a simple approximation of the dewpoint
  // (accurate above 58% humidity) to control the alarm
  // independently of the master control node.
  // Source: https://en.wikipedia.org/wiki/Dewpoint
  float t_dp = t - ((100 - h) / 5);
  is_alarming = t < t_dp;
  
  // Use the DHT's read delay as an alarm timing source
  dv_a = (is_alarming && dv_a == HIGH) ? LOW : HIGH;
  digitalWrite(DP_ALARMPIN, dv_a);

  // Output in JSON
  Serial.print("{ \"api_version\": 0");
  json_print_if("humidity", h);
  json_print_if("temperature", t);
  json_print_if("dewpoint", t_dp);
  json_print_if("light", av_l);
  Serial.println(" }");
}
