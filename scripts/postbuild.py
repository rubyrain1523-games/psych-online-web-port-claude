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
    var done = false; var fin = function() { if (!done) { done = true; if (window.__psychModsEnabled) __psychLoadZips(go0); else go0(); } };
    try { Promise.all(Array.from(document.fonts).map(function(f) { return f.load().catch(function() {}); })).then(fin); setTimeout(fin, 8000); } catch (e) { fin(); }
  };
  try {
    var req = indexedDB.open('psychonline-vfs', 1);
    req.onupgradeneeded = function(e) { e.target.result.createObjectStore('files'); };
    req.onerror = function() { go(); };
    req.onsuccess = function(e) {
      var db = e.target.result; window.__vfsDb = db;
      var c = db.transaction('files', 'readonly').objectStore('files').openCursor();
      c.onsuccess = function(ev) { var cur = ev.target.result; if (cur) { if (window.__psychModsEnabled || (!/^mods\//.test(cur.key) && cur.key !== 'modsList.txt')) window.__vfsPersist[cur.key] = cur.value; cur.continue(); } else go(); };
      c.onerror = function() { go(); };
    };
  } catch (e) { go(); }
}
</script>
'''
launcher=r'''<style>
html,body{touch-action:none;overscroll-behavior:none;-webkit-user-select:none;user-select:none;-webkit-touch-callout:none}
canvas{touch-action:none;outline:none}
#psych-launch{touch-action:pan-y;position:fixed;inset:0;z-index:99999;background:#0b0b10;color:#fff;font-family:system-ui,Segoe UI,Roboto,sans-serif;display:flex;align-items:center;justify-content:center;padding:16px;overflow:auto}
#psych-launch .box{max-width:560px;width:100%}
#psych-launch h1{font-size:24px;margin:0 0 4px}
#psych-launch p{color:#a8a8b8;margin:0 0 18px;font-size:14px}
#psych-launch button{display:block;width:100%;text-align:left;margin:0 0 10px;padding:14px 16px;border-radius:10px;border:1px solid #33334a;background:#16161f;color:#fff;font-size:16px;cursor:pointer}
#psych-launch button:hover,#psych-launch button:focus{border-color:#7b6cff;background:#1d1d2b;outline:none}
#psych-launch button small{display:block;color:#a8a8b8;font-size:12.5px;margin-top:3px}
#psych-launch .note{color:#ffb86b;font-size:13px;min-height:18px;margin-top:6px}
</style>
<div id="psych-launch"><div class="box">
<h1>Friday Night Funkin&#39; Psych Online</h1>
<p>Pick how you want to start the game.</p>
<button data-hidden="0" data-mods="0">Normal &mdash; Vanilla<small>Runs in this tab. No mods.</small></button>
<button data-hidden="0" data-mods="1">Normal &mdash; Modded<small>Runs in this tab. Mods enabled (can be slower to start).</small></button>
<button data-hidden="1" data-mods="0">Hidden &mdash; Vanilla<small>Opens in an about:blank tab so the page address isn&#39;t shown. No mods.</small></button>
<button data-hidden="1" data-mods="1">Hidden &mdash; Modded<small>Opens in an about:blank tab. Mods enabled.</small></button>
<div class="note" id="psych-launch-note"></div>
</div></div>
<script>
(function() {
  var q = new URLSearchParams(location.search);
  var launch = q.get('launch');
  var panel = document.getElementById('psych-launch');
  var note = document.getElementById('psych-launch-note');
  function startGame(mods) {
    window.__psychModsEnabled = !!mods;
    panel.style.display = 'none';
    var sc = document.createElement('script');
    sc.src = './PsychOnline.js?v=__VER__';
    sc.onload = function() { __psychBoot(function() { lime.embed("PsychOnline", "openfl-content", 1280, 720, { parameters: {} }); }); };
    document.head.appendChild(sc);
    if (mods) addImportButton();
  }
  function addImportButton() {
    var inp = document.createElement('input');
    inp.type = 'file'; inp.accept = '.zip'; inp.multiple = true; inp.style.display = 'none';
    var btn = document.createElement('button');
    btn.textContent = 'Import mod (.zip)';
    btn.style.cssText = 'position:fixed;left:8px;bottom:8px;z-index:9999;padding:6px 10px;border-radius:8px;border:1px solid #555;background:rgba(20,20,30,.8);color:#fff;font:13px system-ui,sans-serif;cursor:pointer;opacity:.75';
    btn.onmouseenter = function() { btn.style.opacity = 1; };
    btn.onmouseleave = function() { btn.style.opacity = .75; };
    btn.onclick = function() { inp.click(); };
    inp.onchange = function() {
      Array.prototype.forEach.call(inp.files, function(f) {
        f.arrayBuffer().then(function(buf) {
          if (window.psychImportZip) window.psychImportZip(f.name, new Uint8Array(buf));
          else alert('The game is still loading. Try again in a moment.');
        });
      });
      inp.value = '';
    };
    document.body.appendChild(inp); document.body.appendChild(btn);
  }
  function openHidden(mods) {
    var base = location.href.split('#')[0].split('?')[0];
    var url = base + '?launch=' + (mods ? 'modded' : 'vanilla');
    var w = window.open('about:blank', '_blank');
    if (!w) { note.textContent = 'Your browser blocked the pop-up. Allow pop-ups for this site and try again.'; return; }
    w.document.open();
    w.document.write('<!doctype html><html><head><meta charset="utf-8"><title></title></head><body style="margin:0;background:#000"><iframe src="' + url + '" allow="autoplay; fullscreen; gamepad; clipboard-read; clipboard-write" style="position:fixed;inset:0;width:100%;height:100%;border:0"></iframe></body></html>');
    w.document.close();
    note.textContent = 'Opened in a new about:blank tab. You can close this one.';
  }
  if (launch === 'vanilla' || launch === 'modded') { startGame(launch === 'modded'); return; }
  Array.prototype.forEach.call(panel.querySelectorAll('button'), function(b) {
    b.addEventListener('click', function() {
      var mods = b.getAttribute('data-mods') === '1';
      if (b.getAttribute('data-hidden') === '1') openHidden(mods); else startGame(mods);
    });
  });
})();
</script>
'''.replace('__VER__',str(int(__import__('time').time())))
s=s.replace('<script type="text/javascript" src="./PsychOnline.js"></script>', boot+launcher,1)
s=re.sub(r'lime\.embed \("PsychOnline", "openfl-content", 1280, 720, \{ parameters: \{\} \}\);', '', s)
open(p,'w').write(s)
