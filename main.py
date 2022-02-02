import numpy as np
import pandas as pd
from PIL import Image

table = pd.read_excel(r'table_braille.xlsx')


list_braille = list(table["Column5"])

dict_binary = {}
for i in range(len(list_braille)):
    dict_binary['{0:08b}'.format(i)] = list_braille[i]


def lancement(filepath):
    image = Image.open(filepath)
    image = image.convert('L')
    return encodage(image)

def scaler(image):
    long,larg = image.size
    image = image.resize((400,int(larg/(long/600))),Image.ANTIALIAS)
    return image

def cropper(image):
    image = scaler(image)
    long,larg = image.size
    while larg%8 !=0:
        larg -=1
    left,top,right,bottom = 0,0,long,larg
    image = image.crop((left, top, right, bottom))
    return image


def encodage(image):
    image = cropper(image)
    long, larg = image.size
    tolerance = 150
    x_dec = 0
    y_dec = 0
    dechiffr = []
    for Y in range(int(larg / 8) - 1):
        for X in range(int(long / 2)):
            code = ['0', '0', '0', '0', '0', '0', '0', '0']
            for x in range(2):
                for y in range(3):
                    if image.getpixel((x_dec + x, y_dec + y)) > tolerance:
                        code[-((y+(x*3)) + 1)] = '1'  # le - est la parce que les clé du dict sont a l'envers
            if image.getpixel((x_dec, y_dec + 8)) > tolerance:
                code[1] = '1'
            if image.getpixel((x_dec + 1, y_dec + 8)) > tolerance:
                code[0] = '1'

            x_dec += 2
            dechiffr.append(dict_binary[''.join(code)])
        dechiffr.append('\n')
        y_dec += 8
        x_dec = 0
    return ''.join(dechiffr)



print(lancement("drake.jpg"))












