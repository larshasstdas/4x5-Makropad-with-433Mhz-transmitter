#include <Arduino.h>
#include <RCSwitch.h>
#include <Adafruit_NeoPixel.h>

#define STARTBYTE 0xAB
#define BYTE_PINGPONG   'P'
#define BYTE_KEY        'K'
#define BYTE_LED        'L'
#define BYTE_MODE       'M'

#define MODE_STATIC   0
#define MODE_BREATHING 1
#define MODE_RAINBOW  2

#define LED_PIN 6          // GPIO6 = LED-Data
#define NUM_LEDS 20

uint8_t currentMode = MODE_STATIC;
uint8_t currentColor[3] = {0, 0 , 30};   //GRB
uint8_t currentSpeed = 100;
uint8_t dimFactor[NUM_LEDS];

Adafruit_NeoPixel pixels(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

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
const unsigned long RF_CODE = 12341;
const int RF_BITS = 24;

bool buttonPressed(uint8_t &key);
void goToSleep();
void wakeToButton();
void startPC();
void sendData(uint8_t type, uint8_t length, uint8_t *data);
bool receiveData(uint8_t *type, uint8_t *length, uint8_t *data);
void renderMode();
void applyDimMask();
void setMode(uint8_t *data, uint8_t length);


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

  for (int i = 0; i < NUM_LEDS; i++) 
  {
    dimFactor[i] = 255;
  }

  pixels.begin();
  pixels.setBrightness(80);
  pixels.clear();
  pixels.show();

  mySwitch.enableTransmit(0);
}


void loop()
{
  uint8_t key;
  uint8_t type, length, data[60];

  if(millis() - lastPing >= PING_INTERVAL)
  {
    sendData('P', 0, nullptr);
    lastPing = millis();
  }

  if(receiveData(&type, &length, data))
  {
    if(type == BYTE_PINGPONG)
    {
      lastPong = millis();
    }
    else if(type == BYTE_MODE)
    {
      setMode(data, length);
    }
    else if(type == BYTE_LED)
    {
      if(length == NUM_LEDS)
      {
        memcpy(dimFactor, data, NUM_LEDS);
      }
    }
  }

  if(millis() - lastPong > PONG_SLEEP)
  {
    goToSleep();
    lastPong = millis();
  }

  if(buttonPressed(key))
  {
    if(key == 1)
    {
      sendData(BYTE_PINGPONG, 0, nullptr);
      lastPing = millis();

      bool gotPong = false;
      
      while(millis() - lastPing < 1000)
      {
        uint8_t t, l, d[60];
        if(receiveData(&t, &l, d) && t == BYTE_PINGPONG)
        {
          gotPong = true;
          break;
        }
      }   
      if(!gotPong)
      {
        startPC();
      }  
    }
    sendData(BYTE_KEY, 1, &key);
  }

  renderMode();
  applyDimMask();
  pixels.show();

  delay(5);
}

bool buttonPressed(uint8_t &key)
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
  for(int i = 0; i < COLS; i++) 
  {
    digitalWrite(colPINS[i], LOW);
  }

  for(int i = 0; i < ROWS; i++) 
  {
    attachInterrupt(digitalPinToInterrupt(rowPINS[i]), wakeToButton, FALLING);
  }

  pixels.clear();
  pixels.show();

  awake = false;

  while(!awake)
  {
    __asm volatile ("wfi");
  }

  for(int i = 0; i < ROWS; i++) 
  {
    detachInterrupt(digitalPinToInterrupt(rowPINS[i]));
  }

  for(int i = 0; i < COLS; i++) 
  {
    digitalWrite(colPINS[i], HIGH);
  }
}

void wakeToButton()
{
  awake = true;
}

void startPC()
{
  for (int i = 0; i < 5; i++) 
  {
    mySwitch.send(RF_CODE, RF_BITS);
    delay(5);
  }
}

void sendData(uint8_t type, uint8_t length, uint8_t *data)
{
  Serial.write(STARTBYTE);
  Serial.write(type);
  Serial.write(length);
  for(int i = 0; i < length; i++)
  {
    Serial.write(data[i]);
  }
}

bool receiveData(uint8_t *type, uint8_t *length, uint8_t *data)
{
  static bool headerRead = false;
  static uint8_t TYPE = 0;
  static uint8_t LENGTH = 0;
  static uint8_t currentLength = 0;
  static uint8_t DATA[60];

  if(!headerRead)
  {
    if(Serial.available() < 3) return false;

    if(Serial.read() != STARTBYTE) return false;

    TYPE = Serial.read();
    LENGTH = Serial.read();
    currentLength = 0;
    headerRead = true;

    if(LENGTH > 60)
    {
      headerRead = false;
      return false;
    }
  }
  while(currentLength < LENGTH && Serial.available() > 0)
  {
    DATA[currentLength] = Serial.read();
    currentLength++;
  }
  if(currentLength >= LENGTH)
  {
    *type = TYPE;
    *length = LENGTH;
    memcpy(data, DATA, LENGTH);
    headerRead = false;
    return true;
  }
  return false;
}

void renderMode()
{
  switch (currentMode)
  {
    case MODE_STATIC:
      for (int i = 0; i < NUM_LEDS; i++) 
      {
        pixels.setPixelColor(i, currentColor[1], currentColor[0], currentColor[2]);
      }
      break;

    case MODE_RAINBOW:

      static uint16_t hue = 0;
      for (int i = 0; i < NUM_LEDS; i++) 
      {
        int mod = i % 10;
        if (mod > 4)
        {
          mod = 9 - mod;
        }
        uint16_t ledhue = mod*3000 + hue;
        pixels.setPixelColor(i, pixels.ColorHSV(ledhue));
      }

      hue += currentSpeed / 2;
      break;

    case MODE_BREATHING:
    {
      float phase = (millis() % (6000 - currentSpeed * 20)) / (float)(6000 - currentSpeed * 20);
      float b = (sin(phase * 2 * PI) + 1.0) / 2.0;
      for (int i = 0; i < NUM_LEDS; i++) 
      {
        pixels.setPixelColor(i,
          currentColor[1] * b,
          currentColor[0] * b,
          currentColor[2] * b);
      }
      break;
    }
  }
}

void applyDimMask()
{
  uint8_t *buf = pixels.getPixels();
  for (int i = 0; i < NUM_LEDS; i++) {
    uint8_t f = dimFactor[i];
    buf[i*3]   = (buf[i*3]   * f) >> 8;   // G
    buf[i*3+1] = (buf[i*3+1] * f) >> 8;   // R
    buf[i*3+2] = (buf[i*3+2] * f) >> 8;   // B
  }
}

void setMode(uint8_t *data, uint8_t length)
{
  currentMode = data[0];

  switch(currentMode)
  {
    case MODE_STATIC:
      // [modus, G, R, B]
      if(length == 4) {
        memcpy(currentColor, data + 1, 3);
      }
      break;

    case MODE_RAINBOW:
      // [modus, speed]
      if(length == 2) {
        currentSpeed = data[1];
      }
      break;

    case MODE_BREATHING:
      // [modus, speed, G, R, B]
      if(length == 5) {
        currentSpeed = data[1];
        memcpy(currentColor, data + 2, 3);
      }
      break;
  }
}