import time,zipfile,json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':600},accept_downloads=True)
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)[:200])); pg.on('dialog',lambda d:d.accept())
    pg.goto('http://localhost:8123/index.html'); time.sleep(1)
    pg.click('#psych-mm'); pg.screenshot(path='/tmp/claude-0/m1.png')
    pg.select_option('#mm-opp','pico'); pg.select_option('#mm-stage','__c'); pg.fill('#mm-stage-c','philly')
    pg.click('.tabs button[data-t=music]')
    cv=pg.locator('#mm-pcv'); bx=cv.bounding_box()
    for tr,rowsel in (('Boyfriend voice',5),('Opponent voice',9)):
        pg.click(f'#mm-tr button:has-text("{tr}")')
        for i in range(6):
            pg.mouse.click(bx['x']+56+22*(i*4)+5, bx['y']+16*(rowsel+i%3)+5)
    pg.click('#mm-tr button:has-text("Drums")')
    for i in range(0,32,4): pg.mouse.click(bx['x']+56+22*i+5, bx['y']+16*2+5)
    pg.screenshot(path='/tmp/claude-0/m2.png')
    pg.click('#mm-use'); time.sleep(4); pg.click('#mm-gen')
    print(pg.inner_text('#mm-minfo'))
    pg.click('.tabs button[data-t=chart]'); time.sleep(.5); pg.screenshot(path='/tmp/claude-0/m3.png')
    pg.click('.tabs button[data-t=out]')
    with pg.expect_download() as d: pg.click('#mm-dl')
    d.value.save_as('/tmp/claude-0/out2.zip'); z=zipfile.ZipFile('/tmp/claude-0/out2.zip'); print(z.testzip(), z.namelist())
    c=json.loads(z.read('my-song/data/my-song/my-song.json'))['song']; print(c['player2'],c['stage'],c['needsVoices'],c['notes'][0]['sectionNotes'][:6])
    print(errs); b.close()
