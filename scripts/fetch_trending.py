import urllib.request, ssl, re, json, html

url = "https://github.com/trending?since=weekly&spoken_language_code="
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml',
})
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
with urllib.request.urlopen(req, timeout=45, context=ctx) as resp:
    data = resp.read()
open('F:/tmp/trending_raw.html','wb').write(data)
print("bytes:", len(data))

text = data.decode('utf-8', errors='replace')
articles = re.findall(r'<article class="Box-row".*?</article>', text, re.S | re.I)
print("article count:", len(articles))

repos = []
for a in articles:
    m = re.search(r'href="/([^/]+/[^/]+)"', a)
    repo = m.group(1).strip() if m else None
    desc_m = re.search(r'<p class="col-9.*?>(.*?)</p>', a, re.S | re.I)
    desc = html.unescape(re.sub(r'<.*?>', '', desc_m.group(1)).strip()) if desc_m else ''
    lang_m = re.search(r'itemprop="programmingLanguage">([^<]+)</a>', a)
    lang = lang_m.group(1).strip() if lang_m else ''
    repo_esc = re.escape(repo) if repo else ''
    stars_m = re.search(r'href="/' + repo_esc + r'/stargazers".*?([\d,]+) stars? total', a, re.S | re.I)
    weekly_m = re.search(r'([\d,]+) stars? this week', a, re.S | re.I)
    forks_m = re.search(r'href="/' + repo_esc + r'/forks".*?([\d,]+) forks?', a, re.S | re.I)
    repos.append({
        'repo': repo,
        'desc': desc,
        'lang': lang,
        'stars': stars_m.group(1) if stars_m else '',
        'weekly': weekly_m.group(1) if weekly_m else '',
        'forks': forks_m.group(1) if forks_m else '',
    })

for i, r in enumerate(repos[:15], 1):
    print(f"\n{i}. {r['repo']}")
    print(f"   lang: {r['lang']} | stars: {r['stars']} | weekly: {r['weekly']} | forks: {r['forks']}")
    print(f"   desc: {r['desc'][:150]}")

json.dump(repos, open('F:/tmp/trending.json','w'), ensure_ascii=False, indent=2)
print("\nSaved F:/tmp/trending.json")
