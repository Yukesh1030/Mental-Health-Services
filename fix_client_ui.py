import glob
import re

html_files = glob.glob('client-*.html')

CHART_JS_CDN = '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'
CHART_INIT = """
  /* ---------- Chart.js Mood Chart ---------- */
  const moodCtx = document.getElementById('moodChartCanvas');
  if (moodCtx) {
    new Chart(moodCtx, {
      type: 'line',
      data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [{
          label: 'Mood Level',
          data: [6, 7, 5, 8, 7, 9, 7.2],
          borderColor: '#E8846B',
          backgroundColor: 'rgba(232, 132, 107, 0.15)',
          borderWidth: 3,
          pointBackgroundColor: '#E8846B',
          pointRadius: 4,
          fill: true,
          tension: 0.4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: {
            display: false,
            min: 0,
            max: 10
          },
          x: {
            grid: { display: false, drawBorder: false }
          }
        }
      }
    });
  }
"""

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update Logo in Sidebar
    logo_pattern = r'<div class="brand">\s*<svg.*?</svg>\s*<div><span>Haven</span><small>Your space</small></div>'
    new_logo = r'<div class="brand">\n<img alt="STACKLY Wellness" src="assets/Brand-logo.webp" style="height: 32px; width: auto;"/>'
    html = re.sub(logo_pattern, new_logo, html, flags=re.DOTALL)

    # 2. Update mini logo
    mini_logo_pattern = r'<div class="brand-mini">\s*<svg.*?</svg>\s*<span>Haven</span>\s*</div>'
    new_mini_logo = r'<div class="brand-mini">\n<img alt="STACKLY Wellness" src="assets/Brand-logo.webp" style="height: 24px; width: auto;"/>\n</div>'
    html = re.sub(mini_logo_pattern, new_mini_logo, html, flags=re.DOTALL)

    # 3. Add text-decoration: none to .nav-item
    html = html.replace('.nav-item{', '.nav-item{ text-decoration: none;')

    # 4. If it's client-dashboard.html, add the chart
    if file == 'client-dashboard.html':
        chart_pattern = r'<div class="mood-chart" id="moodChart">.*?</div>\s*<p style'
        new_chart = r'<div style="height: 160px; margin-bottom: 20px;"><canvas id="moodChartCanvas"></canvas></div>\n<p style'
        html = re.sub(chart_pattern, new_chart, html, flags=re.DOTALL)
        
        # Add CDN if not exists
        if 'chart.js' not in html:
            html = html.replace('</head>', f'{CHART_JS_CDN}\n</head>')
            
        # Add chart init script
        if 'moodChartCanvas' in html and 'new Chart(' not in html:
            html = html.replace('/* ---------- Count-up stats ---------- */', CHART_INIT + '\n  /* ---------- Count-up stats ---------- */')
            
        # Remove old GSAP mood chart init
        html = re.sub(r'/\* ---------- Mood chart grow-in ---------- \*/.*?animateMoodChart\(\);', '', html, flags=re.DOTALL)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Updated {file}")
