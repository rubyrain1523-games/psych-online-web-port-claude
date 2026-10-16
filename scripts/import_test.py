import time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); logs=[]
    pg.on('console',lambda m: logs.append(m.text)); pg.on('pageerror',lambda e: logs.append('PAGEERROR '+str(e)))
    pg.goto('http://localhost:8123/index.html'); time.sleep(14)
    pg.set_input_files('#psychImport input','/home/claude/psych/dlmod.zip'); time.sleep(8)
    pg.screenshot(path='/home/claude/psych/imp.png')
    keys=pg.evaluate("""() => new Promise(r => { const out=[]; const c=window.__vfsDb.transaction('files','readonly').objectStore('files').openCursor(); c.onsuccess=e=>{const cur=e.target.result; if(cur){out.push(cur.key); cur.continue();} else r(out);} })""")
    print(keys)
    for l in logs:
        if 'COPY' in l or 'PAGEERROR' in l or 'rror' in l: print(l[:300])
    b.close()
