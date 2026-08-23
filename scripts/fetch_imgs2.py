import urllib.request, ssl, os, json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
base = "F:/gitdisk/chris1798.github.io/assets/images/github-trending-weekly/"

def get(url, out):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 Chrome/120'})
    try:
        with urllib.request.urlopen(req, timeout=40, context=ctx) as resp:
            code = resp.getcode(); content = resp.read()
        with open(out,'wb') as f: f.write(content)
        print(f"{code} {len(content):>7}B -> {os.path.basename(out)}")
    except Exception as e:
        print("FAIL", os.path.basename(out), str(e)[:70])

# omarchy logo
get("https://raw.githubusercontent.com/basecamp/omarchy/master/logo.svg", base+"omarchy-logo.png")
# MoneyPrinterTurbo - 找 banner
for path in ["banner.png","og.png","cover.png","docs/banner.png"]:
    get(f"https://raw.githubusercontent.com/harry0703/MoneyPrinterTurbo/master/{path}", base+f"moneyprinter-{path.replace('/','-')}.png")
# cordis banner
for path in ["banner.png","og.png","docs/banner.png","cover.png"]:
    get(f"https://raw.githubusercontent.com/cordiverse/cordis/master/{path}", base+f"cordis-{path.replace('/','-')}.png")
# omlx banner
for path in ["banner.png","og.png","docs/banner.png"]:
    get(f"https://raw.githubusercontent.com/jundot/omlx/master/{path}", base+f"omlx-{path.replace('/','-')}.png")
# modular S3 banner (already have) - try github OG
for path in ["og.png","banner.png","docs/og.png"]:
    get(f"https://raw.githubusercontent.com/modular/modular/master/{path}", base+f"modular-og-{path.replace('/','-')}.png")
