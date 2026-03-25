# Audit Trail — How to Verify Every Value

This layer is designed for *regulatory-grade trust*. You can verify every number, every decision, every alert.

## Where Logs Live
- `data/audit/log.csv`: CSV with every fetch attempt (timestamp, URL, status, age, error)
- `data/policy/latest.json`: Full JSON payload + `fetchedAt`, `sourceUrl`, `status`
- `data/fx/latest.json`: Full JSON payload + `rate`, `timestampISO`, `ageMinutes`

## How to Re-Run a Fetch Manually
```bash
python3 lib/fetcher.py \
  --url https://api.exchangerate-api.com/v4/latest/USD \
  --cache-ttl 1800 \
  --output data/fx/latest.json
```

## How to Check Freshness
```bash
# Show latest FX rate and age
jq '.rate, .ageMinutes' data/fx/latest.json

# Show last 5 audit log entries
tail -5 data/audit/log.csv
```

---
✅ All logs are human-readable, machine-parsable, and ready for export to your SIEM or compliance platform.