// Import the necessary libraries
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <unordered_map>
#include <ArduinoJson.h>

// Set new names for pins
#define lm35 A0
#define fan D0
#define pin1 D1
#define pin2 D2
#define pin3 D3
#define pin4 D4
#define rgb D5
#define redpin D6
#define greenpin D7
#define bluepin D8

// Set access point name and password
const char *ssid = "SMART-ROOM";
const char *password = "smartroompass";

const int point_temp = 80; // Set the temperature comparison point
const unsigned long interval = 60000; // Set the interrupt value
unsigned long previousMillis = 0; //variable to save time


// Set Color Default value for color channels
int redvalue = 255;
int greenvalue = 255;
int bluevalue = 255;

ESP8266WebServer server(80); //Create a server object

// Function to get analog value and calculate temperature in Celsius
float get_temp() {
  float temp = analogRead(lm35) * (5.0 / 1023.0) * 100;
  return temp;
}

// Panel display function
void route_root() {
  server.send(200, "text/html", "<!DOCTYPE html> <html lang='en'> <head> <meta charset='UTF-8'> <meta name='viewport' content='width=device-width, initial-scale=1.0'> <title>Home Page</title> <style> body { margin: 0; padding: 0; display: flex; align-items: center; justify-content: center; height: 100vh; font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; background: rgb(2, 0, 36); background: linear-gradient(164deg, rgba(2, 0, 36, 1) 0%, rgba(9, 9, 121, 1) 47%, rgba(0, 212, 255, 1) 100%); } .rectangle { width: 40%; height: 70%; text-align: center; color: white; } @media (max-width:500px) { .rectangle { width: 70%; height: 70%; text-align: center; color: white; } } h1 { margin-top: auto; font-size: 60px; } p { font-weight: 700; } p a { color: dodgerblue; text-shadow: 1px 1px black; } .btn { all: unset; } .btn div { font-size: 25px; background-color: royalblue; padding: 20px; margin-top: 24px; border-radius: 64px; } a { all: unset; color: white; } </style> </head> <body> <div class='rectangle'> <h1>Panel</h1> <p>Everything is correct!</p> <p>Programmer: <a href='https://github.com/kinite-gp'>kinite-gp</a></p><a class='btn' href='/rgb'> <div>RGB Controller</div> </a><a class='btn' href='/light'> <div>Lights Controller</div> </a><a class='btn' href='#'> <div>Temp:" + String(get_temp()) + " ℃</div> </a> </div> </body> </html>");
}

// function to change the state of the pins
void route_light_post() {
  String baseNumber = server.arg("baseNumber");

  if (baseNumber != "") {
    int pinNumber = baseNumber.toInt();

    if (pinNumber == 1) {
      if (digitalRead(pin1) == HIGH) {
        digitalWrite(pin1, LOW);
      } else {
        digitalWrite(pin1, HIGH);
      }
    } else if (pinNumber == 2) {
      if (digitalRead(pin2) == HIGH) {
        digitalWrite(pin2, LOW);
      } else {
        digitalWrite(pin2, HIGH);
      }
    } else if (pinNumber == 3) {
      if (digitalRead(pin3) == HIGH) {
        digitalWrite(pin3, LOW);
      } else {
        digitalWrite(pin3, HIGH);
      }
    } else if (pinNumber == 4) {
      if (digitalRead(pin4) == HIGH) {
        digitalWrite(pin4, LOW);
      } else {
        digitalWrite(pin4, HIGH);
      }
    } else if (pinNumber == 5) {
      if (digitalRead(rgb) == HIGH) {
        digitalWrite(rgb, LOW);
      } else {
        digitalWrite(rgb, HIGH);
      }
    }
    route_read();
  } else {
    String responseMessage = "{\"message\":\"bad requests\"";
    server.send(400, "application/json", responseMessage);
  }
}

// Color panel display function
void route_light_get() {
  server.send(200, "text/html", "<!DOCTYPE html> <html lang='en'> <head> <meta charset='UTF-8'> <meta name='viewport' content='width=device-width, initial-scale=1.0'> <title>Light Contol</title> <style> body { margin: 0; padding: 0; display: flex; align-items: center; justify-content: center; height: 100vh; font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; background: rgb(2, 0, 36); background: linear-gradient(164deg, rgba(2, 0, 36, 1) 0%, rgba(9, 9, 121, 1) 47%, rgba(0, 212, 255, 1) 100%); } .rectangle { width: 40%; height: 70%; text-align: center; color: white; } @media (max-width:500px) { .rectangle { width: 70%; height: 80%; text-align: center; color: white; } } h1 { margin-top: auto; font-size: 60px; } p { font-weight: 700; } p a { color: dodgerblue; text-shadow: 1px 1px black; } .btn { all: unset; } .btn div { font-size: 25px; background-color: royalblue; padding: 20px; margin-top: 24px; border-radius: 64px; color: white; } a { all: unset; color: white; } .pb { margin-top: 24px; } body { display: flex; flex-direction: column; } </style> </head> <body> <div class='rectangle'> <h1>Light Controller</h1> <a class='btn' href='#' onclick='executeServerCode(1); return false;'> <div>Pin One</div> </a> <a class='btn' href='' onclick='executeServerCode(2); return false;'> <div>Pin Two</div> </a> <a class='btn' href='#' onclick='executeServerCode(3); return false;'> <div>Pin three</div> </a> <a class='btn' href='#' onclick='executeServerCode(4); return false;'> <div>Pin Four</div> </a> <a class='btn' href='#' onclick='executeServerCode(5); return false;'> <div>Pin RGB</div> </a> </div> <a class='btn pb' href='/'> <div class='btn'>Back Menu</div> </a> <script> function executeServerCode(input) { var link = '/light?baseNumber=' + input; console.log('Link:', link); var xhr = new XMLHttpRequest(); xhr.open('POST', link, true); xhr.send(); } </script> </body> </html>");
}

