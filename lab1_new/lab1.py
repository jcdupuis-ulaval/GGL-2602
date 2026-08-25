import marimo

__generated_with = "0.17.6"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Message pour les étudiants
    """)
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    slider = mo.ui.slider(1,10,label='Demo slider')
    slider
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
