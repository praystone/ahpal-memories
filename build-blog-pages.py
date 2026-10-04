# -*- coding: utf-8 -*-
"""
用 Python 直接產 632 個日誌分頁 HTML
"""
import os
import json
import html

SITE_ROOT = r"C:\Projects\ahpal_backup\backup-7.10.2025_06-35-38_flwsybvf675b\mysql\uchome_site"
BLOGS_JSON = os.path.join(SITE_ROOT, "data", "blogs.json")
OUTPUT_DIR = os.path.join(SITE_ROOT, "public", "blogs")
PAGE_SIZE = 50

# 讀 JSON
print(f"讀 {BLOGS_JSON}")
with open(BLOGS_JSON, encoding="utf-8") as f:
    blogs = json.load(f)

print(f"共 {len(blogs)} 篇日誌")

# 每頁 50 篇
total_pages = (len(blogs) + PAGE_SIZE - 1) // PAGE_SIZE
print(f"共 {total_pages} 頁")

# 產 HTML
os.makedirs(OUTPUT_DIR, exist_ok=True)

def escape(s):
    return html.escape(str(s or ""))

def render_page(page_num):
    start = (page_num - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    page_blogs = blogs[start:end]

    # 分頁導覽
    nav = '<nav class="pagination">'
    if page_num > 1:
        prev_url = "/blogs/" if page_num == 2 else f"/blogs/page/{page_num - 1}/"
        nav += f'<a href="{prev_url}">← 上一頁</a>'
    nav += f'<span>第 {page_num} / {total_pages} 頁</span>'
    if page_num < total_pages:
        nav += f'<a href="/blogs/page/{page_num + 1}/">下一頁 →</a>'
    nav += '</nav>'

    # 日誌內容
    articles = []
    for b in page_blogs:
        articles.append(f'''
<article class="blog-entry">
    <header>
        <h2 class="blog-entry-title">{escape(b.get("title", "(無標題)"))}</h2>
        <div class="blog-entry-meta">
            ✍️ {escape(b.get("author", ""))} ｜ 📅 {escape(b.get("dateline", ""))} ｜ 👁️ {escape(b.get("viewnum", 0))} ｜ 💬 {escape(b.get("replynum", 0))}
        </div>
    </header>
    <div class="blog-entry-body">{b.get("body", "")}</div>
</article>
''')

    html_content = f'''<!DOCTYPE html>
<html lang="zh-tw">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>📝 日誌 - 第 {page_num} 頁 - AHPAL 回憶館</title>
<link rel="stylesheet" href="/css/main.css">
</head>
<body>
<header class="site-header">
    <div class="header-inner">
        <a href="/" class="logo">📚 AHPAL 回憶館</a>
        <nav class="nav-links">
            <a href="/">首頁</a>
            <a href="/members/">會員</a>
            <a href="/blogs/">日誌</a>
            <a href="https://www.ahpal.com/">回到主站</a>
        </nav>
    </div>
</header>
<main class="main-wrapper">
    <div class="content-card">
        <h1>📝 日誌</h1>
        <p class="hero-desc">{len(blogs)} 篇日誌，6 年的生命故事。</p>
        {''.join(articles)}
        {nav}
    </div>
</main>
<footer class="site-footer">
    <div class="footer-inner">
        <p class="footer-copy">© 2026 雅寶社區 · 頂客論壇 (AHPAL.COM)</p>
    </div>
</footer>
</body>
</html>'''

    return html_content

# 產第 1 頁（/blogs/index.html）
with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(render_page(1))
print(f"✅ /blogs/index.html")

# 產第 2~N 頁（/blogs/page/N/index.html）
for page_num in range(2, total_pages + 1):
    page_dir = os.path.join(OUTPUT_DIR, "page", str(page_num))
    os.makedirs(page_dir, exist_ok=True)
    with open(os.path.join(page_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_page(page_num))
    if page_num % 50 == 0:
        print(f"   進度：{page_num} / {total_pages}")

print(f"✅ 產了 {total_pages} 頁")