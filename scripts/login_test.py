import time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); logs=[]
    pg.on('console',lambda m: logs.append(m.text)); pg.on('pageerror',lambda e: logs.append('PAGEERROR '+str(e)[:300]))
    def h(route):
        r=route.request
        logs.append('REQ %s %s ct=%s BODY=%s'%(r.method,r.url,r.headers.get('content-type'),(r.post_data or '')[:200]))
        if r.method=='OPTIONS':
            route.fulfill(status=204,headers={'access-control-allow-origin':'*','access-control-allow-headers':'*','access-control-allow-methods':'*'})
        else:
            route.fulfill(status=200,headers={'access-control-allow-origin':'*','content-type':'application/json'},body='{}')
    pg.route('**/api/auth/login',h)
    pg.goto('http://localhost:8123/index.html?launch=vanilla'); time.sleep(20)
    pg.evaluate("window.psychLoginTest('me@example.org')")
    for _ in range(6): pg.evaluate('1'); time.sleep(2)
    for l in logs:
        if any(k in l for k in ['REQ','LOGIN','PAGEERROR','Could not']): print(l[:400])
    b.close()
