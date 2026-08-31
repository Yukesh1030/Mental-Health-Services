from bs4 import BeautifulSoup
import re

with open('admin-clients.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Find the panel containing "Client Roster"
roster_panel = None
for h2 in soup.find_all('h2'):
    if 'Client Roster' in h2.text:
        roster_panel = h2.find_parent('div', class_='panel')
        break

if roster_panel:
    # Replace its contents with a chart
    new_html = """
    <div class="panel-head" style="margin-bottom: 20px;">
      <h2>Client Risk Distribution</h2>
      <span class="legend">Current Active Clients</span>
    </div>
    
    <div class="chart-container" style="display: flex; flex-wrap: wrap; gap: 40px; align-items: center; justify-content: center; min-height: 250px;">
      
      <!-- Pie Chart SVG -->
      <div class="pie-wrapper" style="position: relative; width: 200px; height: 200px;">
        <svg viewBox="0 0 100 100" style="transform: rotate(-90deg); width: 100%; height: 100%; border-radius: 50%;">
          <!-- Low Risk: 60% -->
          <circle class="pie-segment" cx="50" cy="50" r="25" fill="transparent" stroke="var(--primary)" stroke-width="50" stroke-dasharray="94.2 157.08" stroke-dashoffset="0" data-delay="0.1" />
          <!-- Medium Risk: 25% -->
          <circle class="pie-segment" cx="50" cy="50" r="25" fill="transparent" stroke="var(--gold)" stroke-width="50" stroke-dasharray="39.27 157.08" stroke-dashoffset="-94.2" data-delay="0.3" />
          <!-- High Risk: 15% -->
          <circle class="pie-segment" cx="50" cy="50" r="25" fill="transparent" stroke="var(--accent)" stroke-width="50" stroke-dasharray="23.56 157.08" stroke-dashoffset="-133.47" data-delay="0.5" />
        </svg>
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 130px; height: 130px; background: var(--surface); border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-direction: column; box-shadow: inset 0 4px 10px rgba(0,0,0,0.05);">
            <h3 style="margin:0; font-size: 1.8rem; color: var(--ink);">284</h3>
            <span style="font-size: 0.75rem; color: var(--ink-soft); text-transform: uppercase; letter-spacing: 0.05em;">Total</span>
        </div>
      </div>
      
      <!-- Legend & Bar Chart -->
      <div class="chart-legend" style="display: flex; flex-direction: column; gap: 16px; flex: 1; min-width: 250px;">
        
        <div class="legend-item" style="display: flex; align-items: center; gap: 12px;">
          <div style="width: 16px; height: 16px; border-radius: 4px; background: var(--primary);"></div>
          <div style="flex: 1;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
              <span style="font-weight: 500; font-size: 0.9rem;">Low Risk</span>
              <span style="font-weight: 600; font-size: 0.9rem;">60%</span>
            </div>
            <div style="width: 100%; height: 6px; background: var(--line); border-radius: 3px; overflow: hidden;">
              <div class="legend-bar" style="height: 100%; background: var(--primary); width: 0%;" data-width="60%"></div>
            </div>
          </div>
        </div>

        <div class="legend-item" style="display: flex; align-items: center; gap: 12px;">
          <div style="width: 16px; height: 16px; border-radius: 4px; background: var(--gold);"></div>
          <div style="flex: 1;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
              <span style="font-weight: 500; font-size: 0.9rem;">Medium Risk</span>
              <span style="font-weight: 600; font-size: 0.9rem;">25%</span>
            </div>
            <div style="width: 100%; height: 6px; background: var(--line); border-radius: 3px; overflow: hidden;">
              <div class="legend-bar" style="height: 100%; background: var(--gold); width: 0%;" data-width="25%"></div>
            </div>
          </div>
        </div>

        <div class="legend-item" style="display: flex; align-items: center; gap: 12px;">
          <div style="width: 16px; height: 16px; border-radius: 4px; background: var(--accent);"></div>
          <div style="flex: 1;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
              <span style="font-weight: 500; font-size: 0.9rem;">High Risk</span>
              <span style="font-weight: 600; font-size: 0.9rem;">15%</span>
            </div>
            <div style="width: 100%; height: 6px; background: var(--line); border-radius: 3px; overflow: hidden;">
              <div class="legend-bar" style="height: 100%; background: var(--accent); width: 0%;" data-width="15%"></div>
            </div>
          </div>
        </div>

      </div>
    </div>
    """
    
    # We clear the existing panel content
    roster_panel.clear()
    # Insert new HTML
    new_soup = BeautifulSoup(new_html, 'html.parser')
    for elem in new_soup.children:
        roster_panel.append(elem)

with open('admin-clients.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))

print('Chart HTML added successfully.')
