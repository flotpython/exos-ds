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
  title: Taylor et numpy
---

# Taylor (2/3)

+++

On se propose d'approximer une fonction par la formule de Taylor

$$f_n(x) = \sum_{i=0}^{n}\frac{f^{(i)}(0).x^i}{i!}$$

+++

Ça semble être le bon moment d'utiliser `autograd`

```{code-cell} ipython3
# si nécessaire
# %pip install autograd

import autograd.numpy as np

from math import factorial
```

```{code-cell} ipython3
import matplotlib.pyplot as plt

%matplotlib ipympl
```

## exo v1

+++

### écrivez une fonction

```{code-cell} ipython3
def taylor1(X, derivatives):
    """
    X le domaine (sous-entendu, X[0]<0 et X[-1]>0)
    derivatives: une liste ou un tableau contenant les dérivées successives de f en 0
      i.e. derivatives[n] = f(n)(0) la dérivée n-ième de f en 0
    
    retourne un tableau Y qui est l'approximation de Taylor sur ce domaine pour une fonction
    qui aurait ces dérivées-là
    """
    # à vous
    ...
    shape = X.size,                                    # prune-line
    Y = np.zeros(shape)                                # prune-line
    for degree, derivative in enumerate(derivatives):  # prune-line
        Y += X**degree * derivative/factorial(degree)  # prune-line
    return Y                                           # prune-line
```

### testez la

+++

avec sinus

```{code-cell} ipython3
sinus10 = [0, 1, 0, -1, 0, 1, 0, -1, 0, 1]
```

écrivez le code qui plotte le résultat de `taylor1` sur le domaine X = $[-2\pi, 2\pi]$

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell 

X = np.linspace(-2*np.pi, 2*np.pi)
Y1 = taylor1(X, sinus10)

plt.figure()
plt.plot(X, Y1);
```

## exo v2

```{code-cell} ipython3
from autograd import grad
```

### écrivez une fonction

```{code-cell} ipython3
def taylor2(X, f, n):
    """
    X: le domaine
    f: la fonction
    n: le degré
    
    retourne un tableau Y qui est l'approximation de Taylor sur ce domaine pour cette fonction à ce degré
    """
    derivatives = []                                      # prune-line
    for degree in range(n):                               # prune-line
        # attention à bien passer 0. et pas l'entier 0    # prune-line
        derivatives.append(f(0.))                         # prune-line
        f = grad(f)                                       # prune-line
    print(derivatives)                                    # prune-line
    return taylor1(X, derivatives)                        # prune-line
```

### testez la

+++

avec sinus

```{code-cell} ipython3
# calculez Y2 l'image de X par l'approximation de Taylor pour sinus au degré 10
```

```{code-cell} ipython3
:scrolled: true
:tags: [level_basic]

# prune-cell

Y2 = taylor2(X, np.sin, 10)
```

```{code-cell} ipython3
# comparez Y2 avec Y, le résultat de sinus sur X
# avec ==
# avec isclose
# en les dessinant
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

Y = np.sin(X)

print("with ==\n", Y2 == Y)

print("with np.isclose\n", np.isclose(Y2, Y))
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

plt.figure()
plt.plot(X, Y)
plt.plot(X, Y2);
```

avec une fonction custom

```{code-cell} ipython3
# à vous

def custom(X):
    """
    retourne 2 * sin(X) + cos(X/4)
    """
    ...
    return 2*np.sin(X) + np.cos(X/4)      # prune-line
```

```{code-cell} ipython3
:tags: [raises-exception]

# calculez Y3 l'image de X par custom

Y3 = custom(X)                            # prune-line
```

```{code-cell} ipython3
:tags: [raises-exception]

# calculez Y4 l'image de X par l'approx. de custom d'ordre 20

Y4 = taylor2(X, custom, 20)                # prune-line
```

```{code-cell} ipython3
# comparez Y3 et Y4 comme ci-dessus

...
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell 

print("with ==\n", Y3 == Y4)

print("with np.isclose\n", np.isclose(Y3, Y4, rtol=10**-3))

plt.figure()
plt.plot(X, Y3)
plt.plot(X, Y4);
```

```{code-cell} ipython3
:tags: [raises-exception]

Y3/Y4
```

***
