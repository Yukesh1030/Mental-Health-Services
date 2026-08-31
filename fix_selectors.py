import os
import re

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

    # Fix the selector for the admin-id and client-id
    html = html.replace("document.querySelector('.admin-id .name')", "document.querySelector('.admin-id .txt p:first-child')")
    html = html.replace("document.querySelector('.client-id .name')", "document.querySelector('.client-id .txt p:first-child')")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

print("Fixed CSS selectors for dynamic username.")
