import sys,re
p=sys.argv[1]+'/index.html'
s=open(p).read()
if '__psychBoot' in s: sys.exit(0)
boot='''<script>
window.__vfsPersist = {};
function __psychBoot(go0) {
  var go = function() {
    var done = false; var fin = function() { if (!done) { done = true; go0(); } };
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
s=s.replace('</body>', '''<div id="psychImport" style="position:fixed;top:6px;right:6px;z-index:10;font:12px sans-serif">
<label style="background:rgba(0,0,0,.55);color:#fff;padding:5px 9px;border-radius:5px;cursor:pointer;border:1px solid #888">Import mod (.zip)
<input type="file" accept=".zip" style="display:none" onchange="(function(i){var f=i.files[0];if(!f)return;var r=new FileReader();r.onload=function(){window.psychImportZip(f.name,new Uint8Array(r.result));};r.readAsArrayBuffer(f);i.value='';})(this)"></label></div>
''' + '</body>',1)
s=s.replace('<script type="text/javascript" src="./PsychOnline.js"></script>', boot+'<script type="text/javascript" src="./PsychOnline.js"></script>',1)
s=re.sub(r'lime\.embed \("PsychOnline", "openfl-content", 1280, 720, \{ parameters: \{\} \}\);', '__psychBoot(function() { lime.embed ("PsychOnline", "openfl-content", 1280, 720, { parameters: {} }); });', s)
open(p,'w').write(s)
