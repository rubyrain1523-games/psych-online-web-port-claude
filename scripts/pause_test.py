import time
from playwright.sync_api import sync_playwright
def press(pg,k,w=2.5):
    pg.keyboard.down(k); time.sleep(0.15); pg.keyboard.up(k); time.sleep(w)
HOOK="""()=>{window.__ev=[];const H=Howl.prototype;for(const m of ['play','stop','pause']){const o=H[m];H[m]=function(id){const r=o.apply(this,arguments);try{const st=(new Error().stack||'').split('\\n').slice(2,8).map(l=>l.trim().replace(/\\(.*\\//,'(').replace(/PsychOnline.js\\?v=\\d+:/,'').slice(0,50)).join(' < ');window.__ev.push([m,String(this._src).slice(-6),m==='play'?r:id,this._state,st]);}catch(e){}return r;}}}"""
ST="()=>Howler._howls.filter(h=>h._sounds.some(s=>!s._paused&&!s._ended)).map(h=>String(h._src).slice(-6)+' '+JSON.stringify(h._sounds.filter(s=>!s._paused&&!s._ended).map(s=>[s._id,Math.round(h.seek(s._id)*10)/10])))"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--autoplay-policy=no-user-gesture-required'])
    pg=b.new_context(viewport={'width':1280,'height':720}).new_page()
    pg.goto('http://localhost:8123/index.html?launch=vanilla'); time.sleep(14); pg.mouse.click(640,360)
    pg.evaluate(HOOK)
    press(pg,'Escape',10); press(pg,'Enter',8); press(pg,'Enter',8); time.sleep(3)
    press(pg,'ArrowDown',1); press(pg,'Enter',25)
    press(pg,'f',2); pg.keyboard.type('bopeebo',delay=120); time.sleep(2); press(pg,'Enter',3)
    press(pg,'Enter',5)
    for _ in range(60):
        r=pg.evaluate(ST)
        if len(r)>=2 and all(float(x.split(',')[-1].strip(']'))>4 for x in [y.replace(']]','') for y in r][:1]): break
        pg.evaluate('1'); time.sleep(3)
    print('playing', pg.evaluate(ST))
    pg.evaluate("window.__ev=[]")
    press(pg,'Escape',6); print('after pause', pg.evaluate(ST))
    for e in pg.evaluate("window.__ev"): print(e[0],e[1],e[2],e[3],e[4][:200])
    time.sleep(5); print('pause+5', pg.evaluate(ST))
    pg.evaluate("window.__ev=[]")
    press(pg,'Enter',30); time.sleep(6); print('resumed', pg.evaluate(ST))
    for e in pg.evaluate("window.__ev"): print(e[0],e[1],e[2],e[3],e[4][:200])
    b.close()
