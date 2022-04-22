#include "DHT.h"
#include <SoftwareSeial.h>

#define DHTtype DHT22

#define DHTpin 1
#define RXpin 2
#define TXpin 3
#define ECHOpin 5
#define TRIGpin 6

float temp;
float hum;

long duration;
int distance;

DHT dht(DHTpin, DHTtype);

SoftwareSerial esp8266(2, 3);

void setup() {
  // setting up the ultrasonic sensor
  pinMode(TRIGpin, OUTPUT); // It sets the ECHO pin as OUTPUT  
  pinMode(ECHOpin, INPUT); // It sets the TRIG pin as INPUT  
  Serial.begin(9600); // Serial Communication at the rate of 9600 bps
  Serial.println("The Ultrasonic sensor is live");

  // setting up the humidity and temperature sensor
  dht.begin();
  Serial.println("The Humidity and Temperature sensor is live");
  
  // setting up the wifi module
  esp8266.begin(9600);
}

void readDht()  {
  do {
    delay(2000);
    hum = dht.readHumidity();
    temp = dht.readTemperature(true);
  } while (isnan(hum) || isnan(temp));
  Serial.print("Temperature: ");
  Serial.println(temp);
  Serial.print("Humidity: ");
  Serial.println(hum);
  
}

void readDist() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distanceCm = duration * 0.034 / 2;
  distanceInch = duration * 0.0133 / 2;
  lcd.setCursor(0, 0);
  lcd.print("Distance: "); 
  lcd.print(distanceCm);
  lcd.print(" cm");
  delay(10);
}

void sendWifiData() {
  // still need to implement
}

void loop() {
  delay(60000 * 12) { // every 12 hours
      readDht();
      readDist();
      sendWifiData();
    }
}