# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time

from rpi_ws281x import ws, Color, Adafruit_NeoPixel

# LED strip configuration:
LED_COUNT = 20        # Number of LED pixels.
LED_PIN = 13          # GPIO pin connected to the pixels (must support PWM! GPIO 13 and 18 on RPi 3).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (Between 1 and 14)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 1       # 0 or 1
LED_STRIP = ws.WS2811_STRIP_RGB

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ,
                            LED_DMA, LED_INVERT, LED_BRIGHTNESS,
                            LED_CHANNEL, LED_STRIP)

strip.begin()

num = 0

while True:
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(255, 0, 0))
    strip.show()
    print(f'show: {num}')
    num = (num + 1) % strip.numPixels()
    time.sleep(0.1)