import time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); logs=[]
    pg.on('console',lambda m: logs.append(m.text))
    def h(route):
        r=route.request
        logs.append('REQ %s %s hdr=%s BODY=%s'%(r.method,r.url,dict(list(r.headers.items())[:6]),r.post_data))
        route.fulfill(status=200,headers={'access-control-allow-origin':'*','access-control-allow-headers':'*','content-type':'application/json'},body='{}')
    pg.route('**/api/auth/**',h)
    pg.goto('http://localhost:8123/index.html?launch=vanilla'); time.sleep(18)
    pg.evaluate("window.psychLogin('test@example.com')")
    for _ in range(6): pg.evaluate('1'); time.sleep(3)
    for l in logs:
        if any(k in l for k in ['REQ','LOGIN','requestWeb','request failed']): print(l[:600])
    b.close()
