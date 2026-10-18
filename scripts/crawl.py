import time,sys
from playwright.sync_api import sync_playwright
def press(pg,k,w=2.5):
    pg.keyboard.down(k); time.sleep(0.15); pg.keyboard.up(k); time.sleep(w)
plans={ # name: keys after reaching main menu
 'story':['Enter'],
 'online':['ArrowDown','ArrowDown','Enter'],
 'options':['ArrowDown','ArrowDown','ArrowDown','Enter'],
 'awards':['ArrowDown','ArrowDown','ArrowDown','ArrowDown','Enter'],
 'credits':['ArrowDown','ArrowDown','ArrowDown','ArrowDown','ArrowDown','Enter'],
}
which=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); logs=[]
    pg.on('console',lambda m: logs.append(m.text)); pg.on('pageerror',lambda e: logs.append('PAGEERROR '+str(e)[:400]))
    pg.goto('http://localhost:8123/index.html'); time.sleep(14); pg.mouse.click(640,360)
    press(pg,'Escape',10); press(pg,'Enter',8); press(pg,'Enter',8); time.sleep(3)
    for k in plans[which]: press(pg,k,1.5 if k=='ArrowDown' else 12)
    pg.screenshot(path=f'/home/claude/psych/c_{which}.png')
    for extra in sys.argv[2:]:
        press(pg,extra,2); 
    pg.screenshot(path=f'/home/claude/psych/c_{which}_2.png')
    for l in logs:
        if any(x in l for x in ['CRASH','PAGEERROR','rror','Called from']) and 'CORS' not in l: print(l[:500].replace('\n',' | '))
    b.close()
