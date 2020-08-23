#define I2C_SLAVE_ADDRESS 0x1E
#define RX 3
#define TX 2
#define DEBUG false
#include <Wire.h>
#include <SoftwareSerial.h>

String data="";
int latest=0;
SoftwareSerial gc10(RX, TX);

void setup() {
  Wire.begin(I2C_SLAVE_ADDRESS);
  Wire.onRequest(getLatest);
  gc10.begin(9600);
  if(DEBUG) {
    Serial.begin(9600);
  }
}

void loop(){
  if (gc10.available() > 0) {
    data = gc10.readStringUntil('\n');
    latest = data.toInt();
    if(DEBUG) {
      Serial.println(latest, DEC);
    }
  }
}
 
void getLatest() {
  Wire.write(latest);
  if(DEBUG) {
    Serial.println(latest, DEC);
  }
}
