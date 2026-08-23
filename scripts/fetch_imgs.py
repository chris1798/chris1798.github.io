import urllib.request, ssl, os, json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get(url, out):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 Chrome/120'})
    with urllib.request.urlopen(req, timeout=40, context=ctx) as resp:
        code = resp.getcode()
        content = resp.read()
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'wb') as f:
        f.write(content)
    print(f"{code} {len(content):>7}B -> {out}")

# 各 repo 的 banner/logo 路徑 (從 README 提取)
targets = [
    # modular (S3)
    ("https://modular-assets.s3.us-east-1.amazonaws.com/images/modular-banner-github.png",
     "F:/gitdisk/chris1798.github.io/assets/images/github-trending-weekly/modular-banner.png"),
    # OpenViking (docs/images)
    ("https://raw.githubusercontent.com/volcengine/OpenViking/master/docs/images/ov-logo.png",
     "F:/gitdisk/chris1798.github.io/assets/images/github-trending-weekly/openviking-logo.png"),
    # ai-memory
    ("https://raw.githubusercontent.com/akitaonrails/ai-memory/master/docs/logo-light.png",
     "F:/gitdisk/chris1798.github.io/assets/images/github-trending-weekly/ai-memory-logo.png"),
]
for url, out in targets:
    try:
        get(url, out)
    except Exception as e:
        print("FAIL", out, str(e)[:80])

# 列 master/main 找 banner/og 圖
repos_branch = [
    ("modular/modular", ["main","master"]),
    ("harry0703/MoneyPrinterTurbo", ["main","master"]),
    ("basecamp/omarchy", ["master","main"]),
    ("cordiverse/cordis", ["main","master"]),
    ("public-apis/public-apis", ["main"]),
    ("jundot/omlx", ["main","master"]),
    ("cursor/plugins", ["main","master"]),
    ("anthropics/claude-plugins-community", ["main","master"]),
]
for repo, branches in repos_branch:
    for b in branches:
        try:
            req = urllib.request.Request(f"https://api.github.com/repos/{repo}/contents/?ref={b}",
                headers={'User-Agent':'Mozilla/5.0','Accept':'application/vnd.github+json'})
            with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
                items = json.load(resp)
            imgs = [it for it in items if it['type']=='file' and it['name'].lower().endswith(('.png','.jpg','.svg','.webp')) and any(k in it['name'].lower() for k in ['banner','og','logo','cover','preview','screen','hero'])]
            for it in imgs:
                print(f"[{repo}@{b}] IMG: {it['path']} ({it['size']}B)")
            break
        except Exception as e:
            print(f"[{repo}@{b}] ERR", str(e)[:60])
