import time
from playwright.sync_api import sync_playwright
URL='http://localhost:8123/index.html?launch=modded'
def press(pg,k,w=0.8):
    pg.keyboard.down(k); time.sleep(0.15); pg.keyboard.up(k); time.sleep(w)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--autoplay-policy=no-user-gesture-required'])
    ctx = b.new_context(viewport={'width':1280,'height':720})
    pg = ctx.new_page(); pg.goto(URL); time.sleep(14)
    pg.evaluate("window.psychDownloadMod('http://localhost:8123/dlmod.zip')"); time.sleep(10)
    pg.close()
    pg = ctx.new_page(); logs=[]
    pg.on('console', lambda m: logs.append(m.text)); pg.on('pageerror', lambda e: logs.append('PAGEERROR '+str(e)[:300]))
    pg.goto(URL); time.sleep(14); pg.mouse.click(640,360)
    press(pg,'Escape',10); press(pg,'Enter',8); press(pg,'Enter',8)
    pg.screenshot(path='/home/claude/psych/p0.png')
    press(pg,'ArrowDown',1); press(pg,'Enter',25)
    press(pg,'f',2)
    pg.keyboard.type('testsong',delay=120); time.sleep(2)
    pg.screenshot(path='/home/claude/psych/p1.png')
    press(pg,'Enter',3)
    pg.screenshot(path='/home/claude/psych/p2.png')
    press(pg,'Enter',40); pg.screenshot(path='/home/claude/psych/p3.png')
    press(pg,'Enter',30); pg.screenshot(path='/home/claude/psych/p4.png')
    for l in logs:
        if 'GL Driver' in l or '_volume' in l or l.startswith('Called'): continue
        print(l[:300].replace('\n',' | '))
    b.close()
