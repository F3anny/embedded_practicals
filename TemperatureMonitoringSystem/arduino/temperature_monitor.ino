/*
  IoT Temperature Monitoring System
  Arduino Uno + DHT11 + 16x2 LCD I2C

  Connections:

  DHT11
  VCC  -> 3.3V (or 5V)
  GND  -> GND
  DATA -> D2

  LCD I2C
  VCC -> 5V
  GND -> GND
  SDA -> A4
  SCL -> A5
*/

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

// Try 0x27 first.
// If LCD doesn't display text, change to 0x3F.
LiquidCrystal_I2C lcd(0x27, 16, 2);

// CHANGE THIS TO YOUR NAME
String candidateName =
"IRIBAGIZA FANNY VEENA";

float temperature = 0;

unsigned long lastReadTime = 0;
const unsigned long readInterval = 2000;

unsigned long lastScrollTime = 0;
const unsigned long scrollInterval = 300;

int scrollPos = 0;

void setup()
{
  Serial.begin(9600);

  dht.begin();

  lcd.init();
  lcd.backlight();

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Initializing");
  lcd.setCursor(0, 1);
  lcd.print("System...");

  delay(2000);

  lcd.clear();

  Serial.println("SYSTEM STARTED");
}

void loop()
{
  unsigned long currentTime = millis();

  // Read temperature every 2 seconds
  if (currentTime - lastReadTime >= readInterval)
  {
    readTemperature();
    lastReadTime = currentTime;
  }

  // Update LCD continuously
  updateLCD();

  delay(50);
}

void readTemperature()
{
  float temp = dht.readTemperature();

  if (isnan(temp))
  {
    Serial.println("ERROR: SENSOR READ FAILED");
    return;
  }

  temperature = temp;

  // Send to PC
  Serial.print("TEMP:");
  Serial.println(temperature, 1);
}

void updateLCD()
{
  displayName();

  lcd.setCursor(0, 1);

  lcd.print("Temp:");
  lcd.print(temperature, 1);

  lcd.print((char)223); // degree symbol

  lcd.print("C   ");
}

void displayName()
{
  if (candidateName.length() <= 16)
  {
    lcd.setCursor(0, 0);

    lcd.print(candidateName);

    for (int i = candidateName.length();
         i < 16;
         i++)
    {
      lcd.print(" ");
    }

    return;
  }

  if (millis() - lastScrollTime >= scrollInterval)
  {
    String scrollText =
      candidateName + "    ";

    if (scrollPos >
        scrollText.length() - 16)
    {
      scrollPos = 0;
    }

    lcd.setCursor(0, 0);

    lcd.print(
      scrollText.substring(
        scrollPos,
        scrollPos + 16
      )
    );

    scrollPos++;

    lastScrollTime = millis();
  }
}