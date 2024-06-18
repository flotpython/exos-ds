---
jupytext:
  cell_metadata_filter: all, -hidden, -heading_collapsed, -run_control, -trusted
  notebook_metadata_filter: all, -jupytext.text_representation.jupytext_version, -jupytext.text_representation.format_version,
    -language_info.version, -language_info.codemirror_mode.version, -language_info.codemirror_mode,
    -language_info.file_extension, -language_info.mimetype, -toc
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
  title: meshgrid pour les courbes en 3D
---

# meshes

+++

La fonction `np.meshgrid` est intéressante - entre autres - pour dessiner des courbes en 3d

Son fonctionnement est assez similaire à `np.indices`, mais au lieu de produire des entiers, on va typiquement lui passer des tableaux produits à base de `np.linspace`.

+++

## rappels

```{code-cell} ipython3
import numpy as np
```

```{code-cell} ipython3
np.indices((5, 10))
```

```{code-cell} ipython3
np.linspace(-np.pi, np.pi, 10)
```

## pour dessiner une courbe en 3D

+++

Imaginons qu'on veuille représenter une fonction de $\mathbb{R}^2 \rightarrow \mathbb{R}$

disons $f(x, y) = x^2 + y^2$ 

sur un domaine rectangulaire

+++

la technique standard consiste à 

1. créer deux tableaux X et Y rectangulaires, qui correspondent à notre pavage  
  le premier contient les X, et le second contient les Y, des points du pavage
1. appliquer la fonction en question **à ces deux tableaux**, ce qui donne un tableau rectangulaire avec la valeur de la fonction à ce point

1. on peut ensuite passer ces trois tableaux rectangulaires à `plt.plot_surface`

+++

## étape 1: meshgrid

```{code-cell} ipython3
# on commence par calculer les domaines

domX = np.linspace(-5, 5, 5)
domY = np.linspace(0, 9, 10)
```

```{code-cell} ipython3
# avec meshgrid, c'est magique, ça fabrique le pavage pour nous

X, Y = np.meshgrid(domX, domY)
X, Y
```

on voit bien la ressemblance avec `indices`, en ce sens que le premier tableau contient la coordonnée et X et le second contient la coordonnée en Y

```{code-cell} ipython3
X.shape, Y.shape
```

## étape 2: calcul de Z

+++

maintenant on peut appliquer la fonction

```{code-cell} ipython3
Z = X**2 + Y*2
Z.shape
```

```{code-cell} ipython3
Z
```

## étape 3: dessin

+++

et la dessiner

```{code-cell} ipython3
import matplotlib.pyplot as plt

%matplotlib widget
```

```{code-cell} ipython3
fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
surf = ax.plot_surface(X, Y, Z)

plt.show()
```

naturellement dans la vraie vie on construit des domaines avec plus de points, par défaut `linspace` met 50 points dans l'intervalle

```{code-cell} ipython3
domX2, domY2 = np.linspace(-5, 5), np.linspace(0, 10)
X2, Y2 = np.meshgrid(domX2, domY2)
Z2 = X2**2 + Y2**2
```

```{code-cell} ipython3
fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
surf = ax.plot_surface(X2, Y2, Z2)

plt.show()
```

***
