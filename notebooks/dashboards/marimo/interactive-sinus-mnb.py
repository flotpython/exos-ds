import marimo

__generated_with = "0.6.13"
app = marimo.App()


@app.cell
def __(mo):
    mo.accordion(
        { "### an interactive sinus plot with marimo":
        r"""

        display sinus with 2 sliders for tuning frequency and amplitude  
        **note** how to 2 **sliders** for the frequency are **kept in sync**; do achieve that our code just uses **the same variables** twice

        also here we have used *"Hide code"* to retain only the rendered markdown - quite optional of course

        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum    """
        })
    return


@app.cell
def __(amplitude, frequency, mo):
    mo.vstack([
        "for fun only: synced controls",
        mo.hstack([frequency, amplitude])
    ], align='center')
    return


@app.cell
def __(sinus):
    sinus()
    return


@app.cell
def __(amplitude, frequency, np, plt):
    def sinus():
        fig, ax = plt.subplots()
        X = np.linspace(0, 4*np.pi, 200)
        Y = amplitude.value * np.sin(X * frequency.value)
        plt.ylim((-6, 6))
        return ax.plot(X, Y)
    return sinus,


@app.cell
def __(amplitude, frequency, mo):
    mo.vstack([
        frequency,
        amplitude,
        (f"the frequency is {frequency.value} in Hz"
         f" and amplitude = {amplitude.value}")
    ], align='center')
    return


@app.cell
def __(ui):
    frequency = ui.slider(start=1, stop=10, step=0.1, label="frequency")
    amplitude = ui.slider(start=1, stop=5, step=0.5, label="amplitude")
    return amplitude, frequency


@app.cell
def __():
    import marimo as mo
    return mo,


@app.cell
def __(mo):
    ui = mo.ui
    return ui,


@app.cell
def __():
    import numpy as np
    import matplotlib.pyplot as plt
    return np, plt


if __name__ == "__main__":
    app.run()
