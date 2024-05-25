---
jupytext:
  cell_metadata_filter: all,-hidden,-heading_collapsed,-run_control,-trusted
  cell_metadata_json: true
  encoding: '# -*- coding: utf-8 -*-'
  notebook_metadata_filter: 'all, -jupytext.text_representation.jupytext_version,
    -jupytext.text_representation.format_version,

    -language_info.version, -language_info.codemirror_mode.version, -language_info.codemirror_mode,

    -language_info.file_extension, -language_info.mimetype, -toc'
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
language_info:
  name: python
  nbconvert_exporter: python
  pygments_lexer: ipython3
nbhosting:
  title: suite du TP simple avec des images
---

Licence CC BY-NC-ND, Valérie Roy & Thierry Parmentelat

+++

pour réaliser ce TP localement sur votre ordi, si ce n'est pas déjà fait, {download}`commencez par télécharger le zip<./ARTEFACTS-images.zip>`

+++

# TP images (2/2)

merci à Wikipedia et à stackoverflow

**le but de ce TP n'est pas d'apprendre le traitement d'image  
on se sert d'images pour égayer des exercices avec `numpy`  
(et parce que quand on se trompe ça se voit)**

```{code-cell} ipython3
import numpy as np
from matplotlib import pyplot as plt
```

+++ {"tags": ["framed_cell"]}

**notions intervenant dans ce TP**

````{admonition} →
sur les tableaux `numpy.ndarray`

* `reshape()`, tests, masques booléens, *ufunc*, agrégation, opérations linéaires sur les `numpy.ndarray`
* les autres notions utilisées sont rappelées (très succinctement)

pour la lecture, l'écriture et l'affichage d'images

* utilisez `plt.imread`, `plt.imshow`
* utilisez `plt.show()` entre deux `plt.imshow()` dans la même cellule

**note**

* nous utilisons les fonctions de base sur les images de `pyplot` par souci de simplicité
* nous ne signifions pas là du tout que ce sont les meilleures  
par exemple `matplotlib.pyplot.imsave` ne vous permet pas de donner la qualité de la compression  
alors que la fonction `save` de `PIL` le permet

