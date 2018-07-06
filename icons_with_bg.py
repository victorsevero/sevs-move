import os
from PIL import Image

path_icons = 'icons\\'
path_bg = 'icons_with_bg\\'
icons_dir = os.listdir(path_icons)
train_dir = os.listdir(path_bg)

for file in icons_dir:
    with open(path_icons + file, 'rb') as fp:
        background = Image.open('bg.png')
        icon = Image.open(fp).convert('RGBA')
        x, y = icon.size
        background.paste(icon, (0, 0, x, y), icon)
        background.save(path_bg + '%s.png' %file[0:-4], format='png')
