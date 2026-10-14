import sys, time
from playwright.sync_api import sync_playwright
url = sys.argv[1]; secs = int(sys.argv[2]) if len(sys.argv) > 2 else 25
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--autoplay-policy=no-user-gesture-required'])
    pg = b.new_page(viewport={'width':1280,'height':720})
    logs = []
    pg.on('console', lambda m: logs.append(f'[{m.type}] {m.text}'))
    pg.on('pageerror', lambda e: logs.append(f'[pageerror] {e} :: {getattr(e,"stack","")}'))
    pg.goto(url)
    time.sleep(secs)
    for l in logs[:40]: print(l[:300])
    try:
        pg.screenshot(path='/home/claude/psych/boot.png', timeout=60000)
    except Exception as e:
        print('screenshot failed', str(e)[:100])
    for l in logs[:60]: print(l[:300])
    print('total logs', len(logs))
    b.close()
