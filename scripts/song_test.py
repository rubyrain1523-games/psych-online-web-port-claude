import sys, time
from playwright.sync_api import sync_playwright
term=sys.argv[1]; tag=sys.argv[2]; wait=int(sys.argv[3]) if len(sys.argv)>3 else 30
rights=int(sys.argv[4]) if len(sys.argv)>4 else 0
URL='http://localhost:8123/index.html'
def press(pg,k,w=0.8):
    pg.keyboard.down(k); time.sleep(0.15); pg.keyboard.up(k); time.sleep(w)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--autoplay-policy=no-user-gesture-required'])
    pg = b.new_context(viewport={'width':1280,'height':720}).new_page(); logs=[]
    pg.on('console', lambda m: logs.append(m.text)); pg.on('pageerror', lambda e: logs.append('PAGEERROR '+str(e)[:400]))
    pg.goto(URL); time.sleep(14); pg.mouse.click(640,360)
    press(pg,'Escape',10); press(pg,'Enter',8); press(pg,'Enter',8)
    press(pg,'ArrowDown',1); press(pg,'Enter',25)
    press(pg,'f',2); pg.keyboard.type(term,delay=120); time.sleep(2)
    pg.screenshot(path=f'/home/claude/psych/{tag}_a.png')
    press(pg,'Enter',3)
    for _ in range(rights): press(pg,'ArrowRight',0.6)
    pg.screenshot(path=f'/home/claude/psych/{tag}_d.png')
    press(pg,'Enter',wait)
    pg.screenshot(path=f'/home/claude/psych/{tag}_b.png')
    time.sleep(10); pg.screenshot(path=f'/home/claude/psych/{tag}_c.png')
    for l in logs:
        if 'GL Driver' in l or '_volume' in l or l.startswith('Called') or 'Canvas2D' in l or 'Achievement' in l: continue
        print(l[:350].replace('\n',' | '))
    b.close()
