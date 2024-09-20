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
```

```{code-cell} ipython3
# et on aura besoin aussi de 

from math import factorial

%matplotlib ipympl
import matplotlib.pyplot as plt
```

## exo v1

+++

### écrivez une fonction

```{code-cell} ipython3
:tags: [level_basic]

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

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell 

Y1 = taylor1(X, sinus10)

plt.figure()
plt.plot(X, Y1);

# do not overwrite each time as it messes incremental builds
# plt.savefig("media/taylor2-v1.png")
```

## exo v2

une fois que la logique d'accumulation est acquise, on va calculer les dérivées successives de la fonction

```{code-cell} ipython3
# en utilisant l'outil qu'on a vu dans la première partie

from autograd import grad
```

### écrivez une fonction

```{code-cell} ipython3
:tags: [level_basic]

def taylor2(X, f, n):
    """
    X: le domaine
    f: la fonction
    n: le degré
    
    retourne un tableau Y qui est l'approximation de Taylor sur ce domaine pour cette fonction à ce degré
    """
    derivatives = []                                      # prune-line
    # la somme est de 0 à n inclusivement                 # prune-line
    for degree in range(n+1):                             # prune-line
        # attention à bien passer 0. et pas l'entier 0    # prune-line
        derivatives.append(f(0.))                         # prune-line
        f = grad(f)                                       # prune-line
    # print(derivatives)                                  # prune-line
    return taylor1(X, derivatives)                        # prune-line
```

## testons la v2

+++

### avec sinus au degré 10

```{code-cell} ipython3
:tags: []

# Y est le sinus de X
# Y2 est l'image de X par l'approximation de Taylor pour sinus au degré 10

Y  = np.sin(X)
Y2 = taylor2(X, np.sin, 10)
```

1. comparez Y2 avec Y en les dessinant sur la même courbe - devrait ressembler à ceci:

```{image} media/taylor2-v2-sin.png
:width: 300px
```

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

plt.figure()
plt.plot(X, Y)
plt.plot(X, Y2);
# plt.savefig("media/taylor2-v2-sin.png")
```

2. regardez la coincidence de Y et Y2

quel est le pourcentage du domaine pour lequel l'approximation est valide à $10^{-3}$ près ?

````{admonition} rappel
:class: admonition-small dropdown

on rappelle que `==` n'est pas le bon outil pour comparer les flottants
````

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

compare = np.isclose(Y2, Y, rtol=10**-3)
sum(compare) / len(compare)
```

### avec cosinus, au degré 0

1. affichez cos et son approximation au degré 0, qui devrait ressembler à ceci:

```{image} media/taylor2-v2-cos.png
:width: 300px
```

```{code-cell} ipython3
# à vous
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

Y = np.cos(X)
Y2 = taylor2(X, np.cos, 0)

# prune-cell

plt.figure()
plt.plot(X, Y)
plt.plot(X, Y2);

# plt.savefig("media/taylor2-v2-cos.png")
```

### avec une fonction custom

+++

1. à vous de compléter cette fonction

```{code-cell} ipython3
def custom(X):
    """
    retourne 2 * sin(X) + cos(X/4)
    """
    ...
    return 2*np.sin(X) + np.cos(X/4)      # prune-line
```

+++ {"tags": ["raises-exception"]}

2. calculez Y3 l'image de X par custom  
   et Y4 l'image de X par l'approx. de custom d'ordre 14

```{code-cell} ipython3
:tags: [raises-exception, level_basic]

# prune-cell

Y3 = custom(X)
Y4 = taylor2(X, custom, 14)
```

3. comparez Y3 et Y4 comme ci-dessus - devrait avoir cette allure

```{image} media/taylor2-v2-custom.png
:width: 300px
```

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell 

plt.figure()
plt.plot(X, Y3)
plt.plot(X, Y4);

#don't do this repeatedly to not mess incremental builds
# plt.savefig("media/taylor2-v2-custom.png")
```

4. sur quel pourcentage du domaine a-t-on coincidence à $10^{-3}$ près ?

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
:scrolled: true
:tags: [level_basic]

# prune-cell

compare = np.isclose(Y3, Y4, rtol=10**-3)
sum(compare) / len(compare)
```
