import os
import glob
import re

files_to_update = glob.glob(r"d:\yukesh\projects\Mental Health Services\admin-*.html") + \
                  glob.glob(r"d:\yukesh\projects\Mental Health Services\client-*.html")

for filepath in files_to_update:
    # Skip client-dashboard.html because we already updated it manually, 
    # but the regex is safe anyway because we can check if it's already wrapped.
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern for <div class="brand"> and <div class="brand-mini"> img
    # We want to wrap <img alt="STACKLY Wellness" src="assets/Brand-logo.webp"...> 
    # or <img alt="Haven Logo"...>
    
    # regex to find <img ... src="assets/Brand-logo.webp" ... /> that are NOT inside <a>
    # This is tricky with regex, let's just do specific replacements.
    
    # 1. <div class="brand">\n<img .../>
    # We can replace: <img alt="Haven Logo" src="assets/Brand-logo.webp" style="height: 32px; width: auto;"/>
    # with: <a href="index.html"><img alt="Haven Logo" src="assets/Brand-logo.webp" style="height: 32px; width: auto;"/></a>
    # Wait, the img tags differ between files. In client it's 'alt="STACKLY Wellness"', in admin it's 'alt="Haven Logo"'.
    
    def replace_img(match):
        img_tag = match.group(0)
        # Check if it's already inside an <a> tag. 
        # But we are just matching the img tag directly.
        # It's safer to just find <div class="brand">\n<img ...>
        return img_tag
        
    # Let's use a simpler string replace since the HTML is very consistent.
    
    # Admin brand (height: 32px)
    admin_brand_img = '<img alt="Haven Logo" src="assets/Brand-logo.webp" style="height: 32px; width: auto;"/>'
    # Admin brand-mini (height: 24px)
    admin_mini_img = '<img alt="Haven Logo" src="assets/Brand-logo.webp" style="height: 24px; width: auto;"/>'
    
    # Client brand (height: 32px)
    client_brand_img = '<img alt="STACKLY Wellness" src="assets/Brand-logo.webp" style="height: 32px; width: auto;"/>'
    # Client brand-mini (height: 24px)
    client_mini_img = '<img alt="STACKLY Wellness" src="assets/Brand-logo.webp" style="height: 24px; width: auto;"/>'

    replacements = [
        (f'<div class="brand">\n{admin_brand_img}', f'<div class="brand">\n<a href="index.html">{admin_brand_img}</a>'),
        (f'<div class="brand-mini">\n{admin_mini_img}', f'<div class="brand-mini">\n<a href="index.html">{admin_mini_img}</a>'),
        (f'<div class="brand">\n{client_brand_img}', f'<div class="brand">\n<a href="index.html">{client_brand_img}</a>'),
        (f'<div class="brand-mini">\n{client_mini_img}', f'<div class="brand-mini">\n<a href="index.html">{client_mini_img}</a>'),
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Updated {os.path.basename(filepath)}")
