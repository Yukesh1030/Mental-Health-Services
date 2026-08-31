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

replacement = """    function animateBarCharts(scope){
      const bars = (scope || document).querySelectorAll('[data-chart] .bar');
      bars.forEach((bar, i) => {
        // Read the inline --h style
        let h = bar.parentElement.style.getPropertyValue('--h');
        if (!h) h = window.getComputedStyle(bar.parentElement).getPropertyValue('--h');
        if (!h) h = '50%'; // fallback
        
        // Ensure height is set and element is visible natively first
        bar.style.height = h;
        bar.style.transform = 'scaleY(0)';
        bar.style.transformOrigin = 'bottom';
        bar.style.opacity = '1';
        
        if (typeof gsap !== 'undefined') {
          gsap.to(bar, { scaleY: 1, duration: 0.7, delay: 0.1 + i * 0.06, ease: 'back.out(1.5)' });
        } else {
          bar.style.transform = 'scaleY(1)';
        }
      });
    }"""

for f in files:
    if not os.path.exists(f): continue
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace the animateBarCharts function
    content = re.sub(r'    function animateBarCharts\(scope\)\{.*?    \}', replacement, content, flags=re.DOTALL)

    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print('Updated animateBarCharts successfully.')
