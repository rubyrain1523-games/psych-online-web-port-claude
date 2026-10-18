import time
from playwright.sync_api import sync_playwright
zipb=open('work/export/release/html5/bin/dlmod.zip','rb').read()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); logs=[]
    pg.on('console',lambda m: logs.append(m.text)); pg.on('pageerror',lambda e: logs.append('PAGEERROR '+str(e)[:300]))
    pg.route('https://example-mods.test/**',lambda r: r.abort())
    pg.route('https://corsproxy.io/**',lambda r: r.fulfill(status=200,headers={'access-control-allow-origin':'*','content-type':'application/zip'},body=zipb))
    pg.goto('http://localhost:8123/index.html'); time.sleep(20); pg.mouse.click(640,360); time.sleep(15)
    pg.evaluate("window.psychDownloadMod('https://example-mods.test/dl/cool.zip')"); [ (pg.evaluate('1'), time.sleep(3)) for _ in range(12)]
    for l in logs:
        if 'GL Driver' not in l and 'DBG' not in l and 'Font' not in l: print(l[:400])
    b.close()
