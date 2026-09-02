import os
import glob

files = glob.glob(r"d:\yukesh\projects\Mental Health Services\client-*.html")

old_str_1 = "<strong>🔥 12 day streak</strong>"
new_str_1 = '<strong><i class="fa-solid fa-fire" style="color: #ff5722; margin-right: 6px;"></i>12 day streak</strong>'

old_str_2 = '<div class="streak-pill">🔥 <span class="txt">'
new_str_2 = '<div class="streak-pill"><i class="fa-solid fa-fire" style="color: #ff5722; margin-right: 6px;"></i><span class="txt">'

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    content = content.replace(old_str_1, new_str_1)
    content = content.replace(old_str_2, new_str_2)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {os.path.basename(filepath)}")
