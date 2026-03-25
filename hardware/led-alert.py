#!/usr/bin/env python3
# hardware/led-alert.py — Control RGB LED strip on FX breach

import json
import time
import os
from datetime import datetime

# Simulate LED control (real version would use rpi_ws281x)
LED_PIN = 18
LED_COUNT = 8

def led_red_flash():
    print('🚨 LED ALERT: RED FLASH (simulated)')
    # In prod: 
    # strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, ...)
    # strip.begin()
    # for i in range(3):
    #     for j in range(strip.numPixels()):
    #         strip.setPixelColor(j, Color(255, 0, 0))
    #     strip.show()
    #     time.sleep(0.3)
    #     strip.clear()
    #     strip.show()
    #     time.sleep(0.3)

def check_fx_breach():
    try:
        with open('../data/fx/latest.json') as f:
            fx = json.load(f)
        if fx.get('rate', 0) > 7.35:
            print(f'⚠️  FX BREACH DETECTED: {fx["rate"]} > 7.35')
            led_red_flash()
            return True
    except Exception as e:
        print(f'❌ Error reading FX data: {e}')
    return False

if __name__ == '__main__':
    print(f'🔍 Checking FX breach at {datetime.now()}')
    check_fx_breach()
