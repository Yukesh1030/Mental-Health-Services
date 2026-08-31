import re

files = ['admin-clients.html', 'admin-alerts.html']

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Fix SVG case sensitivity ruined by BeautifulSoup
    content = content.replace('viewbox=', 'viewBox=')
    content = content.replace('preserveaspectratio=', 'preserveAspectRatio=')
    content = content.replace('<lineargradient', '<linearGradient')
    content = content.replace('</lineargradient>', '</linearGradient>')
    content = content.replace('stop-color', 'stop-color') # valid
    content = content.replace('stroke-dasharray', 'stroke-dasharray') # valid
    
    # Fix the missing var(--danger)
    content = content.replace('var(--danger)', 'var(--accent)')
    
    # Ensure opacity defaults are correct for JS
    # If the growth-area has opacity 0, and GSAP fails to trigger, they stay invisible.
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print('SVG Casing and CSS variables fixed.')
