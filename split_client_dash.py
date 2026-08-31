import re
import os

with open('client-dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Navigation Links
nav_links = """<nav class="nav-group" id="navGroup">
<div class="nav-pill" id="navPill"></div>
<a href="client-dashboard.html" class="nav-item"><i class="fas fa-home"></i> Overview</a>
<a href="client-sessions.html" class="nav-item"><i class="fas fa-video"></i> Sessions</a>
<a href="client-journal.html" class="nav-item"><i class="fas fa-book"></i> Journal</a>
<a href="client-resources.html" class="nav-item"><i class="fas fa-heart"></i> Resources</a>
<a href="client-settings.html" class="nav-item"><i class="fas fa-cog"></i> Settings</a>
<a class="nav-item" href="Login.html" style="text-decoration: none;"><i class="fas fa-sign-out-alt"></i> Logout</a>
</nav>"""
html = re.sub(r'<nav class="nav-group" id="navGroup">.*?</nav>', nav_links, html, flags=re.DOTALL)

# 2. Update CSS so .view is always block
html = html.replace('.view{ display:none; }', '.view{ display:block; }')
html = html.replace('.view.active{ display:block; }', '')

# 3. Extract the 5 views
views = {}
view_names = ['overview', 'sessions', 'journal', 'resources', 'settings']
for name in view_names:
    pattern = r'(<section class="view[^"]*" data-view-content="' + name + r'">.*?</section>)'
    match = re.search(pattern, html, re.DOTALL)
    if match:
        views[name] = match.group(1)

# 4. Remove all views from the main shell, we'll inject them one by one
shell_html = re.sub(r'<section class="view[^"]*" data-view-content=".*?">.*?</section>', '[[VIEW_CONTENT]]', html, flags=re.DOTALL)
# The above replace will insert multiple [[VIEW_CONTENT]]. We want only ONE.
shell_html = re.sub(r'(\[\[VIEW_CONTENT\]\]\s*<!-- ===== [A-Z]+ ===== -->\s*)+', '[[VIEW_CONTENT]]\n', shell_html)
shell_html = re.sub(r'\[\[VIEW_CONTENT\]\](?:\s*\[\[VIEW_CONTENT\]\])+', '[[VIEW_CONTENT]]', shell_html)

# 5. Update Javascript navigation logic
js_nav_logic = """  /* ================= Sidebar navigation ================= */
  const navGroup = document.getElementById('navGroup');
  const navPill = document.getElementById('navPill');
  const navItems = Array.from(document.querySelectorAll('.nav-item'));

  function movePill(item, animate){
    if(!item) return;
    const y = item.offsetTop;
    const h = item.offsetHeight;
    if (animate && !reduceMotion) gsap.to(navPill, { top: y, height: h, duration: 0.45, ease: 'power3.out' });
    else {
      navPill.style.top = y + 'px';
      navPill.style.height = h + 'px';
    }
  }

  // Set active based on current URL
  const currentPath = window.location.pathname.split('/').pop() || 'client-dashboard.html';
  navItems.forEach(item => {
    const href = item.getAttribute('href');
    if(href && href === currentPath) {
      item.classList.add('active');
    } else {
      item.classList.remove('active');
    }
  });

  window.addEventListener('resize', () => {
    const active = navItems.find(i => i.classList.contains('active'));
    if (active) movePill(active, false);
  });
  window.addEventListener('load', () => {
    const active = navItems.find(i => i.classList.contains('active'));
    if (active) {
      gsap.set(navPill, { opacity: 0 });
      movePill(active, false);
      gsap.to(navPill, { opacity: 1, duration: 0.4 });
    }
  });"""

shell_html = re.sub(r'/\* ================= Sidebar SPA navigation ================= \*/.*?window\.addEventListener\(\'load\', \(\) => \{.*?\n  \}\);\n', js_nav_logic, shell_html, flags=re.DOTALL)

# 6. Generate the files
file_mapping = {
    'overview': 'client-dashboard.html',
    'sessions': 'client-sessions.html',
    'journal': 'client-journal.html',
    'resources': 'client-resources.html',
    'settings': 'client-settings.html'
}

for name, filename in file_mapping.items():
    if name in views:
        # For overview, we might need to make sure the view class has 'active' just in case, but it's display:block anyway
        final_html = shell_html.replace('[[VIEW_CONTENT]]', views[name])
        
        # We need to clean up any remaining [[VIEW_CONTENT]] just in case
        final_html = final_html.replace('[[VIEW_CONTENT]]', '')
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"Created {filename}")

