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
  pygments_lexer: ipython3
  nbconvert_exporter: python
nbhosting:
  title: Taylor interactif
---

# Taylor (3/3) un dashboard

+++

On rappelle la formule de Taylor

$$f_n(x) = \sum_{i=0}^{n}\frac{f^{(i)}(0).x^i}{i!}$$

+++

## un dashboard

+++

le but du jeu dans cette dernière partie du TP est de créer un dashboard qui permet d'afficher un matplotlib interactif du genre de celui capturé sur la figure, c'est-à-dire à la fois

- interactif: remarquez la poignée de retaillage

- interactif: on peut changer facilement les paramètres d'entrée, c'est-à-dire 
  - choisir le degré de l'approximation
  - choisir une fonction - disons par exemple parmi sinus, cosinus, exponentielle, et custom (liste non exhaustive)
  - le domaine sur lequel on regarde

```{image} media/taylor3-sample.png
:align: center
```

+++

## modes disponibles

la solution à cet exercice est relativement différente selon le mode de restitution choisi pour `matplotlib`; notamment il y a 
* `%matplotlib inline` qui est le mode par défaut, **très ancien** et **pas du tout interactif** (on ne peut pas agrandir, zoomer, etc... dans la figure)
  c'est plutôt plus simple à coder, mais le résultat est vraiment rustique du coup, bref c'est plutôt déconseillé d'investir dans cette voie
