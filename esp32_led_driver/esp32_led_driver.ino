#define FASTLED_ESP32_I2S
// #define FASTLED_FORCE_SOFTWARE_SPI

#include <FastLED.h>

#define STRIP_COUNT 10
#define STRIP_LENGTH 64
#define LED_COUNT STRIP_COUNT * STRIP_LENGTH
#define BUFFER_SIZE LED_COUNT * 3

CRGB leds[STRIP_COUNT][STRIP_LENGTH];
byte buffer[BUFFER_SIZE];

int num = 0;
int bads = 0;

void setup() {
  Serial.begin(115200);
  Serial2.setRxBufferSize(4096);
  Serial2.begin(2000000);
  // Serial2.begin(4000000, SERIAL_8N1, -1, -1, false, 20000UL, 4096);

  for(int i=0; i<STRIP_COUNT; i++){
    for(int j=0; j<STRIP_LENGTH; j++){
      leds[i][j] = CRGB(0, 0, 0);
    }
  }

  // safe pins: 4 5 12 13 14 15 18 19 21 22 23 25 26 27 32 33

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

  // FastLED.setMaxRefreshRate(100);

  FastLED.show();
}

void loop() {  
  int size = Serial2.readBytes(buffer, BUFFER_SIZE);
  // Serial.println(size);
  if(size == BUFFER_SIZE){
    // Serial.println(buffer[1000]);
    while(Serial2.available() > BUFFER_SIZE){
      Serial2.readBytes(buffer, BUFFER_SIZE);
    }
    Serial2.write(255);
    int index = 0;
    bool bad = false;
    for(int i=0; i<STRIP_COUNT; i++){
      for(int j=0; j<STRIP_LENGTH; j++){
        leds[i][j] = CRGB(buffer[index], buffer[index+1], buffer[index+2]);
        // if(buffer[index] != 0 || buffer[index+1] != 0 || (buffer[index+2] != 0 && buffer[index+2] != 170 && buffer[index+2] != 171)){
        //   bad = true;
        //   bads++;
        // }
        index += 3;
      }
    }
    // unsigned long start_time = micros();
    FastLED.show();
    // if(bad){
    //   Serial.println("---ERROR---ERROR---ERROR---");
    // }
    // Serial.println(bads);
    // unsigned long end_time = micros();
    // Serial.println("Good");
    // Serial.println(end_time - start_time);
  }else if(size == 0){
    Serial2.write(255);
  }
  // num++;

  // int index = 0;
  // // int power = int(127.5 * sin(millis()/1000.0 * 3.14) + 127.5);
  // for(int i=0; i<STRIP_COUNT; i++){
  //   for(int j=0; j<STRIP_LENGTH; j++){
  //     leds[i][j] = CRGB(random(256), 0, 0);
  //     index += 3;
  //   }
  // }
  // // Serial.println(power);
  // // unsigned long start_time = micros();
  // FastLED.show();
  // num++;
  // delay(20);
  

  // FastLED.show();
  // delay(100);
  // Serial.println(num);
  // num++;

  // for(int i=0; i<STRIP_COUNT; i++){
  //   for(int j=0; j<STRIP_LENGTH; j++){
  //     leds[i][j] = CRGB(0, 0, 0);
  //   }
  // }
  // for(int i=0; i<STRIP_COUNT; i++){
  //   leds[i][48] = CRGB(255, 0, 0);
  // }
  // // leds[int(num / STRIP_LENGTH / 10) % STRIP_COUNT][int(num / 10) % STRIP_LENGTH] = CRGB(255, 0, 0);
  // num++;
  // // unsigned long start_time = micros();
  // FastLED.show();
  // unsigned long end_time = micros();
  // Serial.println("Good");
  // Serial.println(end_time - start_time);
}
