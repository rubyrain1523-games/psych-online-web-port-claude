import time,glob
from playwright.sync_api import sync_playwright
z=(glob.glob('/home/claude/psych/rel/PsychOnline-Web/dlmod.zip')+glob.glob('/home/claude/psych/dlmod.zip')+glob.glob('/tmp/dlmod.zip'))[0]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); logs=[]
    pg.on('console',lambda m: logs.append(m.text)); pg.on('pageerror',lambda e: logs.append('PAGEERROR '+str(e)[:300]))
    pg.goto('http://localhost:8123/index.html?launch=modded'); time.sleep(25)
    print('button', pg.evaluate("[...document.querySelectorAll('button')].map(b=>b.textContent)"))
    pg.set_input_files('input[type=file]', z)
    for _ in range(8): pg.evaluate('1'); time.sleep(3)
    pg.screenshot(path='/home/claude/psych/I1.png')
    for l in logs:
        if any(k in l for k in ['dlmod','Regular mod','importZip','PAGEERROR']): print(l[:200])
    b.close()
    b=None
