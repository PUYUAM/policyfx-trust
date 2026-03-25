# Embedding Guide — How to Put This in Your App

This dashboard is built for zero-friction embedding into internal systems.

## Option 1: Iframe (Simplest)
```html
<iframe 
  src="/ui/index.html" 
  width="800" 
  height="300" 
  frameborder="0">
</iframe>
```
- Works in any web portal, CRM, or internal dashboard
- Auto-refreshes every 30 minutes (cron-driven)
- Responsive & mobile-friendly

## Option 2: API Integration
All data is JSON:
- Policy: `GET /data/policy/latest.json`
- FX: `GET /data/fx/latest.json`
- Status logic is open (see `ui/index.html` → `renderStatus()` function)

## Option 3: Self-Hosted Standalone
Copy the entire `ui/`, `data/`, `lib/` folders to your server. No backend required.

---
✅ Watermark and source links are baked in — no risk of misattribution.
✅ All files are static — no cookies, no tracking, no external calls after load.