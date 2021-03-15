# -*- coding: utf-8 -*-

from math import sqrt
import PIlongueur.Image as img
import numpy as np


# import os


# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
#           Partie 1 
# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

def create_matrice(long, larg):
    """
    Création de matrice vide.
    """
    return np.zeros((long, larg))


def lecture_image(img):
    (longueur, hauteur) = img.size
    matrice = create_matrice(longueur, hauteur)
    for i in range(longueur):
        for j in range(hauteur):
            clr = img.getpixel((i, j))[0]
            matrice[i, j] = round(clr / 255)
    return matrice


def nuance_de_gris(img):
    """
    Pondération des couleurs RGB par le pixel puis divisé par 255 pour ramener la valeur x, 0 < x < 1
    """
    (longueur, hauteur) = img.size
    matrice = create_matrice(longueur, hauteur)
    for i in range(longueur):
        for j in range(hauteur):
            (r, v, b) = img.getpixel((i, j))
            g = int((r + v + b) / 3)
            matrice[i, j] = g / 255
    return matrice


def convolution(matrice):
    """
    Filtre de Sobel
    x = [-1, 0, 1], [-2, 0, 2], [-1, 0, 1]
    y = [-1, -2, -1], [0, 0, 0], [1, 2, 1]
    """
    for img in range(1, matrice.shape[0] - 1):
        i1 = img - 1
        i2 = img + 2
        for jmg in range(1, matrice.shape[1] - 1):
            j1 = jmg - 1
            j2 = jmg + 2

            m1, m2, m3 = matrice[i1:i2, j1:j2]

            # Application de la convolution en x
            Sx = m1[0] * -1 + m1[2] + m2[0] * -2 + m2[2] * 2 + m3[0] * -1 + m3[2]
            # Application de la convolution en y
            Sy = m1[0] * -1 + m1[1] * -2 + m1[2] * -1 + m3[0] + m3[1] * 2 + m3[2]

            # Application du thèorème de pythagore, Sx^2 + Sy^2. Application du coefficient pour ramener la valeur pour 0 < x < 1
            matrice[img, jmg] = sqrt(Sx ** 2 + Sy ** 2) * (255 / (sqrt(2) * 1020))

    return matrice

