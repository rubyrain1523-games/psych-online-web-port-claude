import time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--autoplay-policy=no-user-gesture-required'])
    ctx=b.new_context(viewport={'width':1280,'height':720})
    pg=ctx.new_page(); logs=[]
    pg.on('console',lambda m: logs.append(m.text)); pg.on('pageerror',lambda e: logs.append('PAGEERROR '+str(e)[:300]))
    pg.goto('http://localhost:8123/index.html'); time.sleep(3)
    pg.screenshot(path='/home/claude/psych/L0.png')
    print('mods flag before', pg.evaluate('window.__psychModsEnabled'), 'game script loaded:', pg.evaluate("typeof lime"))
    # hidden modded
    with ctx.expect_page() as ev:
        pg.click('button[data-hidden="1"][data-mods="1"]')
    w=ev.value; print('popup url', w.url)
    time.sleep(25)
    fr=[f for f in w.frames if 'launch=modded' in f.url]
    print('iframe', [f.url for f in w.frames])
    if fr: print('mods flag in iframe', fr[0].evaluate('window.__psychModsEnabled'), 'canvas', fr[0].evaluate("!!document.querySelector('canvas')"))
    w.screenshot(path='/home/claude/psych/L1.png')
    # normal vanilla in same tab
    pg.click('button[data-hidden="0"][data-mods="0"]'); time.sleep(25)
    print('normal vanilla mods flag', pg.evaluate('window.__psychModsEnabled'), 'canvas', pg.evaluate("!!document.querySelector('canvas')"))
    pg.screenshot(path='/home/claude/psych/L2.png')
    for l in logs:
        if 'PAGEERROR' in l or 'CRASH' in l: print(l[:300])
    b.close()
