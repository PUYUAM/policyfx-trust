// lib/analytics.js — Privacy-first, self-hosted analytics
// Tracks only: dashboard views, FX alerts sent, SHCOMP alerts sent
// All data stored locally in data/analytics/YYYY-MM-DD.json — no external calls

function getTodayFile() {
  const d = new Date();
  return `data/analytics/${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}.json`;
}

async function incrementCounter(key) {
  const file = getTodayFile();
  try {
    const res = await fetch(file);
    let data = res.ok ? await res.json() : { dashboard_views: 0, fx_alerts: 0, shcomp_alerts: 0 };
    
    if (key in data) {
      data[key] += 1;
      // Write back via simple POST to internal endpoint (handled by OpenClaw's static file server)
      await fetch(file, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
    }
  } catch (e) {
    console.debug('Analytics disabled or write failed:', e);
  }
}

// Export for use in ui/index.html
window.policyfxAnalytics = {
  trackDashboardView: () => incrementCounter('dashboard_views'),
  trackFxAlert: () => incrementCounter('fx_alerts'),
  trackShcompAlert: () => incrementCounter('shcomp_alerts')
};