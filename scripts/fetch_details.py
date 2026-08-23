import urllib.request, ssl, json

repos = [
    "modular/modular",
    "harry0703/MoneyPrinterTurbo",
    "basecamp/omarchy",
    "cordiverse/cordis",
    "volcengine/OpenViking",
    "public-apis/public-apis",
    "jundot/omlx",
    "akitaonrails/ai-memory",
    "anthropics/claude-plugins-community",
    "cursor/plugins",
]

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 Chrome/120.0',
        'Accept': 'application/vnd.github+json',
    })
    with urllib.request.urlopen(req, timeout=40, context=ctx) as resp:
        return json.load(resp)

results = {}
for repo in repos:
    owner, name = repo.split('/')
    info = {}
    # API metadata
    try:
        d = get(f"https://api.github.com/repos/{repo}")
        info['description'] = d.get('description') or ''
        info['language'] = d.get('language')
        info['stars'] = d.get('stargazers_count')
        info['forks'] = d.get('forks_count')
        info['topics'] = d.get('topics') or []
        info['homepage'] = d.get('homepage') or ''
        info['license'] = (d.get('license') or {}).get('spdx_id') or ''
        info['created'] = d.get('created_at', '')[:10]
        info['pushed'] = d.get('pushed_at', '')[:10]
        info['url'] = d.get('html_url')
    except Exception as e:
        info['error'] = str(e)
    # README
    for branch in ['main', 'master', 'master']:
        try:
            c = get(f"https://api.github.com/repos/{repo}/contents/README.md?ref={branch}")
            import base64
            readme = base64.b64decode(c['content']).decode('utf-8', errors='replace')
            info['readme'] = readme[:2500]
            break
        except Exception:
            continue
    results[repo] = info

json.dump(results, open('F:/tmp/repo_details.json', 'w'), ensure_ascii=False, indent=2)
print("Fetched details for", len(results), "repos")
for r, d in results.items():
    print(f"\n=== {r} ===")
    print(" stars:", d.get('stars'), "lang:", d.get('language'), "license:", d.get('license'))
    print(" desc:", (d.get('description') or '')[:120])
    print(" topics:", (d.get('topics') or [])[:8])
    print(" readme_head:", (d.get('readme') or 'NO README')[:200].replace('\n',' '))
