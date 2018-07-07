import cv2
import numpy as np
import os
import image_slicer
from PIL import Image
from pynput.keyboard import Key, Controller
import time
import subprocess
import pandas as pd

PATH_BG = 'icons_with_bg\\'
PATH_SLICES = 'slices\\'

def take_screenshot():
    subprocess.call('screenshot.bat')

def convert_png_to_key(pkmn_list, board):
    key_list = ['a', 's', 'e', 'r', 'g',
                'd', 'w', 't', 'q', 'b',
                'c', 'x', 'v', 'z', 'h',
                'i', 'j', 'k', 'l', 'm',
                'n', 'o', 'p', 'u', 'y']
    df = pd.read_csv('pokemon.csv')
    df = df.set_index('species_id')

    png_to_key = dict()
    for pkmn in pkmn_list:
        png_to_key[pkmn] = key_list[pkmn_list.index(pkmn)]

    board = [png_to_key[pkmn] for pkmn in board]

    return board

def resize128(file):
    basedim = 128
    img = Image.open(file)
    wpercent = (basedim/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basedim,hsize), Image.ANTIALIAS)
    img.save(file)

def main():
    if not os.path.exists(PATH_SLICES):
        os.makedirs(PATH_SLICES)

    slices_dir = os.listdir(PATH_SLICES)

    screen = cv2.imread('screen.png')
    template = cv2.imread('icons_with_bg\\717.png')
    dim = 175
    y, x = 714, 15

    crop = screen[y:y+6*dim, x:x+6*dim]
    cv2.imwrite('board.png', crop)
    tiles = image_slicer.slice('board.png', 36, save=False)
    image_slicer.save_tiles(tiles, directory=PATH_SLICES)

    pkmn_imgs = ['302.png', '491.png', '649.png', '717.png']
    board = []

    for slice in slices_dir:
        resize128(PATH_SLICES + slice)
        slice_img = cv2.imread(PATH_SLICES + slice)
        res_match = 0
        best_match = ''
        for pkmn in pkmn_imgs:
            png = cv2.imread(PATH_BG + pkmn)
            res = cv2.matchTemplate(slice_img, png, cv2.TM_CCOEFF_NORMED)
            if res > res_match:
                res_match = res
                best_match = pkmn
        board.append(best_match)

    key_board = convert_png_to_key(pkmn_imgs, board)
    # from IPython import embed; embed()
    keyboard = Controller()
    print('alterna carai')
    time.sleep(2)

    for key in key_board:
        keyboard.press(key)
        keyboard.release(key)

if __name__ == '__main__':
    main()
