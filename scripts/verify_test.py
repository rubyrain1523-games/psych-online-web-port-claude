import time
from playwright.sync_api import sync_playwright
def press(pg,k,w=0.8):
    pg.keyboard.down(k); time.sleep(0.15); pg.keyboard.up(k); time.sleep(w)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); logs=[]
    pg.on('console',lambda m: logs.append(m.text)); pg.on('pageerror',lambda e: logs.append('PAGEERROR '+str(e)[:300]))
    pg.add_init_script("window.addEventListener('error', ev => { try { var e=ev.error; console.log('ERRDETAIL ' + (e && e.value !== undefined ? String(e.value).slice(0,800) : '') + ' stack=' + (e && e.stack ? e.stack.slice(0,900) : '')); } catch(x){} });")
    pg.goto('http://localhost:8123/index.html'); time.sleep(14); pg.mouse.click(640,360)
    press(pg,'Escape',10); press(pg,'Enter',8); press(pg,'Enter',8); time.sleep(3)
    pg.evaluate('window.psychOpenVerify()'); time.sleep(3)
    pg.screenshot(path='/home/claude/psych/vc1.png')
    pg.keyboard.type('ab12',delay=250); time.sleep(2)
    pg.screenshot(path='/home/claude/psych/vc2.png')
    press(pg,'Enter',3)
    pg.screenshot(path='/home/claude/psych/vc3.png')
    for l in logs:
        if 'GL Driver' in l or 'Canvas2D' in l or 'TitleState' in l: continue
        print(l[:1500].replace('\n',' | '))
    b.close()
