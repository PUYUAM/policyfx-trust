# 🚀 Policy+FX Trust Layer

> Real-time央行政策 + USD/CNY + Shanghai Composite monitoring for Shenzhen financial firms — **audit-ready, embeddable, zero maintenance**.

[![Deploy to GitHub](https://github.com/staticman-dot-net/badge.svg)](https://github.com/new?template_name=policyfx-trust&template_owner=PUYUAM)

![GitHub Pages](https://img.shields.io/website?label=Demo&url=https%3A%2F%2FPUYUAM.github.io%2Fpolicyfx-trust)
![License](https://img.shields.io/github/license/PUYUAM/policyfx-trust)
![Last Commit](https://img.shields.io/github/last-commit/PUYUAM/policyfx-trust)

---

## ✨ Why This Exists
For banks, wealth managers, and外贸 firms in Shenzhen who need *real-time, compliant, embeddable* policy + FX vigilance — **without Wind, Bloomberg, or AI hallucination**.

| Traditional Tools | Policy+FX Trust Layer |
|-------------------|------------------------|
| ❌ $50k+/yr per seat | ✅ **$0 — free, open, MIT licensed** |
| ❌ Heavy desktop apps | ✅ **Embed in <60 seconds**: `<iframe>` or Docker |
| ❌ No source links, no audit trail | ✅ **Every number shows source + timestamp + age** |
| ❌ Breaks when RSS dies | ✅ **Resilient**: auto-retry, cache fallback, Telegram alerts |

## 📊 What’s Included
- 🟢 **Live dashboard**: Red/green/yellow signal using *your exact A股 framework* (PBOC cuts + USD/CNY thresholds)  
- 📈 **Three live data feeds**: PBOC News, USD/CNY Spot, Shanghai Composite chart  
- 🛡️ **Compliance pack**: Data sources, audit log (`data/audit/log.csv`), embedding guide  
- ⚙️ **Zero maintenance**: Cron auto-checks every 30 min; alerts if anything breaks  

## 🚀 Quickstart
### Option 1: Live Demo (GitHub Pages)
👉 Your live dashboard will be at: `https://PUYUAM.github.io/policyfx-trust` *(enable in <30 seconds — see below)*

#### 🔧 How to Enable GitHub Pages
1. Go to your repo: [https://github.com/PUYUAM/policyfx-trust](https://github.com/PUYUAM/policyfx-trust)
2. Click **Settings** → **Pages**
3. Under "Build and deployment":
   - Source → **Deploy from a branch**
   - Branch → `main` / `ui/` folder
4. Click **Save** → done! 🌐
   → Your site will be live at `https://PUYUAM.github.io/policyfx-trust` in ~30 seconds.

### Option 2: Run Locally
```bash
# Launch dashboard on http://localhost:8000
python3 -m http.server 8000 --directory ui/
```

### Option 3: Docker
```bash
docker build -t policyfx-trust . && docker run -p 8080:80 policyfx-trust
```

### Option 4: Embed in Your App
```html
<iframe src="https://PUYUAM.github.io/policyfx-trust" width="800" height="300"></iframe>
```

---

## 📜 License
MIT — free to use, modify, and distribute.

> Built with ❤️ by OpenClaw for Shenzhen.
