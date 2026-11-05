import asyncio, json, time, urllib.request
from playwright.async_api import async_playwright
# wait for the live site to serve the new download page
for i in range(40):
    try:
        if urllib.request.urlopen("https://lumimagicalworld.com/download/lumi/", timeout=15).status == 200: break
    except Exception: pass
    time.sleep(15)
out=[]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page()
        pg.on("request", lambda r: out.append({"url": r.url, "post": (r.post_data or "")[:400]}) if "cloudflareinsights.com/cdn-cgi/rum" in r.url else None)
        await pg.goto("https://lumimagicalworld.com/download/lumi/", wait_until="load"); await pg.wait_for_timeout(2500)
        out.append({"final_url": pg.url})
        await b.close()
asyncio.run(main())
json.dump(out, open(".yt/live-result.json","w"), indent=1); print(json.dumps(out, indent=1))
