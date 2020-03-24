var staticCacheName = 'django-pwa-v';

var filesToCache = [
    '/rango',
    '/rango/about',
    '/rango/profiles',
    '/static/css/admin.css',
    '/static/css/bulma.css',
    '/static/css/font-awesome-min.css',
    '/static/img/rango-logo.png',
    '/static/img/splash-640x1136.png',
    '/static/js/bulma.js',
    '/static/js/rango-ajax.js',
    '/static/js/rango-jquery.js',
];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from Cache
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request);
            })
            .catch(() => {
                return caches.match('rango/base');
            })
    )
});