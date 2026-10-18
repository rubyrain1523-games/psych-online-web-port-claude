import time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); logs=[]
    pg.on('console',lambda m: logs.append(m.text)); pg.on('pageerror',lambda e: logs.append('PAGEERROR '+str(e)[:500]))
    def h(route):
        r=route.request
        logs.append('REQ %s %s ct=%s BODY=%s'%(r.method,r.url,r.headers.get('content-type'),(r.post_data or '')[:1500]))
        route.fulfill(status=200,headers={'access-control-allow-origin':'*','access-control-allow-headers':'*','content-type':'application/json'},body='{"error":"stub","code":5000}')
    pg.route('**/matchmake/**',h); pg.on('request',lambda r: logs.append('NET '+r.method+' '+r.url) if 'sniro' in r.url or 'github' in r.url else None)
    pg.goto('http://localhost:8123/index.html'); time.sleep(20); pg.mouse.click(640,360); time.sleep(15)
    pg.evaluate("window.psychJoinTest('wss://funkin.sniro.boo')"); time.sleep(15)
    pg.evaluate("setTimeout(()=>console.log('TOFIRED'),0)"); time.sleep(2)
    print('alive', pg.evaluate('typeof window.psychJoinTest'))
    for l in logs:
        if 'GL Driver' not in l and 'Canvas2D' not in l: print(l[:1800])
    b.close()
