import asyncio, json, http.server, threading, socketserver, os
from playwright.async_api import async_playwright
PORT=8765
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
httpd=socketserver.TCPServer(("",PORT),Q); threading.Thread(target=httpd.serve_forever,daemon=True).start()
out=[]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page()
        async def on_req(r):
            if "cloudflareinsights" in r.url and "beacon.min.js" not in r.url:
                out.append({"url":r.url,"method":r.method,"post":(r.post_data or "")[:1500]})
        pg.on("request", on_req)
        await pg.goto(f"http://localhost:{PORT}/.yt/test.html"); await pg.wait_for_timeout(2500)
        out.append({"mark":"after load"})
        await pg.evaluate("history.replaceState({}, '', '/download/tracked')"); await pg.wait_for_timeout(1500)
        out.append({"mark":"after tracked replaceState"})
        await pg.evaluate("window.__origReplace.call(history, {}, '', '/.yt/test.html')"); await pg.wait_for_timeout(1500)
        out.append({"mark":"after untracked restore", "href": await pg.evaluate("location.href")})
        await pg.evaluate("history.replaceState({}, '', '/download/second')"); await pg.wait_for_timeout(1500)
        out.append({"mark":"after second tracked"})
        await b.close()
asyncio.run(main())
json.dump(out, open(".yt/beacon-result.json","w"), indent=1)
print(json.dumps(out, indent=1)[:4000])