* `%matplotlib notebook` qui était déjà plus moderne; avec ce mode on peut agrandir / zoomer mais il est **devenu obsolète**
* `%matplotlib ipympl` qui est, en 2024, le successeur du précédent - notamment si vous voulez visualiser vos rendus interactifs  
  ce mode nécessite une installation supplémentaire (et [voir aussi cette page pour plus de détails](#label-dashboard-ipympl))
  ```shell
  pip install ipympl
  ```
  et il se peut que vous ayez besoin de relancer votre serveur jupyter après cette installation  

***notre solution utilise ce dernier mode***  
pour quelques exemples voir <https://matplotlib.org/ipympl/examples/full-example.html>

```{code-cell} ipython3
%matplotlib ipympl
```

ce qui change fondamentalement entre le premier mode (`inline`) et les deux autres, c'est que dans le premier cas, à chaque changement de réglage on repeint toute la figure; c'est plus facile à écrire, mais ça "flashe" du coup à chaque fois; dans les autres modèles au contraire, on a une figure affichée, et lorsqu'on change un paramètre on va seulement modifier un des morceaux de la figure

ici par exemple notre figure c'est principalement deux courbes (la fonction, et son approximation), plus les décorations (axes, titres, etc..)  
et au changement de paramètre, on va changer **seulement la courbe de l'approximation** - et éventuellement le titre si on veut

+++

## on utilise le TP #2

+++

pour commencer, on a besoin de la fonction `taylor2` qu'on a écrite dans le TP #2 - et la fonction `custom` aussi d'ailleurs

vous pouvez, au choix:

- soit recopier le code depuis le TP #2
- ou bien, si vous avez un peu de temps et que vous voulez faire proprement, créer un fichier `taylor.py` dans lequel vous mettez le code écrit dans le TP #2, et vous l'importez depuis le notebook #2, et comme ça vous n'avez qu'à l'importer à nouveau ici
  c'est la bonne approche dans la vraie vie si vous voulez respecter le principe DRY (don't repeat yourself)

bref, à vous de faire ce qu'il faut pour définir ces deux symboles

```{code-cell} ipython3
# votre code pour copier ou importer `taylor2` et `custom`
```

```{code-cell} ipython3
# ! pip install autograd
import autograd.numpy as np
import matplotlib.pyplot as plt

from math import factorial
```

## on importe

la librairie qui nous sert ici est `ipywidgets` <https://ipywidgets.readthedocs.io/>

```{code-cell} ipython3
import ipywidgets as widgets

from ipywidgets import AppLayout, Dropdown, IntSlider, FloatSlider, HBox, VBox

plt.ioff();
```

## ipywidgets, comment ça marche ?

on vous montre d'abord pas à pas le code pour faire un tout petit dashboard

+++

### les widgets

un widget c'est un morceau d'interface, qui permet de choisir un paramètre; on va vous montrer le `FloatSlider` qui permet de choisir une valeur flottante, mais il y a aussi le `IntSlider`, le `Dropdown` pour choisir parmi un nombre fini de choix, etc...

```{code-cell} ipython3
# ici knob c'est juste un nom de variable Python

knob = FloatSlider(
    min=0, max=10,
    value=3, step=0.05,
    description="un potard",
    # ceci est jsute cosmétique, vous pouvez ignorer en première lecture...
    layout={'margin': '5px', 'width': '100%'},
)
```

on peut en faire quoi? eh bien si on l'affiche

```{code-cell} ipython3
knob
```

je peux faire bouger la réglette, mais c'est à peu près tout, il ne se passe rien  
c'est normal, on ne l'a pas "branché"

+++

### les callbacks

pour que ma réglette serve à quelque chose, on va lui attacher une *callback*  
c'est-à-dire **une fonction** qui sera **appelée lorsqu'il y aura un changement**  

pour commencer j'écris cette *callback*, c'est une fonction Python,

```{code-cell} ipython3
def knob_has_changed(change):
    print(f"knob vaut maintenant {change.new}, et change name = {change.name}")
```

*so far so good*, mais bien sûr il ne se passe toujours rien si on bouge la réglette  
sauf que maintenant, on est **prêts à "brancher" les deux**, comme ceci:

```{code-cell} ipython3
# on dit au slider que lorsque sa valeur change (names='value')
# il doit appeler la callback knob_has_changed

knob.observe(knob_has_changed, names='value')
```

et maintenant si vous faites bouger la réglette, il va se passer des trucs  
bon, pour ne pas polluer tout l'écran, les impressions qu'on fait se retrouvent dans la console de Jupyter Lab, regardez bien le bas de l'écran, 
```{image} media/jlab-console.png
:width: 300px
:align: right
```

vous ouvrez la console et vous voyez les messages affichés par la callback, qui disent e.g.
```text
knob vaut maintenant 2.85, et change name = value
```

super, on a déjà un moyen de choisir parmi plusieurs valeurs, et de réagir aux changements

+++

### les boites pour construire

la librairie vient aussi avec des moyens d'organiser les widgets en lignes et colonnes, c'est là qu'interviennent les `HBox` et `VBox`

````{admonition} keep it simple

pour rester simple, on va mettre **plusieurs fois la même réglette**, mais bien sûr dans la vraie app ce ne sera plus le cas
````

```{code-cell} ipython3
VBox([
    # la première ligne est elle-même composite
    HBox([knob, knob]),
    # dans la deuxième ligne on met juste un widget
    knob
])
```

vous remarquez d'ailleurs que les trois réglettes sont synchrones, c'est normal car elles servent à définir **une seule valeur** !  
qui est d'ailleurs en permanence accessible comme

```{code-cell} ipython3
# par contre le résultat de cette cellule ne va pas
# tout seul se rafraichir si vous bougez la réglette...

knob.value
```

### matplotlib incrémental

il ne nous reste plus qu'à voir comment on peut utiliser matplotlib de manière incrémentale, c'est-à-dire comment on peut **modifier** une figure **après** l'avoir affichée  

ça se présente comme ceci; imaginons qu'on a créé une figure, qui montre la valeur de `knob` sur le domaine

```{code-cell} ipython3
X = np.linspace(-2*np.pi, 2*np.pi)

fig = plt.figure(figsize=(4, 2))
ax = plt.axes()

# on va afficher une droite Y=knob
# donc Y sera dans l'intervalle [0, 10]
# plt.ylim(0, 10)
ax.set_ylim(0, 10)

# la clé est de garder une référence vers la courbe

line = ax.plot(
    # une astuce pour que Y soit de la même forme que X
    X, X*0. + knob.value)

fig.show()
```

````{admonition} pourquoi le set_ylim ?

on a mis la hauteur de la courbe (les bornes en Y) "en dur", pourquoi ça me direz-vous ?

souvenez-vous que sinon, c'est matplotlib qui va calculer ces bornes *automatiquement*; essayez de commenter cette ligne pour voir du coup ce qui se passerait sans elle
````

+++

eh bien, grâce à cette référence vers `line`, on va pouvoir modifier la figure "après coup" en faisant juste, par exemple

```{code-cell} ipython3
# on change ensuite la hauteur comme on veut

# par exemple Y = 4
# attention à ce line[0], ce n'est pas intuitif !
line[0].set_data(X, X * 0. + 4)

# c'est ceci qui va "flusher" la mise à jour de la figure
# à ne faire qu'une fois que tous les changements sont effectués
fig.canvas.draw()
```

### on assemble avec AppLayout

enfin pour mettre tout ensemble, on dispose d'une classe `AppLayout`; le tout se présenterait comme ceci

```{code-cell} ipython3
knob = FloatSlider(
    min=0, max=10,
    value=3, step=0.05,
    description="pick Y",
    # ceci est juste cosmétique, vous pouvez ignorer en première lecture...
    layout={'margin': '0px 5px', 'width': '100%'},
)

fig = plt.figure(figsize=(4, 2))
axes = plt.axes()
axes.set_ylim((0, 10))
line = axes.plot(X, 0*X + knob.value)

def update_y(change):
    print("got a change", change)
    line[0].set_data(X, X*0. + change.new)
    fig.canvas.draw()

knob.observe(update_y, names='value')

controls = knob
# on aurait pu mettre artificiellement 2 réglettes
controls = HBox([knob, knob])

AppLayout(
    header=controls,
    center=fig.canvas,
    footer=None,
    pane_heights=[1, 6, 0],
)
```

## à vous de vous en inspirer

en vous inspirant du petit exemple, et en explorant [la documentation de  `ipywidgets`](https://ipywidgets.readthedocs.io/), tentez de reproduire un dashboard comme décrit dans le screenshot au début de ce notebook
