import os
import re

files = [
    'admin-dashboard.html',
    'admin-clients.html',
    'admin-therapists.html',
    'admin-reports.html',
    'admin-alerts.html',
    'admin-settings.html',
    'client-dashboard.html'
]

NEW_SCRIPT = """// Dynamic Username - runs immediately
(function() {
  var user = localStorage.getItem('currentUser') || 'Admin';
  var formatted = user.charAt(0).toUpperCase() + user.slice(1);
  function applyUser() {
    var nameEl = document.getElementById('userName');
    var avatarEl = document.getElementById('userAvatar');
    if (nameEl) nameEl.textContent = formatted;
    if (avatarEl) avatarEl.textContent = formatted.substring(0, 2).toUpperCase();
    document.querySelectorAll('h1').forEach(function(h1) {
      if (h1.textContent.indexOf('Good morning') !== -1) {
        h1.textContent = 'Good morning, ' + formatted + '.';
      }
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyUser);
  } else {
    applyUser();
  }
})();"""

for filename in files:
    if not os.path.exists(filename): continue
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add id="userName" and id="userAvatar" to admin-id elements
    html = re.sub(
        r'<div class="admin-id"><div class="avatar"(?! id=)',
        '<div class="admin-id"><div class="avatar" id="userAvatar"',
        html
    )
    html = re.sub(
        r'<div class="admin-id"><div class="avatar" id="userAvatar">[^<]+</div><div class="txt"><p(?! id=)',
        lambda m: m.group(0).replace('<p', '<p id="userName"'),
        html
    )
    # Handle client-id too
    html = re.sub(
        r'<div class="client-id"><div class="avatar"(?! id=)',
        '<div class="client-id"><div class="avatar" id="userAvatar"',
        html
    )
    html = re.sub(
        r'<div class="client-id"><div class="avatar" id="userAvatar">[^<]+</div><div class="txt"><p(?! id=)',
        lambda m: m.group(0).replace('<p', '<p id="userName"'),
        html
    )

    # 2. Remove all old dynamic username scripts (any variant)
    html = re.sub(r'// Dynamic Username.*?}\)\(\);', '', html, flags=re.DOTALL)
    html = re.sub(r'// Dynamic Username.*?}\);', '', html, flags=re.DOTALL)

    # 3. Inject the new clean script just before </script> at end of file
    html = html.rstrip()
    # Find the last </script> and insert before it
    idx = html.rfind('</script>')
    if idx != -1:
        html = html[:idx] + "\n" + NEW_SCRIPT + "\n" + html[idx:]

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Fixed: {filename}")

print("Done.")
