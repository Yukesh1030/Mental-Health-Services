from bs4 import BeautifulSoup
import re

with open('admin-settings.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

profile_rows = soup.find_all('div', class_='form-row')
if profile_rows:
    panel = profile_rows[0].find_parent('div', class_='panel')
    if panel and not panel.find('form'):
        form = soup.new_tag('form', action='404.html', method='GET')
        # Skip the panel-head, wrap the rest
        children = list(panel.children)
        for child in children:
            if child.name == 'div' and 'panel-head' in child.get('class', []):
                continue
            form.append(child.extract())
        
        # Add a submit button
        submit_btn = soup.new_tag('button', type='submit', attrs={'class': 'btn primary'})
        submit_btn.string = 'Save Changes'
        submit_btn['style'] = 'margin-top: 16px;'
        form.append(submit_btn)
        
        panel.append(form)
        
        # Make inputs required
        for inp in form.find_all('input'):
            if inp.get('type') != 'file':
                inp['required'] = ''

with open('admin-settings.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))

print('Fixed admin-settings.html form')
