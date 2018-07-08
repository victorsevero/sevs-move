import cv2
import numpy as np
import os
import shutil
import image_slicer
import PIL.Image
from pynput.keyboard import Key, Controller
import subprocess
import pandas as pd
from tkinter import *

import time
# from IPython import embed

PATH_BG = 'icons_with_bg\\'
PATH_SLICES = 'slices\\'

# def interface():
#     top = Tk()
#     top.title('Sevs Move')
#     top.geometry('800x600')
#     # top.wm_iconbitmap('icon.ico')
#
#     b = Button(top, text='Configurar time', command=ask_pokemons)
#     b.pack()
#
#     B = Button(top, text='Scan & Fill', command=scan_e_preenchimento)
#
#     top.mainloop()


def take_screenshot():

    subprocess.call('screenshot.bat')


def slice_screenshot(screen):

    dim = 175
    y, x = 714, 15
    crop = screen[y:y+6*dim, x:x+6*dim]
    cv2.imwrite('board.png', crop)
    tiles = image_slicer.slice('board.png', 36, save=False)
    image_slicer.save_tiles(tiles, directory=PATH_SLICES)
    slices_dir = os.listdir(PATH_SLICES)

    return slices_dir


def ask_pokemons():

    pkmn_list = []
    dex = pd.read_csv('pokemon.csv')
    dex = dex.set_index('identifier')
    name_to_number = dex.to_dict()
    name_to_number = name_to_number['species_id']

    n = int(input('Quantos pokémon/disruptions há no total? '))
    for i in range(n):
        pkmn = input('Qual o %d pokémon/disruption? ' % (i + 1)).lower()
        pkmn_list.append(pkmn)

    pkmn_list = ['%s.png' % str(name_to_number[pkmn]).zfill(3) for pkmn in pkmn_list]

    return pkmn_list


def resize128(file):

    basedim = 128
    img = PIL.Image.open(file)
    wpercent = (basedim/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basedim,hsize), PIL.Image.ANTIALIAS)
    img.save(file)


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


def match_board(slices_dir, pkmn_imgs):

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

    return key_board


def scan_e_preenchimento():
    if not os.path.exists(PATH_SLICES):
        os.makedirs(PATH_SLICES)

    # screen = cv2.imread('screen.png')
    screen = take_screenshot()
    slices_dir = slice_screenshot(screen)
    # pkmn_imgs = ['302.png', '491.png', '649.png', '717.png']
    pkmn_imgs = ask_pokemons()
    board = match_board(slices_dir, pkmn_imgs)

    keyboard = Controller()
    time.sleep(2)

    for key in board:
        keyboard.press(key)
        keyboard.release(key)

    shutil.rmtree(PATH_SLICES)
    os.remove('screen.png')
    os.remove('board.png')


if __name__ == '__main__':
    scan_e_preenchimento()
