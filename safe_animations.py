import re

files = ['admin-clients.html', 'admin-alerts.html']

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # admin-clients.html: Remove inline opacity="0" and stroke-dashoffset="600"
    content = content.replace('opacity="0"', 'opacity="1"')
    content = content.replace('stroke-dashoffset="600"', '') # let default stroke show
    
    # Change gsap.to to gsap.from for admin-clients
    # Find: gsap.to('.growth-area', { opacity: 1, duration: 1.5, ease: 'power2.inOut', delay: 0.2 });
    content = content.replace("gsap.to('.growth-area', { opacity: 1,", "gsap.from('.growth-area', { opacity: 0,")
    content = content.replace("gsap.to('.growth-line', { strokeDashoffset: 0,", "gsap.from('.growth-line', { strokeDashoffset: 600,")
    content = content.replace("gsap.to('.growth-pt', { opacity: 1,", "gsap.from('.growth-pt', { opacity: 0,")
    
    # admin-alerts.html: Remove transform: scaleY(0); and opacity: 0; from CSS
    content = content.replace('transform: scaleY(0); transform-origin: bottom; opacity: 0;', 'transform-origin: bottom;')
    
    # Change gsap.to to gsap.from for admin-alerts
    content = content.replace("gsap.to('.v-bar-inner', { scaleY: 1, opacity: 1,", "gsap.from('.v-bar-inner', { scaleY: 0, opacity: 0,")
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print('Updated animations to use gsap.from and removed default hidden states.')
