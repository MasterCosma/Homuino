#include <CapacitiveSensor.h>

/

int threshold = 50;      // Capacitive action threshold
int count = 0;      // Counts to 500 for swipes
long previousMillis = 0;

CapacitiveSensor   cs_4_2 = CapacitiveSensor(4, 2);       // 22K resistor between pins 4 & 2, pin 2 is sensor pin, add a wire and or foil
CapacitiveSensor   cs_4_6 = CapacitiveSensor(4, 6);       // 22K resistor between pins 4 & 6, pin 6 is sensor pin, add a wire and or foil

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  long start = millis();
  long total1 =  cs_4_2.capacitiveSensor(30);
  long total2 =  cs_4_6.capacitiveSensor(30);

  if (total1 > threshold) {
    previousMillis = millis();
    count = millis() - previousMillis;
    while (count < 500) {
      count = millis() - previousMillis;
      long total2 =  cs_4_6.capacitiveSensor(30);
      if (total2 > threshold) {
        if (count < 100) Serial.println("Click"); else Serial.println("Swipe1");
        delay(1000);
        break;
      }
    }
  }
  
  if (total2 > threshold) {
    previousMillis = millis();
    count = millis() - previousMillis;
    while (count < 500) {
      count = millis() - previousMillis;
      long total1 =  cs_4_2.capacitiveSensor(30);
      if (total1 > threshold) {
        if (count > 100) Serial.println("Swipe2");
        delay(1000);
        break;
      }
    }
  }
}
