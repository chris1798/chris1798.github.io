import re, json
data = open('F:/tmp/trending_raw.html', encoding='utf-8', errors='replace').read()
articles = re.findall(r'<article class="Box-row">(.*?)</article>', data, re.S | re.I)
print("count:", len(articles))
for i, a in enumerate(articles[:3], 1):
    print(f"\n===== ARTICLE {i} (len={len(a)}) =====")
    h2 = re.search(r'<h2[^>]*>(.*?)</h2>', a, re.S | re.I)
    if h2:
        print("H2 RAW:", h2.group(1)[:400])
    for m in re.finditer(r'href="[^"]*/(stargazers|forks)/?[^"]*"', a):
        print("LINK:", m.group(0)[:150])
