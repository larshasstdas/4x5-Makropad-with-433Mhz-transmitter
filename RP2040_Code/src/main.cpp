#include <Arduino.h>
#include <RCSwitch.h>

const int COLS = 5;
const int ROWS = 4;

const int colPINS[COLS] = {7, 4, 3, 2, 1};
const int rowPINS[ROWS] = {5, 8, 9, 10};

//bool keyState[ROWS][COLS] = {false};

volatile bool awake = false;

unsigned long lastPing = 0;
unsigned long lastPong = 0;

const unsigned long PING_INTERVAL = 2000;
const unsigned long PONG_SLEEP = 5000;

RCSwitch mySwitch = RCSwitch();
const unsigned long RF_CODE = 12345;
const int RF_BITS = 24;

bool buttonPressed(int &key);
void goToSleep();
void wakeToButton();
bool checkOnPC();
void startPC();


void setup() 
{
  Serial.begin(115200);
  lastPong = millis();

  for(int i = 0; i < COLS; i++)
  {
    pinMode(colPINS[i], OUTPUT);
    digitalWrite(colPINS[i], HIGH);
  }

  for(int i = 0; i < ROWS; i++)
  {
    pinMode(rowPINS[i], INPUT_PULLUP);
  }

  mySwitch.enableTransmit(0);
}


void loop()
{
  int key;
  unsigned long now = millis();

  if(now - lastPing >= PING_INTERVAL)
  {
    Serial.println("PING");
    lastPing = now;
  }

  if(Serial.available())
  {
    String msg = Serial.readStringUntil('\n');
    msg.trim();
    if(msg == "PONG")
    {
      lastPong = now;
    }
  }

  if(now - lastPong > PONG_SLEEP)
  {
    goToSleep();
    lastPong = millis();
  }

  if(buttonPressed(key))
  {
    if(key == 1)
    {
      if(!checkOnPC())
      {
        startPC();
      }
    }

    Serial.print("KEY_");
    Serial.println(key);
  }
  delay(5);
}

bool buttonPressed(int &key)
{
  static bool keyPressed = false;
  static unsigned long lastPressTime = 0;

  if (keyPressed && millis() - lastPressTime < 200) 
  {
    return false;
  }

  keyPressed = false;

  for(int i = 0; i < COLS; i++)
  {
    digitalWrite(colPINS[i], LOW);

    for(int j = 0; j < ROWS; j++)
    {
      if(digitalRead(rowPINS[j]) == LOW)
      {
        key = j*COLS + (COLS - 1 - i) + 1;
        keyPressed = true;
        lastPressTime = millis();
        digitalWrite(colPINS[i], HIGH);
        return true;
      }
    }
    digitalWrite(colPINS[i], HIGH);
  }
  return false;
}

void goToSleep()
{
  for(int i = 0; i < COLS; i++) {
    digitalWrite(colPINS[i], LOW);
  }

  for(int i = 0; i < ROWS; i++) {
    attachInterrupt(digitalPinToInterrupt(rowPINS[i]), wakeToButton, FALLING);
  }

  //TODO turn off LEDs

  awake = false;

  while(!awake)
  {
    __asm volatile ("wfi");
  }

  for(int i = 0; i < ROWS; i++) {
    detachInterrupt(digitalPinToInterrupt(rowPINS[i]));
  }

  for(int i = 0; i < COLS; i++) {
    digitalWrite(colPINS[i], HIGH);
  }
}

void wakeToButton()
{
  awake = true;
}

bool checkOnPC()
{
  Serial.println("PING");

  unsigned long time_of_ping = millis();

  while(millis() - time_of_ping < 500)
  {
    if(Serial.available())
    {
      String msg = Serial.readStringUntil('\n');
      msg.trim();
      if(msg == "PONG")
      {
        return true;
      }
    }
    delay(5);
  }
  return false;
}

void startPC()
{
  for (int i = 0; i < 5; i++) 
  {
    mySwitch.send(RF_CODE, RF_BITS);
    delay(5);
  }
}