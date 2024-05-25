---
jupytext:
  cell_metadata_filter: all
  cell_metadata_json: true
  encoding: '# -*- coding: utf-8 -*-'
  notebook_metadata_filter: all,-language_info,-toc,-jupytext.text_representation.jupytext_version,-jupytext.text_representation.format_version
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
notebookname: Mandelbrot
version: '1.0'
---

+++ {"run_control": {"frozen": false, "read_only": false}}

<div class="licence">
<span>Licence CC BY-NC-ND</span>
<span>Thierry Parmentelat &amp; Arnaud Legout</span>
</div>

```{code-cell} ipython3
---
run_control:
  frozen: false
  read_only: false
slideshow:
  slide_type: slide
trusted: true
---
import numpy as np
import matplotlib.pyplot as plt
%matplotlib ipympl
```

+++ {"run_control": {"frozen": false, "read_only": false}}

# l'ensemble de Mandelbrot

il s'agit de calculer l'image de la convergence de mandelbrot:

<img src="media/mandelbrot.svg">

+++

## comment ça marche ?

+++ {"cell_style": "center", "run_control": {"frozen": false, "read_only": false}, "slideshow": {"slide_type": "slide"}}

* dans l'espace complexe, on définit pour chaque $c\in\mathbb{C}$ la suite
   * $z_0 = c$
   * $z_{n+1} = z_n^2 + c$
* on démontre que 
  * lorsque $|z_n|>2$, la suite diverge

+++ {"cell_style": "center", "run_control": {"frozen": false, "read_only": false}, "slideshow": {"slide_type": "-"}}

il s'agit pour nous de 

* partir d'un pavé rectangulaire  
  par exemple sur la figure, on a pris l'habituel  
  $re \in [-2, 0.8]$ et  $im \in [-1.4, 1.4]$
* découper ce pavé en un maillage de $w \times h$ points  
  (sur la figure, 1000 x 1000)
* on se fixe un nombre maximal `max` d'itérations (disons 20)
  * et pour chaque point du maillage, on va calculer si la suite diverge avant `max` itérations
* c'est-à-dire plus spécifiquement on calcule un tableau `diverge` de la taille du maillage
  * pour chaque point `z`, on calcule les `max` premiers termes de la suite
  * et à la première itération `n` où la suite diverge (son module est supérieur à 2)  
    alors on affecte `diverge[z] = n`
* on n'a plus qu'à afficher ensuite l'image obtenue avec `plt.imshow`

+++ {"run_control": {"frozen": false, "read_only": false}, "slideshow": {"slide_type": "slide"}}

*indices*

* pour fabriquer la grille des points de départ, 
  on pourra regarder `np.linspace` et `np.meshgrid`

```{code-cell} ipython3
:trusted: true

# à vous de jouer
def mandelbrot(w, h):
    pass
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
:trusted: true

# prune-begin
```

# solution

+++ {"run_control": {"frozen": false, "read_only": false}, "slideshow": {"slide_type": "slide"}}

* une adaptation libre de l'[implementation proposée dans le tutorial scipy](https://docs.scipy.org/doc/numpy/user/quickstart.html#indexing-with-boolean-arrays)

```{code-cell} ipython3
---
run_control:
  frozen: false
  read_only: false
slideshow:
  slide_type: slide
trusted: true
---
import numpy as np
import matplotlib.pyplot as plt
```

```{code-cell} ipython3
---
run_control:
  frozen: false
  read_only: false
slideshow:
  slide_type: slide
trusted: true
---
# it's a little confusing that 
# real part = column = second dimension
# imag part = line =   first  dimension

def mandelbrot(height, width, *,
               re_range=(-2, 0.8), im_range=(-1.4, 1.4),
               max_iteration=20):
    """
    computes a height x width ndarray of integers that says after 
    how many iterations the mandelbrot suite for that point diverges
    
    Parameters:
      height(int): is the number of points in the height (imag) dimension
      width(int): is the number of points in the width (real) dimension
      re_range(tuple[float]): describes the real domain
      im_range(tuple[float]): describes the imag domain
      max_iteration: after that many iterations, a suite that does not diverge
        is deemed as converging
    """

    re1, re2 = re_range
    im1, im2 = im_range
    re, im = np.meshgrid(
        np.linspace(re1, re2, width),
        np.linspace(im1, im2, height))

    # an array of complexes
    c = re + 1j * im
    # initialize z 
    z = c
    # will contain the iteration where a divergence was found
    diverge_iteration = max_iteration + np.zeros( c.shape, dtype=int)

    for iteration in range(max_iteration):
        # create a new z array - c is left intact
        z = z * z + c
        # the complexes that diverged before this iteration
        bool_diverge = z * np.conj(z) > 4
        # the ones that diverged exactly at this iteration
        bool_diverge_now = bool_diverge & (diverge_iteration == max_iteration)
        # mark these
        diverge_iteration[bool_diverge_now] = iteration
        # avoid diverging too much ?
        z[bool_diverge] = 2

    return diverge_iteration
```

```{code-cell} ipython3
---
run_control:
  frozen: false
  read_only: false
scrolled: false
slideshow:
  slide_type: slide
trusted: true
---
plt.figure(figsize=(10, 10))
diverge = mandelbrot(1024, 1024)
plt.imshow(diverge)
plt.savefig("mandelbrot.svg", format="svg")
```

included as svg

```{image} mandelbrot.svg
:align: center
```
