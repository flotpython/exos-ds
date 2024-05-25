# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all,-hidden,-heading_collapsed,-run_control,-trusted
#     notebook_metadata_filter: all, -jupytext.text_representation.jupytext_version,
#       -jupytext.text_representation.format_version,-language_info.version, -language_info.codemirror_mode.version,
#       -language_info.codemirror_mode,-language_info.file_extension, -language_info.mimetype,
#       -toc, -rise, -version
#     text_representation:
#       extension: .py
#       format_name: light
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
#   language_info:
#     name: python
#     nbconvert_exporter: python
#     pygments_lexer: ipython3
# ---

# # a streamlit dashboard for Taylor

# ````{admonition} attention
# :class: warning
#
# this code won't work from a notebook, you need to kick it off from a terminal using (download as .py if needed)
# ```bash
# streamlit run streamlit-taylor.py
# ```
# ````
#
# This will open a browser page where you can interact with a dashboard that looks like this
#
# ```{image} streamlit-taylor.png
# :width: 500px
# ```

from math import factorial

import autograd
import autograd.numpy as np

from bokeh.plotting import figure, show

# +
import streamlit as st

FORMULA = r"""
F_n(x) = \sum_{i=0}^{n} \frac{f^{(i)}(0)x^{i}}{i!}
"""


# -

class Taylor:
    """
    provides an animated view of Taylor approximation
    where one can change the degree interactively

    Taylor is applied on X=0, translate as needed
    """

    def __init__(self, function, domain, y_range):
        self.function = function
        self.domain = domain
        self.y_range = y_range

    def display(self, degree):
        """
        create full drawing

        Parameters:
          y_range: a (ymin, ymax) tuple
            for the animation to run smoothly, we need to display
            all Taylor degrees with a fixed y-axis range
        """
        # create figure
        x_range = (self.domain[0], self.domain[-1])
        self.figure = figure(title=self.function.__name__,
                             x_range=x_range, y_range=self.y_range)

        # each of the 2 curves is a bokeh line object
        self.figure.line(self.domain, self.function(self.domain), color='green')
        self.line_approx = self.figure.line(
            self.domain, self._approximated(degree), color='red', line_width=2)

        st.bokeh_chart(self.figure, use_container_width=True)

    def _approximated(self, degree):
        """
        Computes and returns the Y array, the images of the domain
        through Taylor approximation

        Parameters:
          degree: the degree for Taylor approximation
        """
        # initialize with a constant f(0)
        # 0 * self.domain allows to create an array
        # with the right length
        result = 0 * self.domain + self.function(0.)
        # f'
        derivative = autograd.grad(self.function)
        for n in range(1, degree+1):
            # the term in f(n)(x)/n!
            result += derivative(0.)/factorial(n) * self.domain**n
            # next-order derivative
            derivative = autograd.grad(derivative)
        return result


st.title("Taylor approximation of sin(x)")

st.latex(FORMULA)

degree = st.slider(
    "enter degree n", value=1, step=2,
    help="the degree of the approximating polynom; the higher the degree, the better the match")

max_domain = st.number_input(
    "enter max X (in π)", value=4,
    help="the figure will use a [0, MAX] domain in the X dimension"
)

DOMAIN = np.linspace(0, max_domain*np.pi, 1000)

# an instance
animator = Taylor(np.sin, DOMAIN, (-1.5, 1.5))

animator.display(degree)
