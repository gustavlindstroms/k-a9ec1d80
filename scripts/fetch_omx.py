"""Hämtar OMXS30 från Yahoo Finance och skriver 6edea6c9/omx.json. Behåller gamla filen vid fel."""
import json, sys, urllib.request

URL = "https://query1.finance.yahoo.com/v8/finance/chart/%5EOMX?interval=1d&range=5d"
OUT = "6edea6c9/omx.json"

try:
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    meta = json.load(urllib.request.urlopen(req, timeout=20))["chart"]["result"][0]["meta"]
    price = meta["regularMarketPrice"]
    prev = meta.get("chartPreviousClose") or meta.get("previousClose")
    pct = meta.get("regularMarketChangePercent")
    if pct is None:
        pct = (price / prev - 1) * 100
    data = {"price": round(price, 2), "changePercent": round(pct, 2), "marketTime": meta["regularMarketTime"]}
except Exception as e:
    print(f"Kunde inte hämta OMX: {e}", file=sys.stderr)
    sys.exit(0)

with open(OUT, "w") as f:
    json.dump(data, f)
print(data)
