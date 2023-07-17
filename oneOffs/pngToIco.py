from PIL import Image
import os
import mf

def convert_png_to_ico(png_path, ico_path):
    img = Image.open(png_path)
    img.save(ico_path, format='ICO', sizes=[(32,32)])

# Usage
pngPath = mf.browseForFile()
# Get the directory of the png file
pngDir = os.path.dirname(pngPath)
# Combine directory with the ico filename
icoPath = os.path.join(pngDir, 'icon.ico')
# Convert png to ico
convert_png_to_ico(pngPath, icoPath)
