from bs4 import BeautifulSoup
import re

with open('admin-clients.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

script = soup.find_all('script')[-1]
if script:
    new_js = """
    /* ---------- Custom Chart Animations ---------- */
    function animateCustomCharts() {
      if (typeof gsap === 'undefined') return;
      
      // Animate pie segments (stroke-dashoffset from 157.08 to target)
      gsap.utils.toArray('.pie-segment').forEach((segment) => {
        const targetOffset = segment.getAttribute('stroke-dashoffset');
        const delay = parseFloat(segment.getAttribute('data-delay') || 0);
        
        // Start from fully hidden
        gsap.set(segment, { strokeDashoffset: 157.08 });
        
        // Animate to target
        gsap.to(segment, { 
          strokeDashoffset: targetOffset, 
          duration: 1.5, 
          delay: delay + 0.2, 
          ease: 'power3.out' 
        });
      });
      
      // Animate horizontal legend bars
      gsap.utils.toArray('.legend-bar').forEach((bar, i) => {
        const width = bar.getAttribute('data-width');
        gsap.set(bar, { width: '0%' });
        gsap.to(bar, { 
          width: width, 
          duration: 1.2, 
          delay: 0.5 + (i * 0.15), 
          ease: 'power2.out' 
        });
      });
    }
    
    // Call it when AOS is done or on load
    window.addEventListener('load', animateCustomCharts);
    """
    
    # Append the js safely
    script.string = (script.string or '') + new_js

with open('admin-clients.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))

print('Chart JS added successfully.')
