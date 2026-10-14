import sys, time, json
from playwright.sync_api import sync_playwright
url = sys.argv[1]
steps = json.loads(sys.argv[2])  # list of [key, wait_seconds, shotname]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--autoplay-policy=no-user-gesture-required'])
    pg = b.new_page(viewport={'width':1280,'height':720})
    logs = []
    pg.on('console', lambda m: logs.append(f'[{m.type}] {m.text}'))
    pg.on('pageerror', lambda e: logs.append(f'[pageerror] {e} :: {getattr(e,"stack","")[:600]}'))
    pg.goto(url)
    time.sleep(15)
    pg.mouse.click(640, 360)
    for key, wait, shot in steps:
        if key:
            for k in key.split('+'):
                n=1
                if '*' in k: k,n=k.split('*'); n=int(n)
                for _ in range(n):
                    pg.keyboard.down(k); time.sleep(0.12); pg.keyboard.up(k); time.sleep(0.08)
        time.sleep(wait)
        if shot:
            try: pg.screenshot(path=f'/home/claude/psych/{shot}.png', timeout=60000)
            except Exception as e: print('shot failed', shot)
    for l in logs:
        if 'GL Driver' in l or 'Canvas2D' in l: continue
        print(l[:700])
    b.close()
