import urllib.request, ssl, os, json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
base = "F:/gitdisk/chris1798.github.io/assets/images/github-trending-weekly/"
os.makedirs(base, exist_ok=True)

def get(url, out):
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 Chrome/120'})
    try:
        with urllib.request.urlopen(req, timeout=40, context=ctx) as resp:
            code = resp.getcode(); content = resp.read()
        with open(out,'wb') as f: f.write(content)
        print(f"{code} {len(content):>7}B -> {os.path.basename(out)}")
    except Exception as e:
        print("FAIL", os.path.basename(out), str(e)[:50])

def list_files(repo, branches):
    for b in branches:
        req = urllib.request.Request(f"https://api.github.com/repos/{repo}/contents/?ref={b}",
            headers={'User-Agent':'Mozilla/5.0','Accept':'application/vnd.github+json'})
        try:
            with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
                items = json.load(resp)
            imgs = [it for it in items if it['type']=='file' and it['name'].lower().endswith(('.png','.jpg','.svg','.webp'))]
            print(f"\n[{repo}@{b}] {len(items)} items, images:")
            for it in imgs:
                print("   ", it['path'], it['size'])
            return True
        except Exception as e:
            print(f"[{repo}@{b}] ERR {str(e)[:40]}")
    return False

list_files("modular/modular", ["main","master","devel"])
list_files("harry0703/MoneyPrinterTurbo", ["main","master"])
list_files("cordiverse/cordis", ["main","master","master"])
list_files("jundot/omlx", ["main","master"])
list_files("basecamp/omarchy", ["master","main"])
list_files("public-apis/public-apis", ["main","master"])
list_files("cursor/plugins", ["main","master"])
list_files("anthropics/claude-plugins-community", ["main","master"])
