import time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_context(viewport={'width':1280,'height':720},has_touch=True).new_page(); logs=[]
    pg.on('console',lambda m: logs.append(m.text))
    pg.goto('http://localhost:8123/index.html?launch=vanilla'); time.sleep(16)
    pg.evaluate("document.querySelector('#openfl-content').addEventListener('touchstart',e=>console.log('JSTOUCH '+e.touches.length),true); window.addEventListener('mousedown',e=>console.log('JSMOUSE'),true)")
    cdp=pg.context.new_cdp_session(pg)
    for i in range(4):
        cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':640,'y':360}]}); time.sleep(0.6); cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]}); time.sleep(1)
    for l in logs:
        if 'TOUCH' in l or 'JSMOUSE' in l: print(l[:120])
    print(len([l for l in logs if 'TOUCHSTART' in l]))
    b.close()
