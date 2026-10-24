// Runtime cache: once visited online, the game also loads offline.
const C='psych-v1';
self.addEventListener('install',e=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{
  const r=e.request; if(r.method!=='GET'||!r.url.startsWith(self.location.origin)) return;
  e.respondWith(fetch(r).then(res=>{ if(res.ok){const c=res.clone(); caches.open(C).then(k=>k.put(r,c));} return res; })
    .catch(()=>caches.match(r,{ignoreSearch:true})));
});
