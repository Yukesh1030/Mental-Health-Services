import glob
import re
import os

html_files = glob.glob('*.html')

JS_SCRIPT = """
<!-- Dynamic Profile Update -->
<script>
(function() {
    function updateProfile() {
        var user = localStorage.getItem('currentUser');
        if (!user) user = 'Admin';
        
        // Format the name: replace dots/underscores with space and capitalize each word
        var formatted = user.replace(/[._]/g, ' ').split(' ').map(function(word) {
            return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
        }).join(' ');

        // Get initials (up to 2 letters)
        var initials = formatted.split(' ').map(function(w){return w[0];}).join('').substring(0, 2).toUpperCase();

        var nameEl = document.getElementById('userName');
        var avatarEl = document.getElementById('userAvatar');
        
        if (nameEl) nameEl.textContent = formatted;
        if (avatarEl) avatarEl.textContent = initials;

        document.querySelectorAll('h1').forEach(function(h1) {
            if (h1.textContent.indexOf('Good morning') !== -1) {
                h1.textContent = 'Good morning, ' + formatted + '.';
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', updateProfile);
    } else {
        updateProfile();
    }
})();
</script>
"""

for file in html_files:
    if file in ['404.html', 'About.html', 'Contact.html', 'index.html', 'Login.html', 'Resources.html', 'Services.html', 'Signup.html', 'Therapists.html']:
        continue
        
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Clean up old dynamic username script
    html = re.sub(r'// Dynamic Username.*?\n}\)\(\);', '', html, flags=re.DOTALL)
    html = re.sub(r'// Dynamic Username.*?}\)\(\);', '', html, flags=re.DOTALL)
    html = re.sub(r'<!-- Dynamic Profile Update -->.*?</script>', '', html, flags=re.DOTALL)

    # 2. Fix admin-id profile structure if it's not having id
    html = re.sub(
        r'<div class="admin-id">\s*<div class="avatar"(?! id=)',
        '<div class="admin-id"><div class="avatar" id="userAvatar"',
        html
    )
    html = re.sub(
        r'<div class="admin-id">\s*<div class="avatar" id="userAvatar">[^<]+</div>\s*<div class="txt">\s*<p(?! id=)',
        lambda m: m.group(0).replace('<p', '<p id="userName"'),
        html
    )
    
    # 3. For client dashboard, if it has <div class="avatar">AV</div> but no name
    if file == 'client-dashboard.html':
        html = re.sub(
            r'<div class="avatar">AV</div>',
            '<div class="client-id" style="display:flex; align-items:center; gap:10px;"><div class="avatar" id="userAvatar">AV</div><div class="txt" style="display:none;"><p id="userName">User</p></div></div>',
            html
        )
        # Wait, the user said "in profile section name should be displayed".
        # So I will make the text visible in client-dashboard as well.
        html = re.sub(
            r'<div class="client-id" style="display:flex; align-items:center; gap:10px;"><div class="avatar" id="userAvatar">AV</div><div class="txt" style="display:none;">',
            '<div class="client-id" style="display:flex; align-items:center; gap:10px;"><div class="avatar" id="userAvatar">AV</div><div class="txt" style="display:block; text-align:left; line-height:1.2;">',
            html
        )
        html = re.sub(
            r'<div class="avatar">AV</div>',
            '<div class="client-id" style="display:flex; align-items:center; gap:10px;"><div class="avatar" id="userAvatar">AV</div><div class="txt" style="display:block; text-align:left; line-height:1.2;"><p id="userName" style="font-weight:600; color:var(--ink); font-size:0.86rem; margin:0;">User</p><p style="font-size:0.75rem; color:var(--ink-faint); margin:0;">Client</p></div></div>',
            html
        )
        # also update existing client-id if present
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

    # 4. Inject script before </body>
    if '</body>' in html:
        html = html.replace('</body>', JS_SCRIPT + '\n</body>')
    else:
        html += JS_SCRIPT
        
    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Updated {file}")
