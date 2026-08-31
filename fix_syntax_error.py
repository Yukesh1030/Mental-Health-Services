import os

files = [
    'admin-dashboard.html',
    'admin-clients.html',
    'admin-therapists.html',
    'admin-sessions.html',
    'admin-reports.html',
    'admin-alerts.html',
    'admin-settings.html',
    'client-dashboard.html'
]

for filename in files:
    if not os.path.exists(filename): continue
    
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    # Fix the literal \n
    html = html.replace("});\\n\\n  // Dynamic Username", "});\\n  // Dynamic Username")
    # Actually just to be totally safe:
    html = html.replace("});\\n", "});\\n")
    # Wait, in Python, replace("\\\\n", "\\n") will replace the literal backslash n with a newline.
    html = html.replace("\\\\n", "\\n")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

print("Fixed SyntaxError caused by literal backslash n.")
