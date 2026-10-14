import time, zipfile
from playwright.sync_api import sync_playwright
URL='http://localhost:8123/index.html'
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader'])
    pg = b.new_context().new_page(); pg.goto(URL); time.sleep(14)
    pg.evaluate("window.psychDownloadMod('http://localhost:8123/dlmod.zip')"); time.sleep(10)
    sizes = pg.evaluate("""() => new Promise(r => { const out={}; const c=window.__vfsDb.transaction('files','readonly').objectStore('files').openCursor(); c.onsuccess=e=>{const cur=e.target.result; if(cur){out[cur.key]=cur.value.byteLength; cur.continue();} else r(out);} })""")
    z = zipfile.ZipFile('/home/claude/psych/dlmod.zip')
    for i in z.infolist():
        k='mods/'+i.filename
        print(i.filename, 'zip', i.file_size, 'idb', sizes.get(k))
    b.close()
