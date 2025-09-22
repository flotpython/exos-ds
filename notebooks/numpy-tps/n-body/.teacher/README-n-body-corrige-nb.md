---
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

dans ce TP on vous invite à écrire un simulateur de la trajectoire de n corps qui interagissent entre eux au travers de leurs masses, pour produire des sorties de ce genre

```{image} media/init3.png
:align: center
:width: 600px
```

+++

on suppose:

- on se place dans un monde en 2 dimensions
- on fixe au départ le nombre de corps N
- chacun est décrit par une masse constante
- et au début du monde chacun possède une position et une vitesse

```{admonition} la 3D
en option on vous proposera, une fois votre code fonctionnel en 2D, de passer à la 3D  
ça peut valoir le coup d'anticiper ça dès le premier jet, si vous vous sentez de le faire comme ça
```

+++

## imports

on pourra utiliser le mode `ipympl` de `matplotlib`

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt

%matplotlib ipympl
```

## initialisation aléatoire

en fixant arbitrairement des limites dans l'espace des positions, des vitesses et des masses, la fonction `init_problem()` tire au hasard une configuration de départ pour la simulation

```{code-cell} ipython3
# les bornes pour le tirage au sort initial
mass_max = 3.
    
x_min, x_max = -10., 10.
y_min, y_max = -10., 10.

speed_max = 1.
```

```{code-cell} ipython3
# votre code

def init_problem(N):
    """
    retourne un tuple masses, positions, speeds
    de formes resp.   (N,)    (2, N)     (2, N)
    tiré au sort dans les bornes définies ci-dessus
    """
    return None, None, None
```

```{code-cell} ipython3
# prune-cell

def init_problem(N):
    masses = np.random.uniform(0, mass_max, size=N)
    X = np.random.uniform(x_min, x_max, N)
    Y = np.random.uniform(y_min, y_max, N)
    angles = np.random.uniform(0, 2*np.pi, N)
    modules = np.random.uniform(0, speed_max, N)
    Sx = modules * np.cos(angles)
    Sy = modules * np.sin(angles)
    return (
        masses,
        # reshape(2, -1) is equivalent to (2, N) here
        np.concatenate((X, Y)).reshape((2, -1)), 
        np.concatenate((Sx, Sy)).reshape((2, -1))
       )
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

## initialisation reproductible

par commodité on vous donne la fonction suivante qui crée 3 objets:

- le premier - pensez au soleil - de masse 3, an centre de la figure, de vitesse nulle
- et deux objets de masse 1, disposés symétriquement autour du soleil  
  - position initiale (5, 1) et vitesse initiale (-1, 0)
  - symétrique en     (-5, -1) et vitesse initiale (1, 0)

```{code-cell} ipython3
# for your convenience

def init3():
    # first element is sun-like: heavy, at the center, and no speed
    masses = np.array([3, 1, 1], dtype=float)
    positions = np.array([
        [0, 5, -5], 
        [0, 1, -1]], dtype=float)
    speeds = np.array([
        [0, -1, 1], 
        [0, 0, 0]], dtype=float)
    return masses, positions, speeds
```

## les forces

à présent, on va écrire une fonction qui va calculer les influences de toutes les particules entre elles, suivant la loi de Newton


$$
\vec{F}_i = \sum_{\substack{j=1 \\ j \neq i}}^N 
   G \, m_i m_j \, \frac{\vec{r}_j - \vec{r}_i}{\lvert \vec{r}_j - \vec{r}_i \rvert^3}
$$

pour cela on se propose d'écrire la fonction suivante

```{code-cell} ipython3
# votre code

def forces(masses, positions, G=1.0):
    """
    returns an array of shape (2,  N)
    that contains the force felt by each mass from all the others
    G is the Newton constant and by default is set to 1 
    (we have abstract units anyway)
    """
    pass
```

```{code-cell} ipython3
# prune-cell

def forces(masses, positions, G=1.0):
    
    # creating an extra dimension so we can do the n-square difference
    delta = positions.T[None, :, :] - positions.T[:, None, :]  # (N, N, 2)

    distance2 = np.sum(delta**2, axis=-1)  # squared distances   (N, N)
    np.fill_diagonal(distance2, np.inf)    # avoid self-interaction

    distance3 = distance2 ** 1.5           # cubed distance      (N, N)
    
    # compute forces: F_ij = G * m_i * m_j * delta_ij / |r_ij|^3
    # (N, N, 2)
    forces_ij = G * delta / distance3[:, :, None] * (masses[None, :, None] * masses[:, None, None]) 
    
    # sum over j to get net force on i
    forces = np.sum(forces_ij, axis=1)  # (N, 2)
    
    return forces.T  # shape (2, N)
```

```{code-cell} ipython3
# pour tester, voici les valeurs attendues avec la config prédéfinie

masses, positions, speeds = init3()

f = forces(masses, positions)

# should be true
np.all(np.isclose(f, np.array([
    [ 0.        , -0.12257258,  0.12257258],
    [ 0.        , -0.02451452,  0.02451452]])))
```

## le simulateur

à présent il nous reste à utiliser cette brique de base pour "faire avancer" le modèle depuis son état initial et sur un nombre fixe d'itérations

cela pourrait se passer dans une fonction qui ressemblerait à ceci

```{code-cell} ipython3
# votre code

def simulate(masses, positions, speeds, dt=0.1, nb_steps=100):
    """
    should return the positions across time
    so an array of shape (nb_steps, 2, N)
    optional dt is the time step
    """
    pass
```

