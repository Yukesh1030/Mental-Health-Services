from bs4 import BeautifulSoup
import re

# 1. Update admin-clients.html (Client Growth)
with open('admin-clients.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

growth_html = """
<div class="svg-chart-container" style="position: relative; width: 100%; height: 160px; margin-top: 10px;">
  <svg viewBox="0 0 400 160" preserveAspectRatio="none" style="width: 100%; height: 100%; overflow: visible;">
    <!-- Grid Lines -->
    <line x1="0" y1="20" x2="400" y2="20" stroke="var(--line)" stroke-dasharray="4" />
    <line x1="0" y1="60" x2="400" y2="60" stroke="var(--line)" stroke-dasharray="4" />
    <line x1="0" y1="100" x2="400" y2="100" stroke="var(--line)" stroke-dasharray="4" />
    <line x1="0" y1="140" x2="400" y2="140" stroke="var(--ink-faint)" stroke-width="1" />
    
    <!-- Area Fill -->
    <path class="growth-area" d="M0,140 L0,110 Q50,90 80,100 T160,80 T240,60 T320,40 T400,20 L400,140 Z" fill="url(#gradientPrimary)" opacity="0" />
    
    <!-- Line -->
    <path class="growth-line" d="M0,110 Q50,90 80,100 T160,80 T240,60 T320,40 T400,20" fill="none" stroke="var(--primary)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="600" stroke-dashoffset="600" />
    
    <!-- Points -->
    <circle class="growth-pt" cx="0" cy="110" r="5" fill="var(--surface)" stroke="var(--primary)" stroke-width="3" opacity="0" />
    <circle class="growth-pt" cx="80" cy="100" r="5" fill="var(--surface)" stroke="var(--primary)" stroke-width="3" opacity="0" />
    <circle class="growth-pt" cx="160" cy="80" r="5" fill="var(--surface)" stroke="var(--primary)" stroke-width="3" opacity="0" />
    <circle class="growth-pt" cx="240" cy="60" r="5" fill="var(--surface)" stroke="var(--primary)" stroke-width="3" opacity="0" />
    <circle class="growth-pt" cx="320" cy="40" r="5" fill="var(--surface)" stroke="var(--primary)" stroke-width="3" opacity="0" />
    <circle class="growth-pt" cx="400" cy="20" r="5" fill="var(--surface)" stroke="var(--primary)" stroke-width="3" opacity="0" />
    
    <!-- Gradient Def -->
    <defs>
      <linearGradient id="gradientPrimary" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="var(--primary)" stop-opacity="0.4" />
        <stop offset="100%" stop-color="var(--primary)" stop-opacity="0" />
      </linearGradient>
    </defs>
  </svg>
  
  <!-- X-Axis Labels -->
  <div style="display: flex; justify-content: space-between; margin-top: 8px; padding: 0 10px; color: var(--ink-faint); font-size: 0.75rem;">
    <span>Mar</span>
    <span>Apr</span>
    <span>May</span>
    <span>Jun</span>
    <span>Jul</span>
    <span>Aug</span>
  </div>
</div>
"""

bar_chart_div = soup.find('div', class_='bar-chart')
if bar_chart_div:
    # Check if parent is Client Growth panel
    parent = bar_chart_div.find_parent('div', class_='panel')
    if parent and 'Client Growth' in parent.text:
        bar_chart_div.replace_with(BeautifulSoup(growth_html, 'html.parser'))

with open('admin-clients.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))


# 2. Update admin-alerts.html (7-Day Alert Volume)
with open('admin-alerts.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

volume_html = """
<div class="svg-chart-container" style="position: relative; width: 100%; height: 140px; margin-top: 10px; display: flex; align-items: flex-end; justify-content: space-between; padding: 0 10px;">
  <!-- We will just use native div bars but heavily styled so they never fail -->
  <style>
    .v-bar-col { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; gap: 8px; height: 100%; }
    .v-bar-wrap { width: 100%; max-width: 24px; height: 100%; display: flex; align-items: flex-end; justify-content: center; background: rgba(0,0,0,0.03); border-radius: 6px; padding: 2px; }
    .v-bar-inner { width: 100%; border-radius: 4px; transform: scaleY(0); transform-origin: bottom; opacity: 0; }
    .v-bar-col span { font-size: 0.7rem; color: var(--ink-faint); font-weight: 500; }
  </style>
  
  <div class="v-bar-col"><div class="v-bar-wrap"><div class="v-bar-inner" style="height: 30%; background: var(--primary);"></div></div><span>M</span></div>
  <div class="v-bar-col"><div class="v-bar-wrap"><div class="v-bar-inner" style="height: 50%; background: var(--primary);"></div></div><span>T</span></div>
  <div class="v-bar-col"><div class="v-bar-wrap"><div class="v-bar-inner" style="height: 40%; background: var(--primary);"></div></div><span>W</span></div>
  <div class="v-bar-col"><div class="v-bar-wrap"><div class="v-bar-inner" style="height: 85%; background: var(--danger);"></div></div><span>T</span></div>
  <div class="v-bar-col"><div class="v-bar-wrap"><div class="v-bar-inner" style="height: 60%; background: var(--primary);"></div></div><span>F</span></div>
  <div class="v-bar-col"><div class="v-bar-wrap"><div class="v-bar-inner" style="height: 20%; background: var(--primary);"></div></div><span>S</span></div>
  <div class="v-bar-col"><div class="v-bar-wrap"><div class="v-bar-inner" style="height: 15%; background: var(--primary);"></div></div><span>S</span></div>
</div>
"""

bar_chart_div = soup.find('div', class_='bar-chart')
if bar_chart_div:
    parent = bar_chart_div.find_parent('div', class_='panel')
    if parent and '7-Day Alert Volume' in parent.text:
        bar_chart_div.replace_with(BeautifulSoup(volume_html, 'html.parser'))

with open('admin-alerts.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))

print('Updated both charts successfully.')
