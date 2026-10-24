import time,glob,os
from playwright.sync_api import sync_playwright
B='/home/claude/psych/work/export/release/html5/bin'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required','--use-gl=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720})
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)[:150])); pg.on('console',lambda m:errs.append(m.text[:150]) if m.type=='error' else None)
    pg.goto('file://'+B+'/index.html'); time.sleep(2)
    with pg.expect_file_chooser() as fc:
        pg.click('button[data-hidden="0"][data-mods="0"]')
    fc.value.set_files(B)
    time.sleep(60)
    pg.screenshot(path='/tmp/claude-0/file1.png')
    print(errs[:8])
    b.close()
