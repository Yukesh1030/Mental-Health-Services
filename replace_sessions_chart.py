from bs4 import BeautifulSoup

# Update admin-sessions.html
with open('admin-sessions.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

volume_html = """
<div class="svg-chart-container" style="position: relative; width: 100%; height: 140px; margin-top: 10px; display: flex; align-items: flex-end; justify-content: space-around; padding: 0 10px;">
  <style>
    .w-bar-col { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; gap: 8px; height: 100%; }
    .w-bar-wrap { width: 100%; max-width: 32px; height: 100%; display: flex; align-items: flex-end; justify-content: center; background: rgba(0,0,0,0.03); border-radius: 6px; padding: 2px; }
    .w-bar-inner { width: 100%; border-radius: 4px; transform-origin: bottom; opacity: 1; }
    .w-bar-col span { font-size: 0.75rem; color: var(--ink-faint); font-weight: 500; }
  </style>
  <div class="w-bar-col"><div class="w-bar-wrap"><div class="w-bar-inner" style="height: 40%; background: var(--primary);"></div></div><span>W1</span></div>
  <div class="w-bar-col"><div class="w-bar-wrap"><div class="w-bar-inner" style="height: 60%; background: var(--primary);"></div></div><span>W2</span></div>
  <div class="w-bar-col"><div class="w-bar-wrap"><div class="w-bar-inner" style="height: 85%; background: var(--gold);"></div></div><span>W3</span></div>
  <div class="w-bar-col"><div class="w-bar-wrap"><div class="w-bar-inner" style="height: 50%; background: var(--primary);"></div></div><span>W4</span></div>
</div>
"""

bar_charts = soup.find_all('div', class_='bar-chart')
for bc in bar_charts:
    parent = bc.find_parent('div', class_='panel')
    if parent and '4-Week Volume' in parent.text:
        bc.replace_with(BeautifulSoup(volume_html, 'html.parser'))

# Append JS
script = soup.find_all('script')[-1]
if script:
    new_js = """
    // Custom GSAP for Volume Bar Chart
    window.addEventListener('load', () => {
      if (typeof gsap !== 'undefined') {
        gsap.from('.w-bar-inner', { scaleY: 0, opacity: 0, duration: 0.8, stagger: 0.1, ease: 'back.out(1.5)', delay: 0.2 });
      }
    });
    """
    script.string = (script.string or '') + new_js

with open('admin-sessions.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))

print('Updated session chart.')
