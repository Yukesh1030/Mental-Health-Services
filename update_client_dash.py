import os
import re
from bs4 import BeautifulSoup

file_path = 'client-dashboard.html'
if not os.path.exists(file_path):
    print("File not found")
    exit()

with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Emojis map
emoji_map = {
    '👥': '<i class="fas fa-users"></i>',
    '🗓️': '<i class="fas fa-calendar-alt"></i>',
    '⚠️': '<i class="fas fa-exclamation-triangle"></i>',
    '💰': '<i class="fas fa-dollar-sign"></i>',
    '📈': '<i class="fas fa-chart-line"></i>',
    '🚨': '<i class="fas fa-exclamation-circle"></i>',
    '⏱️': '<i class="fas fa-stopwatch"></i>',
    '✅': '<i class="fas fa-check-circle"></i>',
    '📝': '<i class="fas fa-edit"></i>',
    '📅': '<i class="fas fa-calendar-day"></i>',
    '💬': '<i class="fas fa-comment-dots"></i>',
    '💻': '<i class="fas fa-laptop"></i>',
    '📱': '<i class="fas fa-mobile-alt"></i>',
    '📉': '<i class="fas fa-chart-bar"></i>',
    '💡': '<i class="fas fa-lightbulb"></i>',
    '🧠': '<i class="fas fa-brain"></i>',
    '⚙️': '<i class="fas fa-cog"></i>'
}

for emoji, tag in emoji_map.items():
    html = html.replace(emoji, tag)

soup = BeautifulSoup(html, 'html.parser')

# Add FontAwesome CDN
if not soup.find('link', href=re.compile('font-awesome')):
    head = soup.find('head')
    if head:
        fa_link = soup.new_tag('link', rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css')
        head.append(fa_link)
        style = soup.new_tag('style')
        style.string = "\\n  .nav-item i.fas { font-size: 1.1rem; width: 18px; text-align: center; opacity: 0.85; flex-shrink: 0; }\\n"
        head.append(style)

# Sidebar mapping for client dashboard
sidebar_map = {
    'overview': 'fas fa-home',
    'sessions': 'fas fa-video',
    'journal': 'fas fa-book',
    'resources': 'fas fa-heart',
    'settings': 'fas fa-cog'
}

for item in soup.find_all(class_='nav-item'):
    view = item.get('data-view')
    if view in sidebar_map:
        svg = item.find('svg')
        if svg:
            i_tag = soup.new_tag('i', attrs={'class': sidebar_map[view]})
            svg.replace_with(i_tag)
    elif 'Logout' in item.text:
        svg = item.find('svg')
        if svg:
            i_tag = soup.new_tag('i', attrs={'class': 'fas fa-sign-out-alt'})
            svg.replace_with(i_tag)

# Topbar bell
bell = soup.find('div', class_='bell')
if bell:
    svg = bell.find('svg')
    if svg:
        i_tag = soup.new_tag('i', attrs={'class': 'fas fa-bell', 'style': 'font-size: 1.2rem;'})
        svg.replace_with(i_tag)

# Forms validation
search_inputs = soup.find_all('input', placeholder=lambda p: p and 'Search' in p)
for s_input in search_inputs:
    if s_input.parent.name != 'form':
        form = soup.new_tag('form', action='404.html', method='GET', style='display:inline-block; width:100%; max-width:400px; margin:0;')
        s_input.wrap(form)
        s_input['required'] = ''

# 404 Redirection for links and buttons
for a in soup.find_all('a'):
    if 'nav-item' in a.get('class', []): continue
    if 'brand' in (a.parent.get('class', []) if a.parent else []): continue
    if a.get('href') and a['href'].startswith('javascript:'): continue
    if a.get('href') and a['href'].startswith('#'): continue
    a['href'] = '404.html'

for btn in soup.find_all('button'):
    classes = btn.get('class', [])
    if 'nav-item' in classes or 'sidebar-close' in classes or btn.get('id') == 'hamburger':
        continue
    if btn.get('type') == 'submit' or (btn.parent and btn.parent.name == 'form'):
        continue
    # Ensure mood buttons don't break JS if they have classes. Wait, client dashboard has mood buttons!
    # They should not be rerouted if they trigger JS UI, but user said all general links to 404.
    # We will exclude mood buttons specifically.
    if 'mood-btn' in classes:
        continue
    if not btn.has_attr('onclick'):
        btn['onclick'] = "window.location.href='404.html';"

# Dynamic Username Script
script_tags = soup.find_all('script')
if script_tags:
    last_script = script_tags[-1]
    dynamic_js = """
// Dynamic Username
window.addEventListener('DOMContentLoaded', () => {
  const user = localStorage.getItem('currentUser');
  if(user) {
    const formatted = user.charAt(0).toUpperCase() + user.slice(1);
    const nameEl = document.querySelector('.client-id .name');
    const avatarEl = document.querySelector('.client-id .avatar');
    if (nameEl) nameEl.textContent = formatted;
    if (avatarEl) avatarEl.textContent = formatted.substring(0, 2).toUpperCase();
  }
});
    """
    if "localStorage.getItem('currentUser')" not in (last_script.string or ""):
        last_script.string = (last_script.string or '') + dynamic_js

# Remove badge from sidebar
for badge in soup.find_all('span', class_='badge'):
    badge.decompose()

# Restore SVG Case
out = str(soup)
out = out.replace('viewbox=', 'viewBox=')
out = out.replace('preserveaspectratio=', 'preserveAspectRatio=')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(out)

print("Client dashboard updated.")