// Pin status display function
void route_read() {
  StaticJsonDocument<200> ports;
  bool isHigh = true;

  isHigh = digitalRead(pin1) == HIGH;
  ports["pin_1"] = isHigh ? "High" : "Low";

  isHigh = digitalRead(pin2) == HIGH;
  ports["pin_2"] = isHigh ? "High" : "Low";

  isHigh = digitalRead(pin3) == HIGH;
  ports["pin_3"] = isHigh ? "High" : "Low";

  isHigh = digitalRead(pin4) == HIGH;
  ports["pin_4"] = isHigh ? "High" : "Low";

  isHigh = digitalRead(rgb) == HIGH;
  ports["pin_RGB"] = isHigh ? "High" : "Low";

  isHigh = digitalRead(fan) == HIGH;
  ports["pin_FAN"] = isHigh ? "High" : "Low";

  String jsonStatus;
  serializeJson(ports, jsonStatus);
  server.send(200, "application/json", jsonStatus);
}

// Color change function
void route_rgb_post() {
  String red = server.arg("red");
  String green = server.arg("green");
  String blue = server.arg("blue");

  int redValue = red.toInt();
  int greenValue = green.toInt();
  int blueValue = blue.toInt();

  analogWrite(redpin, redValue);
  analogWrite(greenpin, greenValue);
  analogWrite(bluepin, blueValue);
}

// Color changing panel display function
void route_rgb_get() {
  server.send(200, "text/html", "<!DOCTYPE html> <html lang='en'> <head> <meta charset='UTF-8'> <meta name='viewport' content='width=device-width, initial-scale=1.0'> <title>RGB Controller Form</title> <style> body { margin: 0; padding: 0; display: flex; align-items: center; justify-content: center; height: 100vh; font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; background: rgb(2, 0, 36); background: linear-gradient(164deg, rgba(2, 0, 36, 1) 0%, rgba(9, 9, 121, 1) 47%, rgba(0, 212, 255, 1) 100%); } .rectangle { width: 40%; height: 70%; text-align: center; color: white; } @media (max-width:500px) { .rectangle { width: 70%; height: 70%; text-align: center; color: white; } } .colorPicker { width: 100%; height: 90px; margin-top: 24px; } .btn { all: unset; font-size: 25px; background-color: royalblue; padding: 20px; margin-top: 24px; border-radius: 64px; color: white; } .rgbForm { margin-bottom: 50px; } a { all: unset; color: white; } body { display: flex; flex-direction: column; } </style> </head> <body> <div class='rectangle'> <h1>RGB Controller</h1> <form id='rgbForm' class='rgbForm'><input type='color' class='colorPicker' id='colorPicker' name='colorPicker'><input type='submit' class='btn' value='Apply Change'></form> </div> <a href='/'> <div class='btn a'>Back Menu</div> </a> <script>var rgbForm = document.getElementById('rgbForm'); rgbForm.addEventListener('submit', function (event) { event.preventDefault(); var colorPicker = document.getElementById('colorPicker'); var selectedColor = colorPicker.value; var rgbArray = selectedColor.match(/\\w\\w/g).map(function (hex) { return parseInt(hex, 16); }); fetch('/rgb?red=' + rgbArray[0] + '&green=' + rgbArray[1] + '&blue=' + rgbArray[2], { method: 'POST', }).then(response => response.json()).then(data => { console.log('ok', data); }).catch(error => { console.error('no', error); }); }); </script> </body> </html>");
}

void setup() {
  // Setting the required pins to be on
  pinMode(fan, OUTPUT);
  pinMode(pin1, OUTPUT);
  pinMode(pin2, OUTPUT);
  pinMode(pin3, OUTPUT);
  pinMode(pin4, OUTPUT);

  pinMode(rgb, OUTPUT);

  pinMode(redpin, OUTPUT);
  pinMode(greenpin, OUTPUT);
  pinMode(bluepin, OUTPUT);

  Serial.begin(115200); // Setting up the serial port
  WiFi.softAP(ssid, password); // Setting up the access point

  // Show ip server in serial
  IPAddress myip = WiFi.softAPIP();
  Serial.print("\n\nControl Panel IP Address: ");
  Serial.println(myip);

  // Enable server routes
  server.on("/", HTTP_GET, route_root);
  server.on("/light", HTTP_POST, route_light_post);
  server.on("/light", HTTP_GET, route_light_get);
  server.on("/read", HTTP_GET, route_read);
  server.on("/rgb", HTTP_POST, route_rgb_post);
  server.on("/rgb", HTTP_GET, route_rgb_get);

  // Setting up the server
  server.begin();
}

void loop() {
  // Accept server requests
  server.handleClient();

  // Current time storage
  unsigned long currentMillis = millis();

  // Fan activation based on sensor temperature
  // It is checked every minute
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    if (get_temp() > point_temp) {
      if (digitalRead(fan) == LOW) {
        digitalWrite(fan, HIGH);
      }
    } else {
      if (digitalRead(fan) == HIGH) {
        digitalWrite(fan, LOW);
      }
    }
  }
}
