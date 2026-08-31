import os
import re
from bs4 import BeautifulSoup

# 1. Update forms.js
with open('js/forms.js', 'r', encoding='utf-8') as f:
    forms_js = f.read()

if "localStorage.setItem('currentUser'" not in forms_js:
    # insert before window.location.href = 'admin-dashboard.html';
    forms_js = forms_js.replace("if (loginAs && loginAs.value === 'Admin') {", "let username = email.value.split('@')[0];\n                localStorage.setItem('currentUser', username);\n                if (loginAs && loginAs.value === 'Admin') {")
    with open('js/forms.js', 'w', encoding='utf-8') as f:
        f.write(forms_js)


# 2. Update all admin pages
files = [
    'admin-dashboard.html',
    'admin-clients.html',
    'admin-therapists.html',
    'admin-sessions.html',
    'admin-reports.html',
    'admin-alerts.html',
    'admin-settings.html'
]

for filename in files:
    if not os.path.exists(filename): continue
    
    with open(filename, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Remove badge '5' from alerts
    for a in soup.find_all('a', class_='nav-item'):
        if 'Alerts' in a.text or a.get('data-view') == 'alerts':
            badge = a.find('span', class_='badge')
            if badge:
                badge.decompose()
    
    # Add dynamic username script
    script_tags = soup.find_all('script')
    if script_tags:
        last_script = script_tags[-1]
        
        dynamic_js = """
    // Dynamic Username
    window.addEventListener('DOMContentLoaded', () => {
      const user = localStorage.getItem('currentUser');
      if(user) {
        const formatted = user.charAt(0).toUpperCase() + user.slice(1);
        const nameEl = document.querySelector('.admin-id .name');
        const avatarEl = document.querySelector('.admin-id .avatar');
        if (nameEl) nameEl.textContent = formatted;
        if (avatarEl) avatarEl.textContent = formatted.substring(0, 2).toUpperCase();
      }
    });
        """
        
        if "localStorage.getItem('currentUser')" not in (last_script.string or ""):
            last_script.string = (last_script.string or '') + dynamic_js

    # Write back to file, fixing BeautifulSoup lowercasing issues for SVGs (just in case)
    html_content = str(soup)
    html_content = html_content.replace('viewbox=', 'viewBox=')
    html_content = html_content.replace('preserveaspectratio=', 'preserveAspectRatio=')
    html_content = html_content.replace('<lineargradient', '<linearGradient')
    html_content = html_content.replace('</lineargradient>', '</linearGradient>')
    html_content = html_content.replace('stop-color', 'stop-color')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

print('Updated dynamic username and removed alert badge.')
