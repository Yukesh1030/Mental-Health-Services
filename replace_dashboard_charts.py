from bs4 import BeautifulSoup

# Update admin-dashboard.html
with open('admin-dashboard.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

growth_html = """
<div class="svg-chart-container" style="position: relative; width: 100%; height: 160px; margin-top: 10px;">
  <svg viewBox="0 0 400 160" preserveAspectRatio="none" style="width: 100%; height: 100%; overflow: visible;">
    <line x1="0" y1="20" x2="400" y2="20" stroke="var(--line)" stroke-dasharray="4" />
    <line x1="0" y1="60" x2="400" y2="60" stroke="var(--line)" stroke-dasharray="4" />
    <line x1="0" y1="100" x2="400" y2="100" stroke="var(--line)" stroke-dasharray="4" />
    <line x1="0" y1="140" x2="400" y2="140" stroke="var(--ink-faint)" stroke-width="1" />
    <path class="growth-area" d="M0,140 L0,110 Q50,90 80,100 T160,80 T240,60 T320,40 T400,20 L400,140 Z" fill="url(#gradientPrimary)" opacity="1" />
    <path class="growth-line" d="M0,110 Q50,90 80,100 T160,80 T240,60 T320,40 T400,20" fill="none" stroke="var(--primary)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="600" />
    <circle class="growth-pt" cx="0" cy="110" r="5" fill="var(--surface)" stroke="var(--primary)" stroke-width="3" opacity="1" />
    <circle class="growth-pt" cx="80" cy="100" r="5" fill="var(--surface)" stroke="var(--primary)" stroke-width="3" opacity="1" />
    <circle class="growth-pt" cx="160" cy="80" r="5" fill="var(--surface)" stroke="var(--primary)" stroke-width="3" opacity="1" />
    <circle class="growth-pt" cx="240" cy="60" r="5" fill="var(--surface)" stroke="var(--primary)" stroke-width="3" opacity="1" />
    <circle class="growth-pt" cx="320" cy="40" r="5" fill="var(--surface)" stroke="var(--primary)" stroke-width="3" opacity="1" />
    <circle class="growth-pt" cx="400" cy="20" r="5" fill="var(--surface)" stroke="var(--primary)" stroke-width="3" opacity="1" />
    <defs>
      <linearGradient id="gradientPrimary" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="var(--primary)" stop-opacity="0.4" />
        <stop offset="100%" stop-color="var(--primary)" stop-opacity="0" />
      </linearGradient>
    </defs>
  </svg>
  <div style="display: flex; justify-content: space-between; margin-top: 8px; padding: 0 10px; color: var(--ink-faint); font-size: 0.75rem;">
    <span>Mar</span><span>Apr</span><span>May</span><span>Jun</span><span>Jul</span><span>Aug</span>
  </div>
</div>
"""

volume_html = """
<div class="svg-chart-container" style="position: relative; width: 100%; height: 140px; margin-top: 10px; display: flex; align-items: flex-end; justify-content: space-between; padding: 0 10px;">
  <style>
    .v-bar-col { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; gap: 8px; height: 100%; }
    .v-bar-wrap { width: 100%; max-width: 24px; height: 100%; display: flex; align-items: flex-end; justify-content: center; background: rgba(0,0,0,0.03); border-radius: 6px; padding: 2px; }
    .v-bar-inner { width: 100%; border-radius: 4px; transform-origin: bottom; opacity: 1; }
    .v-bar-col span { font-size: 0.7rem; color: var(--ink-faint); font-weight: 500; }
  </style>
  <div class="v-bar-col"><div class="v-bar-wrap"><div class="v-bar-inner" style="height: 30%; background: var(--primary);"></div></div><span>M</span></div>
  <div class="v-bar-col"><div class="v-bar-wrap"><div class="v-bar-inner" style="height: 50%; background: var(--primary);"></div></div><span>T</span></div>
  <div class="v-bar-col"><div class="v-bar-wrap"><div class="v-bar-inner" style="height: 40%; background: var(--primary);"></div></div><span>W</span></div>
  <div class="v-bar-col"><div class="v-bar-wrap"><div class="v-bar-inner" style="height: 85%; background: var(--accent);"></div></div><span>T</span></div>
  <div class="v-bar-col"><div class="v-bar-wrap"><div class="v-bar-inner" style="height: 60%; background: var(--primary);"></div></div><span>F</span></div>
  <div class="v-bar-col"><div class="v-bar-wrap"><div class="v-bar-inner" style="height: 20%; background: var(--primary);"></div></div><span>S</span></div>
  <div class="v-bar-col"><div class="v-bar-wrap"><div class="v-bar-inner" style="height: 15%; background: var(--primary);"></div></div><span>S</span></div>
</div>
"""

bar_charts = soup.find_all('div', class_='bar-chart')
for bc in bar_charts:
    parent = bc.find_parent('div', class_='panel')
    if parent:
        if 'Client Growth' in parent.text:
            bc.replace_with(BeautifulSoup(growth_html, 'html.parser'))
        elif 'Alert Volume' in parent.text:
            bc.replace_with(BeautifulSoup(volume_html, 'html.parser'))

# Append JS
script = soup.find_all('script')[-1]
if script:
    new_js = """
    // Custom GSAP for Charts
    window.addEventListener('load', () => {
      if (typeof gsap !== 'undefined') {
        gsap.from('.growth-area', { opacity: 0, duration: 1.5, ease: 'power2.inOut', delay: 0.2 });
        gsap.from('.growth-line', { strokeDashoffset: 600, duration: 1.5, ease: 'power2.out', delay: 0.2 });
        gsap.from('.growth-pt', { opacity: 0, duration: 0.5, stagger: 0.1, delay: 1.2 });
        gsap.from('.v-bar-inner', { scaleY: 0, opacity: 0, duration: 0.8, stagger: 0.08, ease: 'back.out(1.5)', delay: 0.2 });
      }
    });
    """
    script.string = (script.string or '') + new_js

with open('admin-dashboard.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))

print('Updated dashboard charts.')
