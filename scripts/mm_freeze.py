import time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--no-sandbox','--autoplay-policy=no-user-gesture-required','--use-gl=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)[:200])); pg.on('dialog',lambda d:d.accept())
    pg.goto('http://localhost:8123/index.html?launch=vanilla'); time.sleep(30)
    pg.mouse.click(640,360); pg.keyboard.press('Enter'); time.sleep(15)
    S="(()=>({ctx:Howler.ctx.state,f:window.__f||0}))()"
    print('before',pg.evaluate("Howler.ctx.state"))
    pg.evaluate("window.psychOpenMaker()"); time.sleep(1)
    print('open',pg.evaluate("Howler.ctx.state"))
    pg.mouse.click(300,300); time.sleep(1); print("afterclick",pg.evaluate("Howler.ctx.state"), pg.evaluate("document.getElementById(\"openfl-content\").style.visibility"))
    pg.evaluate("document.querySelector('#mm-close').onclick()"); time.sleep(1)
    print('closed',pg.evaluate("Howler.ctx.state"), errs)
    b.close()
