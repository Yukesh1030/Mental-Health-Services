import os
import re
from bs4 import BeautifulSoup

files = [
    'admin-dashboard.html',
    'admin-clients.html',
    'admin-therapists.html',
    'admin-sessions.html',
    'admin-reports.html',
    'admin-alerts.html',
    'admin-settings.html'
]

dynamic_js = """
// Dynamic Username
window.addEventListener('DOMContentLoaded', () => {
  let user = localStorage.getItem('currentUser');
  if(!user) {
    user = 'Rohan'; // default fallback for direct access
  }
  if(user) {
    const formatted = user.charAt(0).toUpperCase() + user.slice(1);
    
    // Update top right name
    const nameEl = document.querySelector('.admin-id .name');
    if (nameEl) nameEl.textContent = formatted;
    
    // Update avatar initials
    const avatarEl = document.querySelector('.admin-id .avatar');
    if (avatarEl) avatarEl.textContent = formatted.substring(0, 2).toUpperCase();
    
    // Update Good morning h1
    const h1Els = document.querySelectorAll('h1');
    h1Els.forEach(h1 => {
        if (h1.textContent.includes('Good morning')) {
            h1.textContent = 'Good morning, ' + formatted + '.';
        }
    });
  }
});
"""

for filename in files:
    if not os.path.exists(filename): continue
    
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    # Remove the old script using regex
    html = re.sub(r"// Dynamic Username.*?}\);", "", html, flags=re.DOTALL)
    
    soup = BeautifulSoup(html, 'html.parser')
    
    script_tags = soup.find_all('script')
    if script_tags:
        last_script = script_tags[-1]
        last_script.string = (last_script.string or '').strip() + "\\n" + dynamic_js
        
    out = str(soup)
    # Fix BS4 lowercasing
    out = out.replace('viewbox=', 'viewBox=')
    out = out.replace('preserveaspectratio=', 'preserveAspectRatio=')
    out = out.replace('<lineargradient', '<linearGradient')
    out = out.replace('</lineargradient>', '</linearGradient>')
    out = out.replace('stop-color', 'stop-color')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(out)

print("Updated dynamic username script with fallback and h1 replacement.")
