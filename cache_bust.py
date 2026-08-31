import re

with open('Login.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'src="js/forms\.js.*?"', 'src="js/forms.js?v=2"', content)

with open('Login.html', 'w', encoding='utf-8') as f:
    f.write(content)
