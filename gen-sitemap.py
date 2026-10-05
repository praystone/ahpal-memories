import os

base = 'https://memories.ahpal.com'
urls = [f'{base}/', f'{base}/members/', f'{base}/blogs/']

for f in os.listdir('content/members'):
    if f.endswith('.md') and f != '_index.md':
        urls.append(f'{base}/members/{f[:-3]}/')

for i in range(2, 634):
    urls.append(f'{base}/blogs/page/{i}/')

xml = '<?xml version="1.0" encoding="UTF-8"?>' + chr(10)
xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + chr(10)
for u in urls:
    xml += '  <url><loc>' + u + '</loc></url>' + chr(10)
xml += '</urlset>'

with open('public/sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(xml)

print('OK: ' + str(len(urls)) + ' URLs')