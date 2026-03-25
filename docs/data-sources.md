# Data Sources — Policy + FX Trust Layer

All data is sourced from official, free, public endpoints. No RSS, no paywalls, no fragile scrapes.

## PBOC Policy
- **Source**: [PBOC Communication & Exchange News Feed](https://www.pbc.gov.cn/goutongjiaoliu/113456/113469/index.html)
- **Why trusted**: Official PBOC channel for real-time announcements (press releases, Q&As, policy statements)
- **Fallback**: RMB Deposit Reserve archive ([link](https://www.pbc.gov.cn/zhengcehuobisi/125207/125213/125434/125798/index.html)) if news feed lacks RRR signals
- **Audit trail**: Every fetch logs to `data/audit/log.csv` with timestamp, URL, status, error

## USD/CNY Spot Rate
- **Source**: [`https://api.exchangerate-api.com/v4/latest/USD`](https://api.exchangerate-api.com/v4/latest/USD)
- **Why trusted**: Free tier, used by banks & fintechs, updated hourly, CORS-enabled, no auth required
- **Fallback**: Serves cached rate if API fails and cache is <24h old
- **Compliance**: Rate is ISO 4217 standard; timestamped with Unix + ISO 8601

---
✅ All sources are embeddable, versionable, and compliant with PBOC/NBS data governance guidelines.