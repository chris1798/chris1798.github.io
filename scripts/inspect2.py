import re, json
data = open('F:/tmp/trending_raw.html', encoding='utf-8', errors='replace').read()
articles = re.findall(r'<article class="Box-row">(.*?)</article>', data, re.S | re.I)
# 看第一篇的 star/fork 連結周圍文字
a = articles[0]
# star 連結
for tag in ['stargazers', 'forks']:
    for m in re.finditer(r'href="/[^"]*/%s[^"]*"[^>]*>(.*?)</a>' % tag, a, re.S):
        inner = re.sub(r'<.*?>', '', m.group(1))
        print(f"[{tag}]", repr(inner.strip())[:80])

# 看 total 文字
mtot = re.search(r'([\d,]+) stars? total', a)
print("total stars regex:", mtot.group(1) if mtot else None)
# weekly
mwk = re.search(r'([\d,]+) stars? this week', a)
print("weekly regex:", mwk.group(1) if mwk else None)
# fork 連結後
mf = re.search(r'href="/[^"]*/forks[^"]*"[^>]*>(.*?)</a>', a, re.S)
if mf:
    inner = re.sub(r'<.*?>', '', mf.group(1))
    print("forks inner:", repr(inner.strip())[:80])

# description
d = re.search(r'<p class="col-9.*?>(.*?)</p>', a, re.S | re.I)
print("desc:", repr(d.group(1)[:150]) if d else None)
# language
l = re.search(r'itemprop="programmingLanguage">([^<]+)</a>', a)
print("lang:", l.group(1) if l else None)
