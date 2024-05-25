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

et le dashboard permet de choisir le degré de l'approximation

avec par exemple les fonctions sinus, cosinus, et exponentielle

**modes disponibles**
la solution à cet exercice est reliativement différente selon le mode de restitution choisi pour `matplotlib`; notamment il y a 
* `%matplotlib inline` qui est le mode par défaut, **très ancien** et pas du tout interactif (on ne peut pas agrandir, zoomer, etc... dans la figure); c'est plutôt plus simple à coder, mais le résultat est vraiment rustique du coup, bref c'est plutôt déconseillé d'inverstir dans cette voie
* `%matplotlib ipympl` qui est déjà plus moderne; avec ce mode on peut agrandir / zoomer
* `%matplotlib ipympl` qui semble, en 2022, être le successeur du précédent - notamment si vous voulez visualiser vos rendus interactifs sous vs-code par exemple; ce mode nécessite une installation supplémentaire
```shell
pip install ipympl
```
et il se peut que vous ayez besoin de relancer votre serveur jupyter après cette installation  

notre solution utilise ce dernier mode, pour quelques exemples voir <https://matplotlib.org/ipympl/examples/full-example.html>; cette page peut être utile aussi <https://kapernikov.com/ipywidgets-with-matplotlib/>

```{code-cell} ipython3
%matplotlib ipympl
```

ce qui change fondamentalement entre le premier mode (`inline`) et les deux autres, c'est que dans le premier cas, à chaque changement de réglage on repeint toute la figure; c'est pus facile à écrire, mais ça "flashe" du coup à chaque fois; dans les autres modèles au contraire, on a une figure affichée, et lorsqu'on change un paramètre on va seulement modifier un des morceaux de la figure

ici par exemple notre figure c'est principalement deux courbes (la fonction, et son approximation), plus les décorations (axes, titres, etc..) et au changement de paramètre on va changer seulement la courbe de l'approximation - et éventuellement le titre si on veut

```{code-cell} ipython3
# prune-begin
```

```{code-cell} ipython3
# from v2

from autograd import grad

def taylor1(X, derivatives):
    shape = X.size,                                    # prune-line
    Y = np.zeros(shape)                                # prune-line
    for degree, derivative in enumerate(derivatives):  # prune-line
        Y += X**degree * derivative/factorial(degree)  # prune-line
    return Y                                           # prune-line

def taylor2(X, f, n):
    derivatives = []                                      # prune-line
    for degree in range(n):                               # prune-line
        derivatives.append(f(0.))                         # prune-line
        f = grad(f)                                       # prune-line
    return taylor1(X, derivatives)                        # prune-line
```

```{code-cell} ipython3
import ipywidgets as widgets

from ipywidgets import Dropdown, IntSlider, fixed

def interactive_taylor(functions, domain, yrange, degree_widget):
    """
    e.g. functions     = (np,sin, np.cos)
    e.g. domain        = np.linspace(0, 2*pi)
    e.g. yrange        = (-1, 1)
    e.g. degree_widget = IntSlider(...)
    """
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_ylim(yrange)

    # start with the first function
    f = functions[0]
    n = degree_widget.value
    ax.set_title(f"Taylor approx for {f.__name__} at degree {n}")
    plain_line = ax.plot(domain, f(domain))
    approx_line = ax.plot(domain, taylor2(domain, f, n))

    # [(label, value), ...]
    fun_options = [(f.__name__, f) for f in functions]
    @widgets.interact(function=Dropdown(options=fun_options), degree=degree_widget)
    def update_figure(function, degree):
        ax.lines[0].set_data(domain, f(domain))
        ax.lines[1].set_data(domain, taylor2(domain, f, n))
        ax.set_title(f"Taylor approx for {f.__name__} at degree {degree}")

interactive_taylor(
    (np.sin, np.cos),
    np.linspace(-3*np.pi, 3*np.pi, 100),
    (-1, 1),
    IntSlider(min=0, max=10, step=1, value=0))
```

```{code-cell} ipython3
# prune-end
```

le but du jeu est d'obtenir un matplotlib interactif de ce genre

```{image} taylor-3-example.png
:align: center
```

+++

***
