import time
from playwright.sync_api import sync_playwright
def press(pg,k,w=2.5):
    pg.keyboard.down(k); time.sleep(0.15); pg.keyboard.up(k); time.sleep(w)
JS="()=>Howler._howls.filter(h=>h._sounds.some(s=>!s._paused&&!s._ended)).map(h=>String(h._src).slice(-12)+' dur='+h.duration().toFixed(0)+' sounds='+JSON.stringify(h._sounds.map(s=>[s._id,s._paused,s._ended,s._loop,s._volume])))"
def st(pg,t):
    print(t, pg.evaluate(JS))
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--autoplay-policy=no-user-gesture-required'])
    pg=b.new_page(viewport={'width':1280,'height':720})
    pg.goto('http://localhost:8123/index.html'); time.sleep(14); pg.mouse.click(640,360)
    press(pg,'Escape',10); press(pg,'Enter',8); press(pg,'Enter',8); time.sleep(3); st(pg,'main')
    press(pg,'ArrowDown',1); press(pg,'Enter',25); st(pg,'freeplay')
    press(pg,'f',2); pg.keyboard.type('bopeebo',delay=120); time.sleep(2); press(pg,'Enter',3); st(pg,'selected')
    press(pg,'Enter',40); st(pg,'ingame+40s')
    press(pg,'Enter',6); st(pg,'paused')
    time.sleep(6); st(pg,'paused+6')
    press(pg,'Enter',8); st(pg,'resumed')
    press(pg,'Enter',6); st(pg,'paused2')
    pg.keyboard.press('ArrowDown'); press(pg,'ArrowDown',1); press(pg,'ArrowDown',1); press(pg,'Enter',10); st(pg,'exit-to-menu')
    time.sleep(10); st(pg,'exit+10')
    b.close()
