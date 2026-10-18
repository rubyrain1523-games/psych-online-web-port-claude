import time
from playwright.sync_api import sync_playwright
def press(pg,k,w=2.5):
    pg.keyboard.down(k); time.sleep(0.15); pg.keyboard.up(k); time.sleep(w)
JS="()=>{try{return (typeof Howler!=='undefined'?Howler._howls:[]).filter(h=>!String(h._src).includes('?')).map(h=>[String(h._src).slice(-30),h.state(),h.playing()])}catch(e){return String(e)}}"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--autoplay-policy=no-user-gesture-required'])
    pg=b.new_page(viewport={'width':1280,'height':720}); logs=[]
    pg.on('console',lambda m: logs.append(m.text)); pg.on('pageerror',lambda e: logs.append('PAGEERROR '+str(e)[:400]))
    pg.goto('http://localhost:8123/index.html'); time.sleep(14); pg.mouse.click(640,360)
    for t in ['title']:
        print(t, pg.evaluate(JS))
    press(pg,'Escape',10); print('after esc',pg.evaluate(JS))
    press(pg,'Enter',8); print('after enter1',pg.evaluate(JS))
    press(pg,'Enter',8); time.sleep(3); print('main menu',pg.evaluate(JS))
    for l in logs:
        if any(x in l for x in ['usic','ound','PAGEERROR','udio']): print(l[:300])
    b.close()
