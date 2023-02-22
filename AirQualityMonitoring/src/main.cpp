#include <Arduino.h>
#include "time.h"
#include "DHT.h"
#define DHTPIN 33
#define DHTTYPE DHT11 

#if defined(ESP32)
  #include <WiFi.h>
#elif defined(ESP8266)
  #include <ESP8266WiFi.h>
#endif
#include <Firebase_ESP_Client.h>

//Provide the token generation process info.
#include "addons/TokenHelper.h"
//Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"

// Insert your network credentials
#define WIFI_SSID "Access"
#define WIFI_PASSWORD "s12345678m"

// Insert Firebase project API Key
#define API_KEY "AIzaSyBs6sAl-s6FhpNSiQG0uNH85KCChs7ETLk"

// Insert RTDB URLefine the RTDB URL */
#define DATABASE_URL "https://air-pollution-monitoring-a88eb-default-rtdb.firebaseio.com" 

//Define Firebase Data object
FirebaseData fbdo;

FirebaseAuth auth;
FirebaseConfig config;

// NTP server
const char* ntpServer = "pool.ntp.org";


int mq7A = 34;    // select the input pin for the sensor 14
int mq8A = 35;    // select the input pin for the sensor 27
int mq135A = 32;    // select the input pin for the sensor 26

int mq7D = 14;    // select the input pin for the sensor 34
int mq8D = 27;    // select the input pin for the sensor 35
int mq135D = 26;    // select the input pin for the sensor 32

int mg7AV = 0;  // variable to store the value coming from the sensor
int mq8AV = 0;  // variable to store the value coming from the sensor
int mq135AV = 0;  // variable to store the value coming from the sensor

int mq7DV;  // variable to store the value coming from the sensor
int mq8DV;  // variable to store the value coming from the sensor
int mq135DV;  // variable to store the value coming from the sensor

String values;

// epoch time variable
unsigned long epochTime;

unsigned long duration;
unsigned long starttime;
unsigned long sampletime_ms = 2000;//sampe 30s&nbsp;;
unsigned long lowpulseoccupancy = 0;
float ratio = 0;
float pmValue = 0;

DHT dht(DHTPIN, DHTTYPE);

unsigned long sendDataPrevMillis = 0;
int count = 0;
bool signupOK = false;

void setup(){
  Serial.begin(115200);
  Serial.println("Initializing...");
  pinMode(mq7D, INPUT);
  pinMode(mq8D, INPUT);
  pinMode(mq135D, INPUT);
  dht.begin();
  configTime(0, 0, ntpServer);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED){
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  /* Assign the api key (required) */
  config.api_key = API_KEY;

  /* Assign the RTDB URL (required) */
  config.database_url = DATABASE_URL;

  /* Sign up */
  if (Firebase.signUp(&config, &auth, "", "")){
    Serial.println("ok");
    signupOK = true;
  }
  else{
    Serial.printf("%s\n", config.signer.signupError.message.c_str());
  }

  /* Assign the callback function for the long running token generation task */
  config.token_status_callback = tokenStatusCallback; //see addons/TokenHelper.h
  
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);

  starttime = millis();//get the current time; 
  Serial.println("Heating up sensors elements..."); 
  pinMode(LED_BUILTIN, HIGH); delay(120000); // Delay for 2 min to heatup the sensors 
  Serial.println("Done initializing..."); pinMode(LED_BUILTIN, LOW);
  

}


unsigned long getTime(){
  time_t now;
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)){
    return(0);
  }
  time(&now);
  return now;
}


void loop(){
  // read the value from the sensor:
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();  
  mg7AV = analogRead(mq7A);
  mq8AV = analogRead(mq8A);
  mq135AV = analogRead(mq135A);
  values = "#" + String(mg7AV) + "#" + String(mq8AV) + "#"+ String(mq135AV) + "#" + String(mq7DV) + "#" + String(mq8DV) + "#" + String(mq135DV) + "#" + String(temperature)+ "#" + String(humidity)+"#";
  Serial.println(values);
  Serial.flush();
  delay(10000);                                  // wait 10 seconds for next reading
  if (Firebase.ready() && signupOK && (millis() - sendDataPrevMillis > 15000 || sendDataPrevMillis == 0)){
    sendDataPrevMillis = millis();
    // Write an Int number on the database path test/int
    epochTime = getTime();

    // Write an sensor data on the database path Swiss
    if (Firebase.RTDB.setString(&fbdo, "Swiss/" + String(epochTime), values)){
      Serial.println("PASSED");
      Serial.println("PATH: " + fbdo.dataPath());
      Serial.println("TYPE: " + fbdo.dataType());
    }
    else {
      Serial.println("FAILED");
      Serial.println("REASON: " + fbdo.errorReason());
    }
  
  }
}


