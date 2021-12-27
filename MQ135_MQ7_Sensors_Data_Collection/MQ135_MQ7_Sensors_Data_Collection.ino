#include "DHT.h"
#define DHTPIN 3
#define DHTTYPE DHT11 
int sensorPin = A0;    // select the input pin for the sensor
int sensorPin1 = A1;    // select the input pin for the sensor
int sensorValue = 0;  // variable to store the value coming from the sensor
int sensorValue1 = 0;  // variable to store the value coming from the sensor
int pin = 7;
int mq7Power = 4;
int mq135Power = 5;
int pmPower = 6;
String values;
unsigned long duration;
unsigned long starttime;
unsigned long sampletime_ms = 2000;//sampe 30s&nbsp;;
unsigned long lowpulseoccupancy = 0;
float ratio = 0;
float pmValue = 0;

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200); // sets the serial port to 115200
  pinMode(pin, INPUT);
  dht.begin();  
  starttime = millis();//get the current time;
  delay(60000); // Delay for 1 min to heatup the sensors
}

void loop() {
  // read the value from the sensor:
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();  
  sensorValue = analogRead(sensorPin);
  sensorValue1 = analogRead(sensorPin1);
  values = "#" + String(sensorValue) + "#" + String(sensorValue1) + "#" + String(temperature)+ "#" + String(humidity)+"#";
  Serial.flush();
  Serial.print(values);
  delay(600000);                                  // wait 10 mins for next reading

}
