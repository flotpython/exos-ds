---
jupytext:
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
  title: Taylor interactif
---

# Taylor (3/3) un dashboard

+++

On se propose d'approximer une fonction par la formule de Taylor

$$f_n(x) = \sum_{i=0}^{n}\frac{f^{(i)}(0).x^i}{i!}$$

```{code-cell} ipython3
# ! pip install autograd
import autograd.numpy as np
import matplotlib.pyplot as plt

from math import factorial
```

## un dashboard

+++

en application de ce qu'on a vu sur les notebooks interactifs, on peut s'amuser à fabriquer un dashboard qui permet d'afficher l'approximation de Taylor pour une fonction f passée en paramètre

la dashboard permettrait idéalement de
- choisir le degré de l'approximation
- choisir une fonction - disons par exemple parmi sinus, cosinus, exponentielle, et custom (liste non exhaustive)
- le domaine sur lequel on regarde

```{code-cell} ipython3
# notre fonction custom de la dernière fois

def custom(X):
    return 2*np.sin(X) + np.cos(X/4)
```

**modes disponibles**

la solution à cet exercice est relativement différente selon le mode de restitution choisi pour `matplotlib`; notamment il y a 
* `%matplotlib inline` qui est le mode par défaut, **très ancien** et **pas du tout interactif** (on ne peut pas agrandir, zoomer, etc... dans la figure)
  c'est plutôt plus simple à coder, mais le résultat est vraiment rustique du coup, bref c'est plutôt déconseillé d'investir dans cette voie
* `%matplotlib notebook` qui était déjà plus moderne; avec ce mode on peut agrandir / zoomer mais il est **devenu obsolète**
* `%matplotlib ipympl` qui est, en 2024, le successeur du précédent - notamment si vous voulez visualiser vos rendus interactifs sous vs-code par exemple
  ce mode nécessite une installation supplémentaire (et [voir aussi cette page pour plus de détails](label-dashboard-ipympl))
  ```shell
  pip install ipympl
  ```
  et il se peut que vous ayez besoin de relancer votre serveur jupyter après cette installation  

notre solution utilise ce dernier mode, pour quelques exemples voir <https://matplotlib.org/ipympl/examples/full-example.html>;

```{code-cell} ipython3
%matplotlib ipympl
```

ce qui change fondamentalement entre le premier mode (`inline`) et les deux autres, c'est que dans le premier cas, à chaque changement de réglage on repeint toute la figure; c'est plus facile à écrire, mais ça "flashe" du coup à chaque fois; dans les autres modèles au contraire, on a une figure affichée, et lorsqu'on change un paramètre on va seulement modifier un des morceaux de la figure

ici par exemple notre figure c'est principalement deux courbes (la fonction, et son approximation), plus les décorations (axes, titres, etc..)  
et au changement de paramètre, on va changer **seulement la courbe de l'approximation** - et éventuellement le titre si on veut

```{code-cell} ipython3
# à vous
```

le but du jeu est d'obtenir un matplotlib interactif de ce genre, c'est-à-dire à la fois

- interactif: remarquez la poignée de retaillage
- interactif: on peut changer facilement les paramètres d'entrée, c'est-à-dire à nouveau: le degré, la fonction, le domaine

```{image} media/taylor3-sample.png
:align: center
```

+++

***
