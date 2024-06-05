from math import factorial

import autograd
import autograd.numpy as np

from bokeh.plotting import figure, show

import streamlit as st

FORMULA = r"""
F_n(x) = \sum_{i=0}^{n} \frac{f^{(i)}(0)x^{i}}{i!}
"""

# 2024 june
# StreamlitAPIException: Streamlit only supports Bokeh version 2.4.3, but you have version 3.4.1 installed.
# Please run pip install --force-reinstall --no-deps bokeh==2.4.3 to install the correct version.
#
# to work around that, inspired from
# https://github.com/streamlit/streamlit/issues/5858#issuecomment-1482042533


import streamlit.components.v1 as components
from bokeh.plotting import figure, save
from bokeh.io import output_file


def use_file_for_bokeh(chart: figure, chart_height=500, **kwargs):
    if kwargs:
        print(f"ignoring extra keyword args {kwargs}")
    output_file('bokeh_graph.html')
    save(chart)
    with open("bokeh_graph.html", 'r', encoding='utf-8') as f:
        html = f.read()
    components.html(html, height=chart_height)


st.bokeh_chart = use_file_for_bokeh

# end workaround


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
