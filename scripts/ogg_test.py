import time
from playwright.sync_api import sync_playwright
def press(pg,k,w=2.5):
    pg.keyboard.down(k); time.sleep(0.15); pg.keyboard.up(k); time.sleep(w)
JS="()=>Howler._howls.filter(h=>h._sounds.some(s=>!s._paused&&!s._ended)).map(h=>'dur='+h.duration().toFixed(0)+' src='+String(h._src).slice(0,14))"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--autoplay-policy=no-user-gesture-required'])
    ctx=b.new_context(viewport={'width':1280,'height':720})
    pg=ctx.new_page(); pg.goto('http://localhost:8123/index.html?launch=modded'); time.sleep(22)
    pg.set_input_files('input[type=file]','/tmp/oggmod.zip')
    for _ in range(8): pg.evaluate('1'); time.sleep(3)
    pg.close()
    pg=ctx.new_page(); logs=[]
    pg.on('console',lambda m: logs.append(m.text)); pg.on('pageerror',lambda e: logs.append('PAGEERROR '+str(e)[:300]))
    pg.goto('http://localhost:8123/index.html?launch=modded'); time.sleep(20); pg.mouse.click(640,360)
    press(pg,'Escape',10); press(pg,'Enter',8); press(pg,'Enter',8)
    press(pg,'ArrowDown',1); press(pg,'Enter',25)
    press(pg,'f',2); pg.keyboard.type('testsong',delay=120); time.sleep(2); press(pg,'Enter',3)
    press(pg,'Enter',3)
    for i in range(6):
        time.sleep(8); print(i*8+8, pg.evaluate(JS))
    pg.screenshot(path='/home/claude/psych/og1.png')
    for l in logs:
        if any(k in l for k in ['DBGINST','VOICES','PAGEERR','oggmod']): print(l[:200])
    b.close()
