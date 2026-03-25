#!/usr/bin/env python3
# physical/led-ticker.py — Drive LED ticker with live FX/SHCOMP

import json
from datetime import datetime

# Load data
try:
    with open('../data/fx/latest.json') as f:
        fx = json.load(f)
    with open('../data/shanghai/latest.json') as f:
        shcomp = json.load(f)
except:
    fx = {'rate': 6.900, 'change': '+0.02%'}
    shcomp = {'index': 3025.4, 'change': '-0.23%'}

# Build ticker string
ticker = f"USD/CNY={fx['rate']:.3f} {fx.get('change', '')} | SHCOMP={shcomp['index']:.1f} {shcomp.get('change', '')}"

print('💡 LED ticker message:')
print(ticker)

# In prod: send to hardware via rpi_ws281x or serial
# This is the exact string sent to display