* vous êtes libres d'utiliser une autre librairie comme `opencv`  
  si vous la connaissez assez pour vous débrouiller (et l'installer), les images ne sont qu'un prétexte

**n'oubliez pas d'utiliser le help en cas de problème.**
````

+++

## Création d'un patchwork

+++

1. Le fichier `data/rgb-codes.txt` contient une table de couleurs:
```
AliceBlue 240 248 255
AntiqueWhite 250 235 215
Aqua 0 255 255
.../...
YellowGreen 154 205 50
```
Le nom de la couleur est suivi des 3 valeurs de ses codes `R`, `G` et `B`  
Lisez cette table en `Python` et rangez-la dans la structure qui vous semble adéquate.

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
# prune-cell 1.
colors_dict = dict()
with open('data/rgb-codes.txt', 'r') as f:
    for line in f:
        name, r, g, b = line.split()
        colors_dict[name] = [int(r), int(g), int(b)]
```

```{code-cell} ipython3
# prune-cell 1. 
# ou encore, en plus pédant
colors_dict = dict()
with open('data/rgb-codes.txt', 'r') as f:
    for line in f:
        name, *rgb = line.split()
        colors_dict[name] = list(map(int, rgb))
```

2. Affichez, à partir de votre structure, les valeurs rgb entières des couleurs suivantes  
`'Red'`, `'Lime'`, `'Blue'`

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
# prune-cell 2.
for c in ['Red', 'Lime', 'Blue']:
    print(c, colors_dict[c])
```

3. Faites une fonction `patchwork` qui  

   * prend une liste de couleurs et la structure donnant le code des couleurs RGB
   * et retourne un tableau `numpy` avec un patchwork de ces couleurs  
   * (pas trop petits les patchs - on doit voir clairement les taches de couleurs  
   si besoin de compléter l'image mettez du blanc  
   (`numpy.indices` peut être utilisé)

```{code-cell} ipython3
# votre code
```

````{tip}
en version un peu brute, on pourrait utiliser juste la racine carrée;
par exemple avec 5 couleurs créer un carré 3x3 - mais 3x2 c'est quand même mieux !


pour calculer le rectangle qui contient n couleurs

n | rect | n | rect | n | rect | n | rect |
-|-|-|-|-|-|-|-|
1 | 1x1 | 5 | 2x3 | 9 | 3x3 | 14 | 4x4 |
2 | 1x2 | 6 | 2x3 | 10 | 3x4 | 15 | 4x4 |
3 | 2x2 | 7 | 3x3 | 11 | 3x4 | 16 | 4x4 |
4 | 2x2 | 8 | 3x3 | 12 | 3x4 | 17 | 4x5 |
````

```{code-cell} ipython3
# prune-cell
# a rougher approach would just use a square
def rectangle_size(n):
    '''
    computes the optimal size for a square of rectangle
    to store that many colors;
    if a rectangle, it will be of the form n-1, n
    '''
    c = np.ceil(np.sqrt(n))
    l = np.ceil(n / c)
    return int(l), int(c)

for n in range(1, 18):
    print(f"{n=} -> {rectangle_size(n)=}")
```

```{code-cell} ipython3
# prune-cell
def patchwork (col_list, col_dict, side=5, background='White'):
    '''
    create an image with a patchwork of the col_list colors
    the image contains l*c patches
    each patch is a square of side pixels
    the patchwork can have more patches than colors
    the color of additional patches will be background (white by defaut)
    '''
    # we compute the number of lines and columns of the patchwork
    l, c = rectangle_size(len(col_list))

    # we create the ndarray of the colors
    # (each color has an indice from 0 to len(col_list)-1)
    # initialized with the background color
    colormap = np.array(l*c*[col_dict[background]], dtype=np.uint8)
    # at this point col_tab is of shape (l*c), 3
    # because col_dict[background itself has 3 values]

    # we assign the array with the resolved colors
    colormap[0:len(col_list)] = [col_dict[k] for k in col_list]
    # if this puzzles you, evaluate 10 * [[255, 0, 0]]
    print(f"{colormap.shape=}")

    # the final image is a rectangle of (l*side, c*side) of pixels
    # we compute its indices
    i, j = np.indices((l*side, c*side))
    # we pass the indices in the patchwork of l*c patches (i.e. //side)
    I, J = i//side, j//side

    # c*I + J transforms I and J in the corresponding color indices in the colormap
    # its shape is the same as the final image
    # print(f"{j[:2]=}")
    # print(f"{J[:2]=}")
    # print(f"{c*I+J=}")

    # so all we are left with is .. a simple array-by-array indexation
    return colormap[c*I + J]


colors = [
    'DarkBlue', 'AntiqueWhite', 'LimeGreen',
    'NavajoWhite', 'Tomato', 'DarkGoldenrod',
    'LightGoldenrodYellow', 'OliveDrab',
]
plt.imshow(patchwork(colors, colors_dict, side=5));
```

4. Tirez aléatoirement une liste de couleurs et appliquez votre fonction à ces couleurs.

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
# prune-cell 4.
import random
k = 19
im = patchwork(random.sample(list(colors_dict.keys()), k),
               colors_dict,
               side=10)

plt.imshow(im);
```

5. Sélectionnez toutes les couleurs à base de blanc et affichez leur patchwork  
même chose pour des jaunes

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
# prune-cell 5.
for s in ['white', 'red']: #, 'blue', 'medium', 'light', 'brown'
    colors = [k for k in colors_dict.keys() if s in k.lower()]
    print(f'{len(colors)} "{s}" colors')
    plt.imshow(patchwork(colors, colors_dict))
    plt.show()
```

6. Appliquez la fonction à toutes les couleurs du fichier  
et sauver ce patchwork dans le fichier `patchwork.png` avec `plt.imsave`

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
# prune-cell 6.
im_all = patchwork(list(colors_dict.keys()), colors_dict, side=100)
plt.imshow(im_all);
```

7. Relisez et affichez votre fichier  
   attention si votre image vous semble floue c'est juste que l'affichage grossit vos pixels

vous devriez obtenir quelque chose comme ceci

```{image} media/patchwork-all.jpg
:align: center
```

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
# prune-cell 7.

plt.imsave('patchwork-all.png', im_all)
plt.show()
pat = plt.imread('patchwork-all.png')
plt.imshow(pat);
```

## Somme des valeurs RGB d'une image

+++

0. Lisez l'image `data/les-mines.jpg`

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
# prune-cell 0.
import numpy as np
from matplotlib import pyplot as plt

im = plt.imread('data/les-mines.jpg')
```

1. Créez un nouveau tableau `numpy.ndarray` en sommant **avec l'opérateur `+`** les valeurs RGB des pixels de votre image

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
# prune-cell 1.
# en faisant comme demandé ce n'est pas très élégant
gr0 = im[:, :, 0] + im[:, :, 1] + im[:, :, 2]
```

2. Affichez l'image (pas terrible), son maximum et son type

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
# prune-cell 2.
print(f"type={gr0.dtype}, max={gr0.max()}") # uint8 -> overflow
# image pas correcte à cause des overflows
plt.imshow(gr0, cmap='gray')
plt.show()
```

3. Créez un nouveau tableau `numpy.ndarray` en sommant **avec la fonction d'agrégation `np.sum`** les valeurs RGB des pixels de votre image

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
# prune-cell 3.

# de la manière précédente vous ne pouvez pas obtenir les valeurs
# en niveaux de gris des pixels de l'image, il faudrait faire:
# gr2 = im[:, :, 0]/3 + im[:, :, 1]/3 + im[:, :, 1]/3
# print(gr2.dtype, gr2.max())

gr1 = (np.sum(im, axis=2))
```

4. Affichez l'image, son maximum et son type

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
# prune-cell 4.
print(f"type={gr1.dtype}, max={gr1.max()}") # int64 ok
```

5. Pourquoi cette différence ? Utilisez le help `np.sum?`

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
# prune-cell 5.
# np.sum?
# dtype : dtype, optional
#     The type of the returned array and of the accumulator in which the
#     elements are summed.  The dtype of `a` is used by default unless `a`
#     has an integer dtype of less precision than the default platform
#     integer.  In that case, if `a` is signed then the platform integer
#     is used while if `a` is unsigned then an unsigned integer of the
#     same precision as the platform integer is used.
```

6. Passez l'image en niveaux de gris de type entiers non-signés 8 bits  
(de la manière que vous préférez)

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
# prune-cell 6.
plt.imshow(gr1/3, cmap='gray')
plt.show()
```

```{code-cell} ipython3
# prune-cell 6.bis

gr2 = (im[:, :, 0]/3 + im[:, :, 1]/3 + im[:, :, 1]/3).astype(np.uint8)
plt.imshow(gr2, cmap='gray')
plt.show()
```

7. Remplacez dans l'image en niveaux de gris,  
les valeurs >= à 127 par 255 et celles inférieures par 0  
Affichez l'image avec une carte des couleurs des niveaux de gris  
vous pouvez utilisez la fonction `numpy.where`

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
# prune-cell 7.
gr3 = gr2.copy()
gr3[gr3>=127] = 255
gr3[gr3<127] = 0
```

```{code-cell} ipython3
# prune-cell 7. avec where
gr3 = np.where(gr2>128, 255, 0)
plt.imshow(gr3, cmap='gray')
plt.show()
```

8. avec la fonction `numpy.unique`  
regardez les valeurs différentes que vous avez dans votre image en noir et blanc

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
# prune-cell 8.
print(np.unique(gr3))
```

## Image en sépia

+++

Pour passer en sépia les valeurs R, G et B d'un pixel  
(encodées ici sur un entier non-signé 8 bits)  

1. on transforme les valeurs `R`, `G` et `B` par la transformation  
`0.393 * R + 0.769 * G + 0.189 * B`  
`0.349 * R + 0.686 * G + 0.168 * B`  
`0.272 * R + 0.534 * G + 0.131 * B`  
(attention les calculs doivent se faire en flottants pas en uint8  
pour ne pas avoir, par exemple, 256 devenant 0)  
1. puis on seuille les valeurs qui sont plus grandes que `255` à `255`
1. naturellement l'image doit être ensuite remise dans un format correct  
(uint8 ou float entre 0 et 1)

+++

````{tip}
jetez un coup d'oeil à la fonction `np.dot` 
qui est si on veut une généralisation du produit matriciel

dont voici un exemple d'utilisation:
````

```{code-cell} ipython3
:scrolled: true

# exemple de produit de matrices avec `numpy.dot`
# le help(np.dot) dit: dot(A, B)[i,j,k,m] = sum(A[i,j,:] * B[k,:,m])

i, j, k, m, n = 2, 3, 4, 5, 6
A = np.arange(i*j*k).reshape(i, j, k)
B = np.arange(m*k*n).reshape(m, k, n)

C = A.dot(B)
# or C = np.dot(A, B)

print(f"en partant des dimensions {A.shape} et {B.shape}")
print(f"on obtient un résultat de dimension {C.shape}")
print(f"et le nombre de termes dans chaque `sum()` est {A.shape[-1]} == {B.shape[-2]}")
```

**Exercice**

+++

1. Faites une fonction qui prend en argument une image RGB et rend une image RGB sépia  
la fonction `numpy.dot` peut être utilisée si besoin, voir l'exemple ci-dessus

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
# prune-cell 1. pas à pas
# le même code que ci-dessous mais avec plein de print()

SEPIA = np.array([[0.393, 0.349, 0.272],
                  [0.769, 0.686, 0.534],
                  [0.189, 0.168, 0.131]])

img = plt.imread('data/les-mines.jpg') # dtype = uint8
print(img.dtype)
print(img.shape, SEPIA.shape) # (i, j, 3) (m, 3)

img_SEPIA = img.dot(SEPIA)
# ou img_SEPIA = np.dot(img, SEPIA)
print(img_SEPIA.dtype) # floats64

print(img_SEPIA.min(), img_SEPIA.max()) # de 0 à 344.505

# plt.imshow demande un type correct
# soit uint8 (donc des valeurs entre 0 et 255)
# soit float64 avec des valeurs entre 0 et 1
# (et pas entre 0 et 344.505)
# on doit donc seuiller au dessous de 255 et passer en uint8
img_SEPIA[img_SEPIA>255] = 255
img_SEPIA = img_SEPIA.astype(np.uint8)

plt.imshow(img_SEPIA);
```

```{code-cell} ipython3
# prune-cell 1. avec dot()
# dans ce cas de figure on peut utiliser indifféremment
# np.dot ou @ (aka np.matmul)
# https://numpy.org/doc/stable/reference/generated/numpy.dot.html

def sepia(im, SEPIA=np.array([[0.393, 0.349, 0.272],
                              [0.769, 0.686, 0.534],
                              [0.189, 0.168, 0.131]])):
# les deux marchent
    result = np.dot(im, SEPIA)
#    result = im @ SEPIA
    result[result>255] = 255
    return result.astype(np.uint8)

plt.imshow(
    sepia(plt.imread('data/les-mines.jpg')));
```

prune-cell: comment ça marche ?

la doc dit que
> `dot(a, b)[i,j,k,m] = sum(a[i,j,:] * b[k,:,m])`

dans notre cas:

* a est de dimension 3, et `a.shape = lines, cols, 3`, et
* b est de dimension 2, avec `b.shape = 3, 3`, ce qui donne

> `dot(image, SEPIA)[i, j, canal]
  = sum(image[i, j, :] * SEPIA[:, canal])`  
  cqfd $\diamond$

+++

2. Passez votre patchwork de couleurs en sépia  
Lisez le fichier `patchwork-all.jpg` si vous n'avez pas de fichier perso

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
:cell_style: center

# prune-cell 2.

file = 'media/patchwork-all.jpg'
im = plt.imread(file)
plt.imshow(sepia(im));
```

3. Passez l'image `data/les-mines.jpg` en sépia

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
# prune-cell 3.

im_sepia = sepia(plt.imread('data/les-mines.jpg'))
plt.imshow(im_sepia)
plt.imsave('data/les-mines-sepia.jpg', im_sepia)
```

## Exemple de qualité de compression

+++

1. Importez la librairie `Image`de `PIL` (pillow)  
(vous devez peut être installer PIL dans votre environnement)

```{code-cell} ipython3
# prune-cell 1.
from PIL import Image
```

```{code-cell} ipython3
# votre code
```

2. Quelle est la taille du fichier `data/les-mines.jpg` sur disque ?

```{code-cell} ipython3
file = "data/les-mines.jpg"
```

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
# prune-cell 2. - en bash
%ls -l $file
```

```{code-cell} ipython3
# prune-cell 2. - en Python pour cross-platform
from pathlib import Path
print(f"{file} {Path(file).stat().st_size} bytes")
```

3. Lisez le fichier 'data/les-mines.jpg' avec `Image.open` et avec `plt.imread`

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
# prune-cell 3.
imPLT = plt.imread(file)
imPIL = Image.open(file)
```

4. Vérifiez que les valeurs contenues dans les deux objets sont proches

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
# prune-cell 4.
np.all(np.isclose(imPLT, imPIL))
```

5. Sauvez (toujours avec de nouveaux noms de fichiers)  
l'image lue par `imread` avec `plt.imsave`  
l'image lue par `Image.open` avec `save` et une `quality=100`  
(`save` s'applique à l'objet créé par `Image.open`)

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
# prune-cell 5.
plt.imsave(f'{file}-PLT.jpg', imPLT) # no quality
imPIL.save(f'{file}-PIL.jpg', quality=100)
```

6. Quelles sont les tailles de ces deux fichiers sur votre disque ?  
Que constatez-vous ?

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
# prune-cell 6.
for ext in ['PLT', 'PIL']:
    print(f"{ext} {Path(f'{file}-{ext}.jpg').stat().st_size} bytes")
```

7. Relisez les deux fichiers créés et affichez avec `plt.imshow` leur différence

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
:scrolled: true

# prune-cell 7.

imPLT_PLT = plt.imread(f"{file}-PLT.jpg")
imPLT_PIL = plt.imread(f"{file}-PIL.jpg")
print(np.all(np.isclose(imPLT_PLT, imPLT_PIL)))
plt.imshow(imPLT_PLT - imPLT_PIL);
```
