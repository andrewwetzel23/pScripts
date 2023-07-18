from PIL import Image

import mf

def convert_png_to_ico(png_path, ico_path):
    img = Image.open(png_path)
    img.save(ico_path, format='ICO', sizes=[(32,32)])

# Usage
pngPath = mf.browseForFile()
convert_png_to_ico(pngPath, 'icon.ico')
