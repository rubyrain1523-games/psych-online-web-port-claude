import time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); logs=[]
    pg.on('console',lambda m: logs.append(m.text)); pg.on('pageerror',lambda e: logs.append('PAGEERROR '+str(e)[:300]))
    pg.goto('http://localhost:8123/index.html?launch=modded'); time.sleep(25)
    print([x for x in pg.evaluate("[...document.querySelectorAll('button')].map(b=>b.textContent)")])
    pg.set_input_files('input[type=file]', '/tmp/claude-0/out.zip')
    for _ in range(8): pg.evaluate('1'); time.sleep(3)
    for l in logs:
        if any(k in l.lower() for k in ['test-song','regular mod','importzip','pageerror']): print(l[:200])
    b.close()
