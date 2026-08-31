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

    # The issue is the literal string "\\n" (a backslash followed by an n).
    # We want to replace it with a real newline (or just delete it since it's already on a new line).
    html = html.replace(r"\n", "")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

print("Removed all literal backslash-n characters.")
