import time,json
from playwright.sync_api import sync_playwright
def press(pg,k,w=2.5):
    pg.keyboard.down(k); time.sleep(0.15); pg.keyboard.up(k); time.sleep(w)
HOOK="""()=>{window.__ev=[];const H=Howl.prototype;for(const m of ['play','stop','pause']){const o=H[m];H[m]=function(id){const r=o.apply(this,arguments);try{const st=(new Error().stack||'').split('\\n').slice(2,9).map(l=>l.trim().replace(/\\(.*\\//,'(').slice(0,60)).join(' < ');window.__ev.push([m,String(this._src).slice(-8),m==='play'?r:id,st]);}catch(e){}return r;}}}"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--autoplay-policy=no-user-gesture-required'])
    pg=b.new_page(viewport={'width':1280,'height':720})
    pg.goto('http://localhost:8123/index.html'); time.sleep(14); pg.mouse.click(640,360)
    pg.evaluate(HOOK)
    press(pg,'Escape',10); press(pg,'Enter',8); press(pg,'Enter',8); time.sleep(3)
    press(pg,'ArrowDown',1); press(pg,'Enter',25)
    press(pg,'f',2); pg.keyboard.type('bopeebo',delay=120); time.sleep(2); press(pg,'Enter',3)
    pg.evaluate("window.__ev=[]")
    press(pg,'Enter',45)
    ev=pg.evaluate("window.__ev"); print('--- song start events')
    for e in ev: print(e[0],e[1],e[2],e[3][:230])
    b.close()
