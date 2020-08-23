// SCL:A5 SDA:A4
#include <SoftwareSerial.h>
#include <Wire.h>
#include "SparkFunBME280.h"  /* https://github.com/sparkfun/SparkFun_BME280_Arduino_Library/releases */
#include <BH1750FVI.h>  /* https://github.com/PeterEmbedded/BH1750FVI/releases */
#include <K30_I2C.h>  /* https://github.com/FirstCypress/K30_CO2_I2C_Arduino/tree/master */

BME280 myBME280;
BH1750FVI gy302(BH1750FVI::k_DevModeContLowRes);
K30_I2C k30_i2c = K30_I2C(0x68);

void setup(){
  // ========== GENERAL START ==========
  Serial.begin(9600);
  Wire.begin();
  // ========== GENERAL END ==========
  // ========== BME280 START ==========
  myBME280.settings.commInterface = I2C_MODE; 
  myBME280.settings.I2CAddress = 0x76;
  myBME280.settings.runMode = 3; 
  myBME280.settings.tStandby = 0;
  myBME280.settings.filter = 0;
  myBME280.settings.tempOverSample = 1 ;
  myBME280.settings.pressOverSample = 1;
  myBME280.settings.humidOverSample = 1;
  myBME280.begin();
  // ========== BME280 END ==========
  // ========== GY302 START ==========
  gy302.begin();
  // ========== GY302 END ==========
}

void loop(){
  // Format: Temperature(℃),Humidity(%),Pressure(hPa),CO2(ppm),O2(%),Lux(lx),Radiation(CPM),Radiation(μSv/h)
  // ========== BME280 START ==========
  Serial.print(myBME280.readTempC(), 2);
  Serial.print(",");
  Serial.print(myBME280.readFloatHumidity(), 2);
  Serial.print(",");
  Serial.print(myBME280.readFloatPressure() / 100, 2);
  // ========== BME280 END ==========
  Serial.print(",");
  // ========== K30_CO2 START ==========
  int co2 = 0;
  k30_i2c.readCO2(co2);
  Serial.print(co2);
  // ========== K30_CO2 END ==========
  Serial.print(",");
  // ========== GY302 START ==========
  Serial.print(gy302.GetLightIntensity());
  // ========== GY302 END ==========
  Serial.print(",");
  // ========== GC10 START ==========
  float cpm = readGc10Cpm();
  Serial.print(cpm, 0);
  Serial.print(",");
  Serial.print(cpm / 165.5629139072848, 3);
  // ========== GC10 END ==========
  Serial.println("");
  delay(300);
}

float readGc10Cpm(){
  Wire.requestFrom(0x1E, 1);
  return Wire.read();
}
