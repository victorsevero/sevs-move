import cv2
import numpy as np
import os
import image_slicer
from PIL import Image

def resize128(file):
    basedim = 128
    img = Image.open(file)
    wpercent = (basedim/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basedim,hsize), Image.ANTIALIAS)
    img.save(file)

def main():
    path_bg = 'icons_with_bg\\'
    path_slices = 'slices\\'
    slices_dir = os.listdir(path_slices)

    screen = cv2.imread('screen.png')
    template = cv2.imread('icons_with_bg\\717.png')
    dim = 175
    y, x = 714, 15

    crop = screen[y:y+6*dim, x:x+6*dim]
    cv2.imwrite('board.png', crop)
    tiles = image_slicer.slice('board.png', 36, save=False)
    image_slicer.save_tiles(tiles, directory=path_slices)

    shuffle_move_pkmns = ['302.png', '491.png', '649.png', '717.png']

    for slice in slices_dir:
        # from IPython import embed; embed()
        resize128(path_slices + slice)
        slice_img = cv2.imread(path_slices + slice)
        res_match = 0
        best_match = ''
        for pkmn in shuffle_move_pkmns:
            shuffle_move_icon = cv2.imread(path_bg + pkmn)
            res = cv2.matchTemplate(slice_img, shuffle_move_icon, cv2.TM_CCOEFF_NORMED)
            if res > res_match:
                res_match = res
                best_match = pkmn
        # print("%s %s" %(slice, best_match))


if __name__ == '__main__':
    main()
