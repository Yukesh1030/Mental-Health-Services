from bs4 import BeautifulSoup

# 1. Update admin-clients.html JS
with open('admin-clients.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

script = soup.find_all('script')[-1]
if script:
    new_js = """
    // Custom GSAP for Growth Line Chart
    window.addEventListener('load', () => {
      if (typeof gsap !== 'undefined') {
        gsap.to('.growth-area', { opacity: 1, duration: 1.5, ease: 'power2.inOut', delay: 0.2 });
        gsap.to('.growth-line', { strokeDashoffset: 0, duration: 1.5, ease: 'power2.out', delay: 0.2 });
        gsap.to('.growth-pt', { opacity: 1, duration: 0.5, stagger: 0.1, delay: 1.2 });
      }
    });
    """
    script.string = (script.string or '') + new_js

with open('admin-clients.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))


# 2. Update admin-alerts.html JS
with open('admin-alerts.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

script = soup.find_all('script')[-1]
if script:
    new_js = """
    // Custom GSAP for Volume Bar Chart
    window.addEventListener('load', () => {
      if (typeof gsap !== 'undefined') {
        gsap.to('.v-bar-inner', { scaleY: 1, opacity: 1, duration: 0.8, stagger: 0.08, ease: 'back.out(1.5)', delay: 0.2 });
      }
    });
    """
    script.string = (script.string or '') + new_js

with open('admin-alerts.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))

print('Chart animations appended successfully.')
