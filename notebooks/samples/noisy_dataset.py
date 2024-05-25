"""
module pour tester le traitement de séquences bruitées
"""

import random
import math

def generate_noisy_sequence(nb_element):
    """
    generate a noisy sequence of nb_element

    generate a sequence of nb_element containing random
    elements among integers in [-100, 100], floats in [-100, 100],
    and 'NaN'
    """
    # génère une list contenant les entiers de -100 à 100, 'NaN'
    # et 200 float entre -100 et 100
    seq = list(range(-100, 101))
    seq.extend(['NaN' for i in range(200)])
    seq.extend([random.uniform(-100, 101) for i in range(200)])


    # génère une liste contenant aléatoirement 10 000 éléments dans seq
    return [random.choice(seq) for i in range(nb_element)]


def compute(nb_element):
    """
    call generate_noisy_sequence(nb_element) to generate a list
    and compute the square root of all positive numbers
    """
    return [math.sqrt(x) for x in generate_noisy_sequence(nb_element)
          if (type(x) is int) and (x > 0)]


print(generate_noisy_sequence(20))
print(compute(100))
