import numpy as np
import matplotlib.pyplot as plt

import streamlit as st

st.set_page_config(layout="wide")

st.title("Sinusoidal with matplotlib")

freq = st.slider("frequency", value=1, min_value=1, max_value=10, step=1)

phase = 0

# .sidebar allows to put widgets on the left hand side
amplitude = st.sidebar.selectbox(
     'Amplitude',
     (.1, 1, 3, 5),
     # the index in the tuple above
     # so that initial value is 3
     index=2)

# keep it simple and use a fixed domain
domain = 4


def sinus4(freq, phase, amplitude, domain):

    figure = plt.figure(figsize=(10, 5))
    X = np.linspace(0., domain*np.pi, 250)
    Y = amplitude * np.sin(freq*(X+phase))
    # because we are going to mess with amplitude
    # let us fix the Y scale
    plt.ylim(-5, 5)
    plt.plot(X, Y)
    plt.legend()
    return figure


st.pyplot(fig=sinus4(freq, phase, amplitude, domain))
