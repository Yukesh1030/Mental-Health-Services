import os
import re

files = [
    'admin-dashboard.html',
    'admin-clients.html',
    'admin-therapists.html',
    'admin-sessions.html',
    'admin-reports.html',
    'admin-alerts.html',
    'admin-settings.html'
]

for f in files:
    if not os.path.exists(f): continue
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 1. Hide nav-pill and change active text color
    content = re.sub(
        r'\.nav-pill\{[^}]*\}',
        '.nav-pill{ display: none; }',
        content
    )
    content = re.sub(
        r'\.nav-item\.active\{\s*color:\s*#fff;\s*\}',
        '.nav-item.active{ color: var(--primary); font-weight: 700; background: var(--surface-2); }',
        content
    )

    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print('Updated active color successfully.')
