import sys,re
p=sys.argv[1]+'/index.html'
s=open(p).read()
if '__psychBoot' in s: sys.exit(0)
boot=r'''<script>
window.__vfsPersist = {};
window.__psychZips = [];
// Fetches zipped mods from the repo's top-level "mods" folder (../mods relative to this page) and queues them for install.
function __psychLoadZips(done) {
  var msg = document.createElement('div');
  msg.style.cssText = 'position:fixed;left:8px;bottom:8px;z-index:10;color:#ccc;font:13px monospace;background:rgba(0,0,0,.6);padding:4px 8px;border-radius:4px';
  var finished = false;
  function fin() { if (finished) return; finished = true; if (msg.parentNode) msg.parentNode.removeChild(msg); done(); }
  setTimeout(fin, 120000);
  var seen = {};
  try { seen = JSON.parse(localStorage.getItem('psychAutoMods') || '{}'); } catch (e) {}
  function save() { try { localStorage.setItem('psychAutoMods', JSON.stringify(seen)); } catch (e) {} }
  function list() {
    return fetch('../mods/index.json', { cache: 'no-cache' }).then(function(r) {
      if (!r.ok) throw 0; return r.json();
    }).then(function(j) {
      return j.map(function(x) { return typeof x === 'string' ? { name: x } : x; });
    }).catch(function() {
      var m = location.hostname.match(/^(.+)\.github\.io$/);
      if (!m) return [];
      var repo = location.pathname.split('/')[1];
      return fetch('https://api.github.com/repos/' + m[1] + '/' + repo + '/contents/mods').then(function(r) {
        if (!r.ok) throw 0; return r.json();
      }).then(function(j) {
        return j.filter(function(x) { return x.type === 'file'; }).map(function(x) { return { name: x.name, size: x.size }; });
      }).catch(function() { return []; });
    });
  }
  list().then(function(files) {
    files = files.filter(function(f) { return /\.zip$/i.test(f.name); });
    var chain = Promise.resolve();
    files.forEach(function(f, i) {
      chain = chain.then(function() {
        if (f.size != null && seen[f.name] === f.size) return;
        msg.textContent = 'Loading mod ' + (i + 1) + '/' + files.length + ': ' + f.name;
        document.body.appendChild(msg);
        return fetch('../mods/' + encodeURIComponent(f.name), { cache: 'no-cache' }).then(function(r) {
          if (!r.ok) throw 0; return r.arrayBuffer();
        }).then(function(buf) {
          if (seen[f.name] === buf.byteLength) return;
          window.__psychZips.push({ name: f.name, data: new Uint8Array(buf) });
          seen[f.name] = buf.byteLength; save();
        }).catch(function() {});
      });
    });
    return chain;
  }).then(fin, fin);
}
function __psychBoot(go0) {
  var go = function() {
    var done = false; var fin = function() { if (!done) { done = true; __psychLoadZips(go0); } };
    try { Promise.all(Array.from(document.fonts).map(function(f) { return f.load().catch(function() {}); })).then(fin); setTimeout(fin, 8000); } catch (e) { fin(); }
  };
  try {
    var req = indexedDB.open('psychonline-vfs', 1);
    req.onupgradeneeded = function(e) { e.target.result.createObjectStore('files'); };
    req.onerror = function() { go(); };
    req.onsuccess = function(e) {
      var db = e.target.result; window.__vfsDb = db;
      var c = db.transaction('files', 'readonly').objectStore('files').openCursor();
      c.onsuccess = function(ev) { var cur = ev.target.result; if (cur) { window.__vfsPersist[cur.key] = cur.value; cur.continue(); } else go(); };
      c.onerror = function() { go(); };
    };
  } catch (e) { go(); }
}
</script>
'''
s=s.replace('<script type="text/javascript" src="./PsychOnline.js"></script>', boot+'<script type="text/javascript" src="./PsychOnline.js"></script>',1)
s=re.sub(r'lime\.embed \("PsychOnline", "openfl-content", 1280, 720, \{ parameters: \{\} \}\);', '__psychBoot(function() { lime.embed ("PsychOnline", "openfl-content", 1280, 720, { parameters: {} }); });', s)
open(p,'w').write(s)
