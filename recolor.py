from PIL import Image

def recolor():
    img = Image.open('assets/Brand-logo.webp').convert('RGBA')
    data = img.getdata()
    new_data = []
    target_color = (49, 92, 85)
    
    for item in data:
        if item[3] > 0:
            # Optionally blend with target_color based on luminance, but a simple replace is fine if the logo is a solid color
            new_data.append((target_color[0], target_color[1], target_color[2], item[3]))
        else:
            new_data.append(item)
            
    img.putdata(new_data)
    img.save('assets/Brand-logo.webp', 'WEBP')

recolor()
