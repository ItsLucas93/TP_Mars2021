# -*- coding: utf-8 -*-

from math import sqrt
import PIL.Image as img
import numpy as np
import os
import tqdm


# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
#           Partie 1 
# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

def create_matrice(L, l):
    """
    Création de matrice vide.
    """
    return np.zeros((L, l))

def reconstitution(matrice):
    """ Recréer et renvoie une image à partir d'une matrice. """
    longueur = matrice.shape[0]
    hauteur = matrice.shape[1]
    image = img.new("RGB", (longueur, hauteur))
    for i in range(longueur):
        for j in range(hauteur):
            clr = int(matrice[i, j] * 255)
            image.putpixel((i, j), (clr, clr, clr))
    return image

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
    Filtre de Sobel : https://fr.wikipedia.org/wiki/Filtre_de_Sobel
    x = [-1, 0, 1], [-2, 0, 2], [-1, 0, 1]
    y = [-1, -2, -1], [0, 0, 0], [1, 2, 1]
    """
    for img in range(1, matrice.shape[0] - 1):
        i1 = img - 1 ; i2 = img + 2
        for jmg in range(1, matrice.shape[1] - 1 ):
            j1 = jmg - 1 ; j2 = jmg + 2

            m1, m2, m3 = matrice[i1:i2, j1:j2]

            # Application de la convolution en x
            Sx = m1[0] * -1 + m1[2] + m2[0] * -2 + m2[2] * 2 + m3[0] * -1 + m3[2]
            # Application de la convolution en y
            Sy = m1[0] * -1 + m1[1] * -2 + m1[2] * -1 + m3[0] + m3[1] * 2 + m3[2]

            # Application du thèorème de pythagore, Sx^2 + Sy^2. Application du coefficient pour ramener la valeur pour 0 < x < 1
            matrice[img, jmg] = sqrt(Sx ** 2 + Sy ** 2) * (255 / (sqrt(2) * 1020))

    return matrice

def parcours_L(debutA, finA, step, debutB, finB, matrice):
    """
    Parcours en Longueur de la matrice
    """
    endpoint = False
    for i in range(debutA, finA, step):
        for j in range(debutB, finB):
            if matrice[i, j] == 1:
                borne = i
                endpoint = True
                break
        if endpoint == True:
            break
    return borne


def parcours_l(debutA, finA, step, debutB, finB, matrice):
    """
    Parcours en largeur de la matrice
    """
    endpoint = False
    for j in range(debutA, finA, step):
        for i in range(debutB, finB):
            if matrice[i, j] == 1:
                borne = j
                endpoint = True
                break
        if endpoint == True:
            break
    return borne


def ligne_horizontale(matrice, ep):
    (L, l) = matrice.shape
    ligne = matrice[L // 2]
    nb_paquets = 0
    for i in range(l - ep):
        if ligne[i] == 0.0 or i == 0:
            checkeur = True
            for nb in range(1, ep + 1):
                if not (ligne[i + nb] == 1.0):
                    checkeur = False
        else:
            checkeur = False
        if checkeur:
            nb_paquets += 1
    return nb_paquets


def ligne_verticale(matrice, ep):
    """ Même chose qu'avec 'ligne_horizontale' mais avec une ligne verticale du milieu. """
    (L, l) = matrice.shape
    nb_paquets = 0
    colonne = l // 2
    for i in range(L - ep):
        if matrice[i][colonne] == 0.0 or i == 0:
            checkeur = True
            for nb in range(1, ep + 1):
                if not (matrice[i + nb][colonne] == 1.0):
                    checkeur = False
        else:
            checkeur = False
        if checkeur:
            nb_paquets += 1
    return nb_paquets



def matrice_rognee(matrice, marge):
    """ 
    Matrice rognée
    """
    L = matrice.shape[0]
    l = matrice.shape[1]
    borne_y1 = parcours_L(marge, L - marge, 1, marge, l - marge, matrice)
    borne_y2 = parcours_L(L - marge, marge, -1, marge, l - marge, matrice)
    borne_x1 = parcours_l(marge, l - marge, 1, marge, L - marge, matrice)
    borne_x2 = parcours_l(l - marge, marge, -1, marge, L - marge, matrice)
    return matrice[borne_y1:borne_y2 + 1, borne_x1:borne_x2 + 1]


def matrice_final(matrice1):
    """  Définit un matrice qui aura pour valeur soit 0 (noir) soit 1 (blanc) pour chaque membre.
    Elle est déduite à partir de la matrice de Sobel. """
    (L, l) = matrice1.shape
    matrice2 = create_matrice(L, l)
    for i in range(L):
        for j in range(l):
            if matrice1[i, j] < 0.16:
                matrice2[i, j] = 1.0
            # Comme 'matrice2' est au départ constituée uniquement de 0.0, on laisse cette valeur
            # à 0.0 si elle est supérieure à 0.16, sinon elle passe à 1.0
    return matrice2

def Mise_en_place(path, L, l, **dico):
    """ Définit les différents dictionnaires, listes, dimensions nécessaires à l'algorithme. """
    liste0 = []
    liste1 = []
    liste2 = os.listdir(path)
    size = (L, l)
    for cle, valeur in dico.items():
        for nb in range(valeur):
            liste1.append(cle)
    if len(liste1) != len(liste2):
        raise ValueError("Il doit y avoir autant de types que d'images !")
    return liste0, liste1, liste2, size


def Mise_en_place_inconnu(path, L, l):
    """ Définit la base de données, la liste des chemins menant aux images et les dimensions
    nécessaires à l'algorithme. """
    return [], os.listdir(path), (L, l)


def Mise_en_image(matrice, num, rep, longueur, hauteur):
    if num < 10:
        name = rep + "/image0{}.png".format(num)
    else:
        name = rep + "/image{}.png".format(num)
    image = reconstitution(matrice)
    image = image.resize((longueur, hauteur))
    image.save(name)
    return image


if __name__ == '__main__':
    chemin = "train_data"

    data_base, l_types, l_images, sizes = Mise_en_place(chemin, 400, 400, \
                                                             Type_0=5, Type_1=8, Type_2=8, Type_3=5, Type_4=5, Type_5=9,
                                                             Type_6=4, Type_7=4, Type_8=4, \
                                                             Type_9=6)

    longueur, hauteur = sizes

    for i in range(tqdm(len(l_images))):
        png = img.open(chemin + "/" + l_images[i])
        png = png.resize((longueur, hauteur))
        matrice = matrice_rognee(matrice_final(convolution(nuance_de_gris(png))), 40)
        png = Mise_en_image(matrice, i, "train_data_finished", longueur, hauteur)
        matrice = lecture_image(png)
        paquet_larg = ligne_horizontale(matrice, 1)
        paquet_long = ligne_verticale(matrice, 1)
        data_base.append([matrice, paquet_long, paquet_larg, l_types[i]])
        png.close()