import os
import re

files_to_update = [
    "index.html",
    "About.html",
    "Services.html",
    "Therapists.html",
    "Resources.html",
    "Contact.html"
]

for filename in files_to_update:
    filepath = os.path.join(r"d:\yukesh\projects\Mental Health Services", filename)
    if not os.path.exists(filepath):
        print(f"Not found: {filepath}")
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The HTML files have clear sections.
    # Navbar is inside <nav class="navbar"> ... </nav>
    # Footer is inside <footer class="footer"> ... </footer>
    
    # We will split the file by <nav ... </nav> and <footer ... </footer> 
    # to avoid modifying links inside them.
    
    # Simple approach: find <nav>...</nav> and <footer>...</footer>
    # and replace them with placeholders, then do a regex replace on the rest, 
    # then restore the placeholders.
    
    nav_pattern = re.compile(r'(<nav.*?</nav>)', re.DOTALL | re.IGNORECASE)
    footer_pattern = re.compile(r'(<footer.*?</footer>)', re.DOTALL | re.IGNORECASE)
    
    nav_match = nav_pattern.search(content)
    footer_match = footer_pattern.search(content)
    
    nav_text = nav_match.group(1) if nav_match else ""
    footer_text = footer_match.group(1) if footer_match else ""
    
    # Replace nav and footer with placeholders
    temp_content = content
    if nav_text:
        temp_content = temp_content.replace(nav_text, "<!--NAV_PLACEHOLDER-->")
    if footer_text:
        temp_content = temp_content.replace(footer_text, "<!--FOOTER_PLACEHOLDER-->")
        
    # Replace all href="..." with href="404.html" inside the remaining content
    # Note: <a href="...">...</a>
    # We use a lambda to only replace href inside <a> tags
    def replace_a_href(match):
        return re.sub(r'href="[^"]*"', 'href="404.html"', match.group(0))
        
    temp_content = re.sub(r'<a\s+[^>]*>', replace_a_href, temp_content, flags=re.IGNORECASE)
    
    # Also fix form action to 404.html just in case
    temp_content = re.sub(r'action="[^"]*"', 'action="404.html"', temp_content)
    
    # Restore nav and footer
    if nav_text:
        temp_content = temp_content.replace("<!--NAV_PLACEHOLDER-->", nav_text)
    if footer_text:
        temp_content = temp_content.replace("<!--FOOTER_PLACEHOLDER-->", footer_text)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(temp_content)
        
    print(f"Updated {filename}")
