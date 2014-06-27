/*

Hungarian Notation Prefixes:
- DP: Digtal Pin
- C: Constant (The value is one of several constants like DHT11)

*/

#include "DHT.h"

// Temperature sensor configuration
#define DP_DHTPIN 3
#define C_DHTTYPE DHT11
//#define C_DHTTYPE DHT22
DHT dht(DP_DHTPIN, C_DHTTYPE);

// -- For now, build on code from AdaFruit's DHTtester sketch to
//    make sure I've wired everything correctly.
void setup() {

  Serial.begin(9600);
  Serial.println("Connection established");
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  
  if (isnan(t) || isnan(h)) {
    Serial.println("Failed to read from DHT");
  } else {
    Serial.print("Humidity: "); 
    Serial.print(h);
    Serial.print(" %\t");
    Serial.print("Temperature: "); 
    Serial.print(t);
    Serial.println(" *C %\t");
  }
}
