import time,zipfile,json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1100,'height':800},accept_downloads=True)
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
    pg.goto('http://localhost:8123/index.html'); time.sleep(1)
    pg.click('#psych-mm'); pg.set_input_files('#mm-inst','/tmp/claude-0/t.wav'); time.sleep(1)
    pg.fill('#mm-name','Test Song')
    pg.click('#mm-beats')
    box=pg.locator('#mm-cv').bounding_box()
    pg.mouse.click(box['x']+56+23,box['y']+10); pg.mouse.move(box['x']+56+23*7,box['y']+60)
    pg.screenshot(path='/tmp/claude-0/mm1.png')
    pg.click('.tabs button[data-t=out]')
    with pg.expect_download() as d: pg.click('#mm-dl')
    d.value.save_as('/tmp/claude-0/out.zip')
    z=zipfile.ZipFile('/tmp/claude-0/out.zip'); print(z.testzip(), z.namelist())
    c=json.loads(z.read('test-song/data/test-song/test-song.json')); print(len(c['song']['notes']), c['song']['notes'][0]['sectionNotes'][:3], c['song']['notes'][1]['sectionNotes'][:2])
    print(errs); b.close()
