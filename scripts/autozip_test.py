import time
from playwright.sync_api import sync_playwright
URL='http://localhost:8140/PsychOnline-Web/index.html'
def idb(pg): return pg.evaluate("""() => new Promise(r => { const out=[]; const c=window.__vfsDb.transaction('files','readonly').objectStore('files').openCursor(); c.onsuccess=e=>{const cur=e.target.result; if(cur){out.push(cur.key); cur.continue();} else r(out);} })""")
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader'])
    ctx=b.new_context(viewport={'width':1280,'height':720})
    for n in (1,2):
        pg=ctx.new_page(); logs=[]
        pg.on('console',lambda m: logs.append(m.text)); pg.on('pageerror',lambda e: logs.append('PAGEERROR '+str(e)[:300]))
        pg.goto(URL); time.sleep(16)
        print('boot',n,[k for k in idb(pg) if 'hello' in k][:3], [l[:120] for l in logs if 'boot mod' in l or 'PAGEERROR' in l or 'failed' in l])
        pg.screenshot(path=f'/home/claude/psych/az{n}.png'); pg.close()
    b.close()