```{code-cell} ipython3
# prune-cell

def simulate(masses, positions, speeds, dt=0.1, nb_steps=100):
    # initialize result
    N = masses.shape[0]
    result = np.empty((nb_steps, 2, N))
    # store initial position
    result[0] = positions

    # because we have stored the initial state
    # we need to start at 1 here, we dont have space for more
    for step_counter in range(1, nb_steps):
        # compute forces and accelerations
        accelerations = forces(masses, positions) / masses

        # apply on speeds
        speeds += dt*accelerations

        # apply on positions
        positions += dt*speeds

        # store current position
        result[step_counter] = positions
    return result
```

```{code-cell} ipython3
# pour tester

SMALL_STEPS = 4

s = simulate(masses, positions, speeds, nb_steps=SMALL_STEPS)

try:
    if s.shape == (SMALL_STEPS, 2, 3):
        print("shape OK")
except Exception as exc:
    print(f"OOPS {type(exc)} {exc}")
```

```{code-cell} ipython3
# pour tester: should be true

positions1 = s[1]

np.all(np.isclose(positions1, np.array([
    [ 0.        ,  4.89877427, -4.89877427],
    [ 0.        ,  0.99975485, -0.99975485]
])))
```

## dessiner

ne reste plus qu'à dessiner; quelques indices potentiels:

- 1. chaque corps a une couleur; l'appelant peut vous passer un jeu de couleurs, sinon en tirer un au hasard
- 2.a pour l'épaisseur de chaque point, on peut imaginer utiliser la masse de l'objet  
  2.b ou peut-être aussi, à tester, la vitesse de l'objet (plus c'est lent et plus on l'affiche en gros ?)

```{admonition} masses et vitesses ?
j'ai choisi de repasser à `draw()` le tableau des masses à cause de 2.a;  
si j'avais voulu implémenter 2.b il faudrait tripoter un peu plus nos interfaces - car en l'état on n'a pas accès aux vitesses pendant la simulation - mais n'hésitez pas à le faire si nécessaire..
```

```{code-cell} ipython3
# votre code

def draw(simulation, masses, colors=None, scale=10.):
    """
    takes as input the result of simulate() above,
    and draws the nb_steps positions of each of the N bodies
    ideally it should return a matplotlib Axes object

    one can provide a collection of N colors to use for each body
    if not provided this is randomized

    also the optional scale parameter is used as a constant
    multiplier to obtain the final size of each dot on the figure
    """
    pass
```

```{code-cell} ipython3
# prune-cell

def draw(simulation, masses, colors=None, scale=5.):

    nb_steps, _, N = simulation.shape
    # use colors if provided, else randomize
    colors = (colors if colors is not None
              # not too dark
              else np.random.uniform(0.3, 1., size=(N, 3)))

    # create a figure and its axes
    fig, ax = plt.subplots()

    # not really needed but may come in handy though
    # ax.axis("off")
    # ax.set_aspect('equal')

    ax.set_title(f"we have {N} bodies over {nb_steps} steps")
    # looping on bodies, instead of on steps,
    # so we can also plot each trajectory
    for body_index, color in enumerate(colors):
        mass = masses[body_index]
        ax.scatter(
            # the X's and Y's
            simulation[:, 0, body_index], simulation[:, 1, body_index], 
            # marker size is actually an area
            color=color, s=(mass*scale)**2,
        )
        ax.plot(
            simulation[:, 0, body_index], simulation[:, 1, body_index], 
            color=color, alpha=0.5, linewidth=0.1
        )
    return ax
```

## un jeu de couleurs

```{code-cell} ipython3
# for convenience

colors3 = np.array([
    [32, 32, 32],
    (228, 90, 146),
    (111, 0, 255),
]) / 255
```

## on assemble le tout

pour commencer et tester, on se met dans l'état initial reproductible

```{code-cell} ipython3
# décommentez ceci pour tester votre code

# masses, positions, speeds = init3()
# draw(simulate(masses, positions, speeds), masses, colors3)
```

```{code-cell} ipython3
# prune-cell

steps = 100

masses, positions, speeds = init3()
s = simulate(masses, positions, speeds, nb_steps=steps)
draw(s, masses, colors3);

plt.savefig("init3.png")
```

et avec ces données vous devriez obtenir plus ou moins une sortie de ce genre
```{image} media/init3.png
```

```{code-cell} ipython3
# après vous avez le droit de vous enhardir avec des scénarii plus compliqués
# par exemple

# m5, p5, s5 = init_problem(5)
# sim5 = simulate(m5, p5, s5, nb_steps=200)
# draw(sim5, m5);
```

***
***
***

+++

## partie optionnelle

+++

### option 1: la 3D

modifiez votre code pour passer à une simulation en 3D

+++

### option 2: un rendu plus interactif

le rendu sous forme de multiple scatter plots donne une idée du résultat mais c'est très améliorable  
voyez un peu si vous arrivez à produire un outil un peu plus convivial pour explorer les résultats de manière interactive; avec genre

- une animation qui affiche les points au fur et à mesure du temps
- qu'on peut controler un peu comme une vidéo avec pause / backward / forward
- l'option de laisser la trace du passé
- et si vous avez un code 3d, la possibilité de changer le point de vue de la caméra sur le monde
- etc etc...

pas obligé de rester dans Jupyter Lab hein, il y a plein de technos rigolotes qui savent se décliner sur le web, vous avez l'embarras du choix...
