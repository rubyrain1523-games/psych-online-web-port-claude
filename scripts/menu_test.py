# usage: menu_test.py "<keys comma list>" tag   e.g. "ArrowDown,ArrowDown,Enter"
import sys, time
from playwright.sync_api import sync_playwright
keys=sys.argv[1].split(','); tag=sys.argv[2]
URL='http://localhost:8123/index.html'
def press(pg,k,w=1.2):
    pg.keyboard.down(k); time.sleep(0.15); pg.keyboard.up(k); time.sleep(w)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--autoplay-policy=no-user-gesture-required'])
    pg = b.new_page(viewport={'width':1280,'height':720}); logs=[]
    pg.on('console', lambda m: logs.append(m.text)); pg.on('pageerror', lambda e: logs.append('PAGEERROR '+str(e)[:600]))
    pg.add_init_script("window.addEventListener('error', ev => { try { var e=ev.error; console.log('ERRDETAIL ' + (e && e.value !== undefined ? ('value=' + String(e.value).slice(0,3500)) : '') + ' stack=' + (e && e.stack ? e.stack.slice(0,700) : '')); } catch(x){} });")
    pg.goto(URL); time.sleep(14); pg.mouse.click(640,360)
    press(pg,'Escape',10); press(pg,'Enter',8); press(pg,'Enter',8); time.sleep(4)
    n=0
    for k in keys:
        if k.startswith('wait'): time.sleep(float(k[4:])); continue
        if k.startswith('shot'): pg.screenshot(path=f'/home/claude/psych/{tag}_{k[4:]}.png'); continue
        if k.startswith('type'): pg.keyboard.type(k[4:],delay=100); continue
        press(pg,k)
    pg.screenshot(path=f'/home/claude/psych/{tag}_end.png')
    for l in logs:
        if 'GL Driver' in l or 'Canvas2D' in l or '_volume' in l or l.startswith('Called'): continue
        print(l[:4000].replace('\n',' | '))
    b.close()
