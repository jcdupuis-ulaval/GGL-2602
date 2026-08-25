# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.23.3",
#     "matplotlib>=3.11.1",
#     "numpy>=2.5.2",
#     "pandas>=3.0.5",
#     "plotly>=7.0.0",
# ]
# ///

import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Message pour les personnes étudiantes
    """)
    return


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import ulgeophys as geophys
    import plotly.express as px
    import pandas as pd

    return geophys, mo, np, px


@app.cell
def _(mo):
    model_options =  ["prisme", "sphere"]
    model_selection = mo.ui.dropdown(options=model_options, value="prisme")
    model_selection
    return (model_selection,)


@app.cell
def _(mo):
    l = mo.ui.number(start=0,stop=500,label="l",value=1)
    e = mo.ui.number(start=0, stop=50,label="e",value=1)
    delta_rho = mo.ui.number(start=-2400, stop=2400,label="delta_rho",value=10)
    offset = mo.ui.number(start=-500,stop=500,label="offset",value=50)
    R = mo.ui.number(start=0.1,stop=100,label="Rayon",value=1)
    z = mo.ui.number(start=0,stop=100,label="z",value=1)
    return R, delta_rho, e, l, offset, z


@app.cell
def _(R, delta_rho, e, geophys, l, mo, model_selection, np, offset, z):
    x = np.linspace(0,500,500)
    if (model_selection.value == 'prisme'):
        _output = mo.vstack([l,mo.md(f"Longueur du prisme {l.value} m"),
               e,mo.md(f"Épaisseur du prisme {e.value} m"),
               delta_rho,mo.md(f" Différence de masse volumique {delta_rho.value}" + r"$\frac{kg}{m^3}$" ),
               offset,mo.md(f" Distance du prisme le long de la ligne {offset.value} m"),
               z,mo.md(f"Profondeur du prisme {z.value} m")],align="start")

    #gz = 2.0*e.value*(np.arctan((l.value-(x-offset.value))/z.value) + np.arctan((x-offset.value)/z.value))*delta_rho.value*G*1e5
        gz = geophys.grav_prisme(l.value,e.value,z.value,delta_rho.value,x,offset.value)
        sim_data = {"X(m)":x,"gz(mGal)":gz}
    else:
        _output = mo.vstack([R,mo.md(f"{R.value} m"), 
                             delta_rho,mo.md(f" {delta_rho.value}" + r"$\frac{kg}{m^3}$" ),
                             offset,mo.md(f"{offset.value} m"),
                             z,mo.md(f"{z.value} m")],align="center")
        gz = geophys.grav_sphere(R.value,z.value,delta_rho.value,x,offset.value)
        sim_data = {"X(m)":x,"gz(mGal)":gz}

    _output 
    return (sim_data,)


@app.cell
def _(mo, px, sim_data):
    _fig = px.line(sim_data,x="X(m)",y="gz(mGal)",labels=['Modèle'])
    '''_fig.add_trace(
        go.Scatter(
            x=data['pos'],
            y=field_data_raw-730.6,
        mode='markers',
        name = 'Données brutes')
    )'''
    plot = mo.ui.plotly(_fig)
    return (plot,)


@app.cell
def _(mo, plot):
    mo.hstack([plot])
    return


if __name__ == "__main__":
    app.run()
