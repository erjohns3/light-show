#define FASTLED_ESP32_I2S

#include <FastLED.h>

#define STRIP_COUNT 10
#define STRIP_LENGTH 64
#define LED_COUNT STRIP_COUNT * STRIP_LENGTH
#define BUFFER_SIZE LED_COUNT * 3

CRGB leds[STRIP_COUNT][STRIP_LENGTH];
byte buffer[BUFFER_SIZE];


void setup() {
  // Serial.begin(115200);
  Serial2.setRxBufferSize(4096);
  Serial2.begin(2000000);
  Serial2.write(255);

  for(int i=0; i<STRIP_COUNT; i++){
    for(int j=0; j<STRIP_LENGTH; j++){
      leds[i][j] = CRGB(0, 0, 0);
    }
  }

  FastLED.addLeds< WS2812B, 4, RGB >( leds[0], STRIP_LENGTH );
  FastLED.addLeds< WS2812B, 27, RGB >( leds[1], STRIP_LENGTH );
  FastLED.addLeds< WS2812B, 21, RGB >( leds[2], STRIP_LENGTH );
  FastLED.addLeds< WS2812B, 18, RGB >( leds[3], STRIP_LENGTH );
  FastLED.addLeds< WS2812B, 13, RGB >( leds[4], STRIP_LENGTH );
  FastLED.addLeds< WS2812B, 23, RGB >( leds[5], STRIP_LENGTH );
  FastLED.addLeds< WS2812B, 19, RGB >( leds[6], STRIP_LENGTH );
  FastLED.addLeds< WS2812B, 5, RGB >( leds[7], STRIP_LENGTH );
  FastLED.addLeds< WS2812B, 22, RGB >( leds[8], STRIP_LENGTH );
  FastLED.addLeds< WS2812B, 25, RGB >( leds[9], STRIP_LENGTH );
  FastLED.show();
}

void loop() {
  if (Serial2.readBytes(buffer, BUFFER_SIZE) == BUFFER_SIZE){
    while(Serial2.available() > BUFFER_SIZE){
      Serial2.readBytes(buffer, BUFFER_SIZE);
    }
    Serial2.write(255);
    int index = 0;
    for(int i=0; i<STRIP_COUNT; i++){
      for(int j=0; j<STRIP_LENGTH; j++){
        leds[i][j] = CRGB(buffer[index], buffer[index+1], buffer[index+2]);
        index += 3;
      }
    }
    FastLED.show();
  }
}




// old code

// #define FASTLED_ESP32_I2S

// #include <FastLED.h>

// #define STRIP_COUNT 10
// #define STRIP_LENGTH 64
// #define LED_COUNT STRIP_COUNT * STRIP_LENGTH
// #define BUFFER_SIZE LED_COUNT * 3

// CRGB leds[STRIP_COUNT][STRIP_LENGTH];
// byte buffer[BUFFER_SIZE];


// void setup() {
//   // Serial.begin(115200);
//   Serial2.setRxBufferSize(4096);
//   Serial2.begin(2000000);

//   for(int i=0; i<STRIP_COUNT; i++){
//     for(int j=0; j<STRIP_LENGTH; j++){
//       leds[i][j] = CRGB(0, 0, 0);
//     }
//   }

//   FastLED.addLeds< WS2812B, 4, RGB >( leds[0], STRIP_LENGTH );
//   FastLED.addLeds< WS2812B, 27, RGB >( leds[1], STRIP_LENGTH );
//   FastLED.addLeds< WS2812B, 21, RGB >( leds[2], STRIP_LENGTH );
//   FastLED.addLeds< WS2812B, 18, RGB >( leds[3], STRIP_LENGTH );
//   FastLED.addLeds< WS2812B, 13, RGB >( leds[4], STRIP_LENGTH );
//   FastLED.addLeds< WS2812B, 23, RGB >( leds[5], STRIP_LENGTH );
//   FastLED.addLeds< WS2812B, 19, RGB >( leds[6], STRIP_LENGTH );
//   FastLED.addLeds< WS2812B, 5, RGB >( leds[7], STRIP_LENGTH );
//   FastLED.addLeds< WS2812B, 22, RGB >( leds[8], STRIP_LENGTH );
//   FastLED.addLeds< WS2812B, 25, RGB >( leds[9], STRIP_LENGTH );
//   FastLED.show();
// }

// // 101 magic, then 0-100 rgb
// void loop() {
//   int size = Serial2.readBytes(buffer, BUFFER_SIZE);
//   if(size == BUFFER_SIZE){
//     while(Serial2.available() > BUFFER_SIZE){
//       Serial2.readBytes(buffer, BUFFER_SIZE);
//     }
//     Serial2.write(255);
//     int index = 0;
//     for(int i=0; i<STRIP_COUNT; i++){
//       for(int j=0; j<STRIP_LENGTH; j++){
//         leds[i][j] = CRGB(buffer[index], buffer[index+1], buffer[index+2]);
//         index += 3;
//       }
//     }
//     FastLED.show();
//   } else if(size == 0){
//     // !TODO write on the first failed read, then every 20ms
//     Serial2.write(255);
//   }
// }