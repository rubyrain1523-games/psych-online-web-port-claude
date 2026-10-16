# usage: fp_test.py <search> [downs_before_enter] [play_wait] [tag]
import sys, time
from playwright.sync_api import sync_playwright
q=sys.argv[1]; downs=int(sys.argv[2]) if len(sys.argv)>2 else 0; wait=float(sys.argv[3]) if len(sys.argv)>3 else 25; tag=sys.argv[4] if len(sys.argv)>4 else 'fp'
rights=int(sys.argv[5]) if len(sys.argv)>5 else 0
URL='http://localhost:8123/index.html'
def press(pg,k,w=0.8):
    pg.keyboard.down(k); time.sleep(0.15); pg.keyboard.up(k); time.sleep(w)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--autoplay-policy=no-user-gesture-required'])
    pg = b.new_page(viewport={'width':1280,'height':720}); logs=[]
    pg.on('console', lambda m: logs.append(m.text)); pg.on('pageerror', lambda e: logs.append('PAGEERROR '+str(e)[:400]))
    pg.goto(URL); time.sleep(14); pg.mouse.click(640,360)
    import os
    if os.environ.get('PSET'):
        for kv in os.environ['PSET'].split(','):
            k,v=kv.split('='); pg.evaluate('([k,v])=>window.psychSetting(k,v)',[k,v])
    press(pg,'Escape',10); press(pg,'Enter',8); press(pg,'Enter',8)
    time.sleep(4); pg.screenshot(path='/home/claude/psych/'+tag+'0.png'); press(pg,'ArrowDown',1); press(pg,'Enter',25)
    press(pg,'f',2); pg.keyboard.type(q,delay=120); time.sleep(2)
    press(pg,'Enter',3)
    for _ in range(downs): press(pg,'ArrowDown',0.6)
    for _ in range(rights): press(pg,'ArrowRight',0.8)
    pg.screenshot(path=f'/home/claude/psych/{tag}1.png')
    press(pg,'Enter',wait); pg.screenshot(path=f'/home/claude/psych/{tag}2.png')
    time.sleep(8); pg.screenshot(path=f'/home/claude/psych/{tag}3.png')
    for l in logs:
        if 'GL Driver' in l or 'Canvas2D' in l or '_volume' in l or l.startswith('Called'): continue
        print(l[:3000].replace('\n',' | '))
    b.close()
