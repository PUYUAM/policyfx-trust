# 📊 Analytics — Privacy-First Design

Policy+FX Trust Layer includes *opt-in, self-hosted, zero-external-analytics* — built for Shenzhen’s data sovereignty requirements.

## ✅ What’s Tracked (Only If Enabled)
| Metric | How It’s Collected | Stored |
|--------|---------------------|--------|
| `dashboard_views` | Incremented on each `ui/index.html` page load | `data/analytics/YYYY-MM-DD.json` |
| `fx_alerts` | Incremented when `alerts/fx-red-alert-telegram.py` sends an alert | Same file |
| `shcomp_alerts` | Incremented when `alerts/shcomp-breach-alert.py` sends an alert | Same file |

**No PII. No IP. No cookies. No external domains.**

## 🔧 How to Enable
1. Open `ui/index.html` 
2. Change `const ANALYTICS_ENABLED = false;` → `true`
3. Save & reload

## 📥 How to Export Logs
```bash
# Export today's analytics
cat data/analytics/$(date +%Y-%m-%d).json

# Export all logs as CSV
echo 'date,views,fx_alerts,shcomp_alerts' > analytics.csv && \
  for f in data/analytics/*.json; do 
    d=$(basename $f .json); 
    v=$(jq -r '.dashboard_views // 0' $f); 
    fx=$(jq -r '.fx_alerts // 0' $f); 
    s=$(jq -r '.shcomp_alerts // 0' $f); 
    echo "$d,$v,$fx,$s";
  done >> analytics.csv
```

---
🔒 All data stays on your infrastructure. You own it — always.