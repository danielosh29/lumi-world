"""Fetch the channel's subscriber count and write assets/subs.json.
Uses the YouTube Data API when YT_API_KEY is set; otherwise reads the public channel page."""
import json, os, re, sys, urllib.request, datetime

HANDLE = "lumiandthemagicalworld"
OUT = "assets/subs.json"

def label_for(n):
    step = 500 if n < 10_000 else 1_000 if n < 100_000 else 10_000
    return f"{(n // step) * step:,}+"

def via_api(key):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&forHandle=@{HANDLE}&key={key}"
    data = json.load(urllib.request.urlopen(url, timeout=30))
    return int(data["items"][0]["statistics"]["subscriberCount"])

def via_page():
    req = urllib.request.Request(
        f"https://www.youtube.com/@{HANDLE}/about",
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
                 "Accept-Language": "en-US,en;q=0.9", "Cookie": "CONSENT=YES+1; SOCS=CAI"})
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
    m = re.search(r'"subscriberCountText":\{"simpleText":"([^"]+)"', html) or \
        re.search(r'"subscriberCountText":"([^"]+)"', html) or \
        re.search(r'"([\d.,]+\s*[KM]?)\s+subscribers?"', html)
    if not m:
        raise RuntimeError("subscriber text not found on channel page")
    txt = m.group(1).replace("subscribers", "").replace("subscriber", "").strip()
    mm = re.match(r"([\d.,]+)\s*([KM]?)", txt)
    num = float(mm.group(1).replace(",", "")) * {"": 1, "K": 1_000, "M": 1_000_000}[mm.group(2)]
    return int(num)

def main():
    key = os.environ.get("YT_API_KEY", "").strip()
    count = via_api(key) if key else via_page()
    print("fetched subscriber count:", count)
    prev = {}
    if os.path.exists(OUT):
        prev = json.load(open(OUT))
    if count < 1000 or (prev.get("count") and count < prev["count"] * 0.7):
        sys.exit(f"implausible count {count} (previous {prev.get('count')}); leaving file untouched")
    label = label_for(count)
    if count == prev.get("count"):
        print("count unchanged:", count); return
    json.dump({"count": count, "label": label,
               "updated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")},
              open(OUT, "w"), indent=2)
    print("wrote", OUT, "->", label)

if __name__ == "__main__":
    main()
