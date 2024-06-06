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

```{code-cell} ipython3
# prune-begin
```

```{code-cell} ipython3
# from v2

from autograd import grad

def taylor2(X, f, n):
    derivatives = []                                      # prune-line
    for degree in range(n+1):                             # prune-line
        derivatives.append(f(0.))                         # prune-line
        f = grad(f)                                       # prune-line
    return taylor1(X, derivatives)                        # prune-line
```

```{code-cell} ipython3
import ipywidgets as widgets

from ipywidgets import AppLayout, Dropdown, IntSlider, FloatSlider, HBox, VBox

plt.ioff()

# the widgets
degree = IntSlider(min=0, max=30, step=1, value=0, description="degree")
# degree.layout.width = '80%'
# degree.layout.margin = '0px 20px'

function = Dropdown(options={
    'sinus': np.sin,
    'cosinus': np.cos,
    'exp': np.exp,
    '2sin(x) + cos(x/4)': custom,
},
    value=np.cos,
    description="function to approximate",
   )
function.layout.width = '80%'
function.layout.margin = '0px 20px'

domain = FloatSlider(min=1., max=100, value=10., 
                     description = "domain")

# assemble them
controls = VBox([
    function, 
    HBox([degree, domain])
])

fig = plt.figure()
# hard-wire the y scale
plt.ylim(-3, 3)
# fig.canvas.header_visible = False
# fig.canvas.min_height = '400px'
def update_title():
    plt.title(f'approx {function.value.__name__} with degree {degree.value}')
update_title()

X = np.linspace(-domain.value, domain.value, 200)
Y1 = function.value(X)
Y2 = taylor2(X, function.value, degree.value)

lines1 = plt.plot(X, Y1)
lines2 = plt.plot(X, Y2)

def update_degree(change):
    Y2 = taylor2(X, function.value, degree.value)
    lines2[0].set_data(X, Y2)
    update_title()
    fig.canvas.draw()
    # does not seem to be required
    # fig.canvas.flush_events()

degree.observe(update_degree, names='value')

def update_function(change):
    Y1 = function.value(X)
    Y2 = taylor2(X, function.value, degree.value)
    lines1[0].set_data(X, Y1)
    lines2[0].set_data(X, Y2)
    update_title()
    fig.canvas.draw()

function.observe(update_function, names='value')

def update_domain(change):
    X = np.linspace(-domain.value, domain.value, 200)
    Y1 = function.value(X)
    Y2 = taylor2(X, function.value, degree.value)
    lines1[0].set_data(X, Y1)
    lines2[0].set_data(X, Y2)
    update_title()
    fig.canvas.draw()
    fig.canvas.flush_events()

domain.observe(update_domain, names='value')
    

AppLayout(
    header=controls,
    center=fig.canvas,
    footer=None,
    pane_heights=[1, 6, 0],
)
```

```{code-cell} ipython3
# prune-end
```

le but du jeu est d'obtenir un matplotlib interactif de ce genre, c'est-à-dire à la fois

- interactif: remarquez la poignée de retaillage
- interactif: on peut changer facilement les paramètres d'entrée, c'est-à-dire à nouveau: le degré, la fonction, le domaine

```{image} media/taylor3-sample.png
:align: center
```

+++

***
