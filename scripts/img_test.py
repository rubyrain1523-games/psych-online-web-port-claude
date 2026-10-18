import time
from playwright.sync_api import sync_playwright
def press(pg,k,w=0.8):
    pg.keyboard.down(k); time.sleep(0.15); pg.keyboard.up(k); time.sleep(w)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader'])
    ctx=b.new_context(viewport={'width':1280,'height':720})
    pg=ctx.new_page(); pg.goto('http://localhost:8123/index.html'); time.sleep(14)
    pg.evaluate("window.psychDownloadMod('http://localhost:8123/imgmod.zip')")
    for _ in range(8): pg.evaluate('1'); time.sleep(3)
    pg.close()
    pg=ctx.new_page(); logs=[]
    pg.on('console',lambda m: logs.append(m.text)); pg.on('pageerror',lambda e: logs.append('PAGEERROR '+str(e)[:300]))
    pg.goto('http://localhost:8123/index.html'); time.sleep(14); pg.mouse.click(640,360)
    press(pg,'Escape',10); press(pg,'Enter',8); press(pg,'Enter',8); time.sleep(3)
    pg.screenshot(path='/home/claude/psych/img1.png')
    for l in logs:
        if any(x in l for x in ['WebImage','PAGEERROR','imgmod']): print(l[:300])
    b.close()
