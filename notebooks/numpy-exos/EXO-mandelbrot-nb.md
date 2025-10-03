---
jupytext:
  cell_metadata_json: true
  encoding: '# -*- coding: utf-8 -*-'
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
notebookname: Mandelbrot
---

# l'ensemble de Mandelbrot

il s'agit de calculer l'image de la convergence de mandelbrot:

```{image} media/mandelbrot.svg
:width: 400px
:align: right
```

+++

<div class="licence">
<span>Licence CC BY-NC-ND</span>
<span>Thierry Parmentelat &amp; Arnaud Legout</span>
</div>

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
%matplotlib ipympl
```

## comment ça marche ?

+++ {"cell_style": "center"}

* dans l'espace complexe, on définit pour chaque $c\in\mathbb{C}$ la suite
   * $z_0 = c$
   * $z_{n+1} = z_n^2 + c$
* on démontre que 
  * lorsque $|z_n|>2$, la suite diverge

+++ {"cell_style": "center"}

il s'agit pour nous de 

* partir d'un pavé rectangulaire; par exemple sur la figure, on a pris l'habituel  
  $re \in [-2, 0.8]$ et  $im \in [-1.4, 1.4]$

* découper ce pavé en un maillage de $h \times w$ points  (sur la figure, 1000 x 1000)
* on se fixe un nombre maximal `max` d'itérations (disons 20)  
  et pour chaque point du maillage, on va calculer si la suite diverge avant `max` itérations

* c'est-à-dire plus spécifiquement on calcule un tableau `diverge` de la taille du maillage
  * pour chaque point `z`, on calcule les `max` premiers termes de la suite
  * et à la première itération `n` où la suite diverge (son module est supérieur à 2)  
    alors on affecte `diverge[z] = n`

* on n'a plus qu'à afficher ensuite l'image obtenue `diverge` avec `plt.imshow`

+++

````{admonition} indices

pour fabriquer la grille des points de départ, on pourra regarder `np.linspace` et `np.meshgrid`
````

```{code-cell} ipython3
# à vous de jouer

def mandelbrot(h, w):
    pass
```

```{code-cell} ipython3
# et pour la tester, pour produire la mème figure que ci-dessus

mandelbrot(1000, 1000)
```

## v2

* on peut passer en paramètre à la fonction
  * le domaine en x et en y
  * le nombre maximum d'itérations
* on veut pouvoir produire une image (pour l'insérer dans l'énoncé par exemple)
  * quels formats sont disponibles ?
  * sauvez votre image dans un format vectoriel
  * affichez cette depuis votre notebook

```{code-cell} ipython3
# à vous de jouer
# je vous laisse définir la signature de votre fonction

def mandelbrot2():
    pass
```

et je vous demande de mettre ici quelques tests de votre deuxième fonction

```{code-cell} ipython3
# test #1
```

```{code-cell} ipython3
# test #2
```

```{code-cell} ipython3
# test #3
```

----
