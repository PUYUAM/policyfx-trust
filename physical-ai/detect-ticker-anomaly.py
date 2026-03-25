#!/usr/bin/env python3
# physical-ai/detect-ticker-anomaly.py — Detect anomalies in LED ticker feed

import json
from datetime import datetime
import re

# Mock ticker feed (in prod: reads from serial/USB or GPIO)
ticker_feed = [
    "USD/CNY=6.900 ▲0.02% | SHCOMP=3025.4 ▼0.23%",
    "USD/CNY=6.901 ▲0.03% | SHCOMP=3025.2 ▼0.24%",
    "USD/CNY=6.902 ▲0.04% | SHCOMP=3025.0 ▼0.25%",
    "USD/CNY=6.903 ▲0.05% | SHCOMP=3024.8 ▼0.26%",
    "USD/CNY=6.904 ▲0.06% | SHCOMP=3024.6 ▼0.27%",
    "USD/CNY=6.905 ▲0.07% | SHCOMP=3024.4 ▼0.28%",
    "USD/CNY=6.906 ▲0.08% | SHCOMP=3024.2 ▼0.29%",
    "USD/CNY=6.907 ▲0.09% | SHCOMP=3024.0 ▼0.30%",
    "USD/CNY=6.908 ▲0.10% | SHCOMP=3023.8 ▼0.31%",
    "USD/CNY=6.909 ▲0.11% | SHCOMP=3023.6 ▼0.32%",
    "USD/CNY=6.910 ▲0.12% | SHCOMP=3023.4 ▼0.33%",
    "USD/CNY=6.911 ▲0.13% | SHCOMP=3023.2 ▼0.34%",
    "USD/CNY=6.912 ▲0.14% | SHCOMP=3023.0 ▼0.35%",
    "USD/CNY=6.913 ▲0.15% | SHCOMP=3022.8 ▼0.36%",
    "USD/CNY=6.914 ▲0.16% | SHCOMP=3022.6 ▼0.37%",
    "USD/CNY=6.915 ▲0.17% | SHCOMP=3022.4 ▼0.38%",
    "USD/CNY=6.916 ▲0.18% | SHCOMP=3022.2 ▼0.39%",
    "USD/CNY=6.917 ▲0.19% | SHCOMP=3022.0 ▼0.40%",
    "USD/CNY=6.918 ▲0.20% | SHCOMP=3021.8 ▼0.41%",
    "USD/CNY=6.919 ▲0.21% | SHCOMP=3021.6 ▼0.42%"
]

# Baseline stats
baseline_usd_change = 0.01  # %/tick
baseline_shcomp_change = -0.02  # %/tick

anomalies = []
for i, line in enumerate(ticker_feed):
    try:
        # Parse USD/CNY and SHCOMP
        usd_match = re.search(r'USD/CNY=([\d.]+) ▲([\d.]+)%', line)
        shcomp_match = re.search(r'SHCOMP=([\d.]+) ▼([\d.]+)%', line)
        
        if usd_match and shcomp_match:
            usd_rate = float(usd_match.group(1))
            usd_change = float(usd_match.group(2))
            shcomp_val = float(shcomp_match.group(1))
            shcomp_change = float(shcomp_match.group(2))
            
            # Detect deviation
            if abs(usd_change - baseline_usd_change) > 0.05:
                anomalies.append({
                    "timestamp": datetime.now().isoformat(),
                    "type": "USD_CHANGE_ANOMALY",
                    "value": usd_change,
                    "baseline": baseline_usd_change,
                    "delta": usd_change - baseline_usd_change,
                    "severity": "high" if abs(usd_change - baseline_usd_change) > 0.1 else "medium"
                })
            
            if abs(shcomp_change - baseline_shcomp_change) > 0.05:
                anomalies.append({
                    "timestamp": datetime.now().isoformat(),
                    "type": "SHCOMP_CHANGE_ANOMALY",
                    "value": shcomp_change,
                    "baseline": baseline_shcomp_change,
                    "delta": shcomp_change - baseline_shcomp_change,
                    "severity": "high" if abs(shcomp_change - baseline_shcomp_change) > 0.1 else "medium"
                })
                
    except Exception as e:
        anomalies.append({
            "timestamp": datetime.now().isoformat(),
            "type": "PARSING_ERROR",
            "error": str(e),
            "line": line,
            "severity": "critical"
        })

# Save report
if anomalies:
    filename = f'alerts/ticker-anomaly-{datetime.now().strftime("%Y-%m-%d")}.json'
    with open(filename, 'w') as f:
        json.dump(anomalies, f, indent=2)
    print(f'✅ Anomalies detected: {len(anomalies)} → {filename}')
    for a in anomalies[:3]:
        print(f'   • {a["type"]}: {a["value"]} (δ={a["delta"]:.3f}) — {a["severity"]}')
else:
    print('✅ No anomalies detected.')
