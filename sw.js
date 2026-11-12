// La app funciona sin red, pero la página en sí se pide siempre a la red cuando
// la hay: con caché primero, una versión nueva tardaba dos aperturas en entrar,
// o no entraba. La caché queda como red de seguridad para los tramos sin cobertura.
const CACHE = 'homologacion-v06-23';
const FICHEROS = ['./', './index.html', './manifest.webmanifest', './icon-192.png', './icon-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FICHEROS)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

function esPagina(req){
  return req.mode === 'navigate' || /\/(index\.html)?$/.test(new URL(req.url).pathname);
}

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;

  if (esPagina(e.request)){
    // Red primero, con 4 s de paciencia: si no hay cobertura, se sirve la copia.
    e.respondWith((async () => {
      try {
        const ctl = new AbortController();
        const reloj = setTimeout(() => ctl.abort(), 4000);
        const r = await fetch(e.request, {cache: 'no-store', signal: ctl.signal});
        clearTimeout(reloj);
        const copia = r.clone();
        caches.open(CACHE).then(c => c.put('./index.html', copia)).catch(() => {});
        return r;
      } catch (err) {
        return (await caches.match('./index.html')) || Response.error();
      }
    })());
    return;
  }

  e.respondWith(
    caches.match(e.request, {ignoreSearch: true}).then(hit => hit || fetch(e.request)
      .then(r => { const copia = r.clone();
        caches.open(CACHE).then(c => c.put(e.request, copia)).catch(() => {}); return r; })
      .catch(() => caches.match('./index.html')))
  );
});
