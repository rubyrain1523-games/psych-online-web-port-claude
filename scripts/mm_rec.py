import time,json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']); pg=b.new_page(viewport={'width':1366,'height':768})
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)[:200])); pg.on('dialog',lambda d:d.accept())
    pg.goto('http://localhost:8123/index.html'); time.sleep(1); pg.click('#psych-mm')
    pg.set_input_files('#mm-inst','/tmp/claude-0/t.wav'); time.sleep(1.5)
    pg.click('.tabs button[data-t=chart]'); pg.click('#mm-rec')
    pg.click('#mm-k0'); pg.keyboard.press('z'); pg.click('#mm-chart .tool:first-child') if False else None
    print(pg.evaluate("[0,1,2,3].map(i=>document.getElementById('mm-k'+i).value)"))
    pg.click('#mm-play'); time.sleep(.5)
    for k in ['z','s',';',"'",'s']:
        pg.keyboard.press(k); time.sleep(.4)
    pg.keyboard.down(';'); time.sleep(1.2); pg.keyboard.up(';')
    pg.click('#mm-play'); time.sleep(.3)
    pg.screenshot(path='/tmp/claude-0/r1.png')
    print(pg.inner_text('#mm-info'), errs); b.close()
