#include "DHT.h"
#define DHTTYPE DHT11
#define DHTPIN 3
DHT dht(DHTPIN, DHTTYPE);

#define TRIGPIN 4
#define ECHOPIN 5

#define BUZPIN 6

long duration;
int distance;
float h, t;

int failed = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(BUZPIN, OUTPUT);
  pinMode(TRIGPIN, OUTPUT);
  pinMode(ECHOPIN, INPUT);
  Serial.begin(9600);
  dht.begin();
}

void buzz() {
  tone(BUZPIN, 1000);
  delay(1000);
  noTone(BUZPIN);
  delay(1000);
}

void getDist() {
  digitalWrite(TRIGPIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGPIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGPIN, LOW);
  duration = pulseIn(ECHOPIN, HIGH);
  distance = duration * 0.034 / 2;
}

void getHumTemp(){
  h = dht.readHumidity();
  t = dht.readTemperature();
  if (isnan(h) || isnan(t)) {
    Serial.println("failed");
    return;
  }
}

void sendJSON() {
  Serial.println("{");
  Serial.print("\t\"distance\": ");
  Serial.print(distance);
  Serial.println(",");
  Serial.print("\t\"hum\": ");
  Serial.print(h);
  Serial.println(",");
  Serial.print("\t\"temp\": ");
  Serial.println(t);
  Serial.println("}");
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(500);
  getDist();
  getHumTemp();
  sendJSON();
  if (h > 80 || t > 32 || distance < 10) {
    buzz();
  }
}
