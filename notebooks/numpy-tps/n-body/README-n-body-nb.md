---
authors: [Aubin Geoffre, Thierry Parmentelat]
date: 2025-09-20
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  name: python3
  display_name: Python 3 (ipykernel)
  language: python
language_info:
  name: python
  pygments_lexer: ipython3
  nbconvert_exporter: python
---

# n-body problem

+++

pour faire cette activité sur votre ordi localement, {download}`commencez par télécharger le zip<ARTEFACTS-n-body.zip>`

dans ce TP on vous invite à écrire un simulateur de la trajectoire de n corps qui interagissent entre eux au travers de leur poids, pour produire des sorties de ce genre

```{image} media/init3.png
:align: center
:width: 400px
```

+++

on suppose:

- on se place dans un monde en 2 dimensions
- on fixe au départ le nombre de corps N
- chacun est décrit par une masse constante
- et au début du monde chacun possède une position et une vitesse

+++

## imports

importer les librairies qui vont bien pour cet exercice; on utilisera le mode `ipympl` de `matplotlib`

```{code-cell} ipython3
# à vous
```

## initialisation

en fixant arbitrairement des limites dans l'espace des positions, des vitesses et des masses, on tire au hasard une configuration de départ pour la simulation

```{code-cell} ipython3
# les bornes pour le tirage au sort initial
mass_max = 3.
    
x_min, x_max = -10., 10.
y_min, y_max = -10., 10.

speed_max = 1.
```

```{code-cell} ipython3
# votre code

def init_problem(n):
    """
    retourne un tuple masses, positions, speeds
    """
    return None, None, None
```

```{code-cell} ipython3
# pour tester

# normalement vous devez pouvoir faire ceci

masses, positions, speeds = init_problem(10)

# et ceci devrait afficker OK
try:
    masses.shape == (10,) and positions.shape == speeds.shape == (2, 10)
    print("OK")
except:
    print("KO")
```

## les forces

à présent, on va écrire un fonction qui va calculer les influences de toutes les particules entre elles, suivant la loi de Newton


$$
\vec{F}_i = \sum_{\substack{j=1 \\ j \neq i}}^N 
   G \, m_i m_j \, \frac{\vec{r}_j - \vec{r}_i}{\lvert \vec{r}_j - \vec{r}_i \rvert^3}
$$

pour cela on se propose d'écrire la fonction suivante

```{code-cell} ipython3
# votre code

def forces(positions, masses, G=1.0):
    """
    returns an array of shape (2,  N)
    that contains the force felt by each mass from all the others
    G is the Newton constant and by default is set to 1 
    (we have abstract units anyway)
    """
    pass
```

## le simulateur

à présent il nous reste à utiliser cette brique de base pour "faire avancer" le modèle depuis son état initial et sur un nombre fixe d'itérations

cela pourrait se passer dans une fonction qui ressemblerait à ceci

```{code-cell} ipython3
# votre code

def simulate(masses, positions, speeds, dt=0.1, nb_steps=100):
    """
    should return the positions across time
    so an array of shape (nb_steps, N, 2)
    optional dt is the time step
    """
    pass
```

## dessiner

ne reste plus qu'à dessiner

```{code-cell} ipython3
# votre code

def draw(simulation, colors=None):
    """
    takes as input the result of simulate() above, 
    and draws the nb_steps positions of each of the N bodies
    ideally it should return a matplotlib Axes object

    one can provide a collection of N colors to use for each body
    if not provided this is randomized
    """
    pass
```

## putting it all together

on se met dans un état initial reproductible - surtout pour que vous puissiez facilement votre code

```{code-cell} ipython3
import numpy as np

def init3():
    # N = 3
    # the first element is heavy, at the center, and has no speed
    masses = np.array([3, 1, 1], dtype=float)
    positions = np.array([[0, 5, -5],[0, 1, -1]], dtype=float)
    speeds = np.array([[0, -1, 1],[0, 0, 0]], dtype=float)
    return masses, positions, speeds
```

```{code-cell} ipython3
# décommentez ceci pour tester votre code

# masses, positions, speeds = init3()
# s = simulate(masses, positions, speeds)
# print(f"{s.shape=}")
# draw(s);
```

et avec ces données vous devriez obtenir plus ou moins une sortie de ce genre
```{image} media/init3.png
```
