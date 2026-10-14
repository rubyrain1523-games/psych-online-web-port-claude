import time
from playwright.sync_api import sync_playwright
URL='http://localhost:8123/index.html'
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader'])
    ctx = b.new_context(viewport={'width':1280,'height':720})
    pg = ctx.new_page(); logs=[]
    pg.on('console', lambda m: logs.append(m.text)); pg.on('pageerror', lambda e: logs.append('PAGEERROR '+str(e)[:300]))
    pg.goto(URL); time.sleep(15)
    print('has helper:', pg.evaluate("typeof window.psychDownloadMod"))
    pg.evaluate("window.psychDownloadMod('http://localhost:8123/dlmod.zip')"); time.sleep(12)
    keys = pg.evaluate("""() => new Promise(r => { const c=window.__vfsDb.transaction('files','readonly').objectStore('files').getAllKeys(); c.onsuccess=()=>r(c.result); })""")
    print('IDB keys after download:', keys[:12], len(keys))
    pg2 = ctx.new_page(); logs2=[]
    pg2.on('pageerror', lambda e: logs2.append('PAGEERROR '+str(e)[:300]))
    pg2.goto(URL); time.sleep(12)
    print('restored in new load:', pg2.evaluate("Object.keys(window.__vfsPersist).length"))
    for l in logs:
        if any(w in l for w in ('PAGEERROR','Error','error','mod','Mod','install','Install')) and 'GL Driver' not in l: print('LOG:', l[:300])
    print(logs2[:3])
    b.close()
