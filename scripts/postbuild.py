import sys,re
p=sys.argv[1]+'/index.html'
s=open(p).read()
if '__psychBoot' in s: sys.exit(0)
boot='''<script>
window.__vfsPersist = {};
function __psychBoot(go) {
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
