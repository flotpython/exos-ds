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
  title: Taylor et numpy
---

# Taylor (2/3): convergence

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
```

### testez la

+++

avec sinus

```{code-cell} ipython3
# les valeurs de sin et de ses dérivées successives en 0
# pour l'instant on les passe en dur
# (dans la partie suivante on les calculera)

sinus10 = [0, 1, 0, -1, 0, 1, 0, -1, 0, 1]
```

écrivez le code qui plotte le résultat de `taylor1` sur le domaine X = $[-2\pi, 2\pi]$ - devrait ressembler à ceci:

```{image} media/taylor2-v1.png
:width: 300px
```

```{code-cell} ipython3
X = np.linspace(-2*np.pi, 2*np.pi)
```

## exo v2

une fois que la logique d'accumulation est acquise, on va calculer les dérivées successives de la fonction

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
```

### testez la

````{admonition} rappel

pour comparer des flottants, il faut utiliser `isclose()` et non pas `==`
````

+++

avec sinus

```{code-cell} ipython3
# calculez Y2 l'image de X par l'approximation de Taylor pour sinus au degré 10
```

comparez Y2 avec Y, le résultat de sinus sur X en les dessinant - devrait ressembler à ceci:

```{image} media/taylor2-v2-sin.png
:width: 300px
```

+++

avec cosinus, au degré 0  - devrait ressembler à ceci:

```{image} media/taylor2-v2-cos.png
:width: 300px
```

```{code-cell} ipython3
# à vous
```

avec une fonction custom

```{code-cell} ipython3
# à vous

def custom(X):
    """
    retourne 2 * sin(X) + cos(X/4)
    """
    ...
```

```{code-cell} ipython3
:tags: [raises-exception]

# calculez Y3 l'image de X par custom
```

```{code-cell} ipython3
:tags: [raises-exception]

# calculez Y4 l'image de X par l'approx. de custom d'ordre 14
```

comparez Y3 et Y4 comme ci-dessus - devrait avoir cette allure

```{image} media/taylor2-v2-custom.png
:width: 300px
```

+++

***
