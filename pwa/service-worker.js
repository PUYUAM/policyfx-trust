// pwa/service-worker.js
const CACHE_NAME = 'policyfx-v0.1.7';
const urlsToCache = [
  '/ui/index.html',
  '/ui/trends/usd-cny-7d.svg',
  '/ui/trends/shcomp-7d.svg',
  '/lib/analytics.js',
  '/data/fx/latest.json',
  '/data/policy/latest.json',
  '/data/shanghai/latest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});