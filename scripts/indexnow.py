#!/usr/bin/env python3
"""Submit all sitemap URLs to IndexNow (Bing/Yandex/Naver/Seznam). No account; key file lives in public/."""
import json, re, glob, os, urllib.request
here = os.path.dirname(os.path.abspath(__file__))
key = os.path.basename(glob.glob(os.path.join(here, '..', 'public', '[0-9a-f]' * 32 + '.txt'))[0])[:-4]
xml = urllib.request.urlopen('https://umeboshi-bit.github.io/wakiga-cost/sitemap.xml').read().decode()
urls = re.findall('<loc>(.*?)</loc>', xml)
body = json.dumps({"host": "umeboshi-bit.github.io", "key": key,
  "keyLocation": f"https://umeboshi-bit.github.io/wakiga-cost/{key}.txt", "urlList": urls}).encode()
r = urllib.request.urlopen(urllib.request.Request('https://api.indexnow.org/indexnow', data=body,
  headers={'Content-Type': 'application/json; charset=utf-8'}), timeout=30)
print(r.status, len(urls), 'urls')
