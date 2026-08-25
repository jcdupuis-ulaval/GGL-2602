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
    import plotly.graph_objects as go
    import pandas as pd
    from plotly.subplots import make_subplots

    return geophys, go, make_subplots, mo, np, pd


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
        _output = mo.vstack([R,mo.md(f"Rayon de la sphère {R.value} m"), 
                             delta_rho,mo.md(f"Différence de masse volumique {delta_rho.value}" + r"$\frac{kg}{m^3}$" ),
                             offset,mo.md(f"Distance du centre de la sphère le long de la ligne {offset.value} m"),
                             z,mo.md(f"Profondeur du centre de la sphère {z.value} m")],align="start")
        gz = geophys.grav_sphere(R.value,z.value,delta_rho.value,x,offset.value)
        sim_data = {"X(m)":x,"gz(mGal)":gz}

    _output 
    return (sim_data,)


@app.cell
def _(go, mo, sim_data):
    _fig = go.Figure()
    _fig.add_trace(go.Scatter(x=sim_data['X(m)'], y=sim_data['gz(mGal)'], mode='lines', name='Modélisation'))

    plot = mo.ui.plotly(_fig)
    _fig.update_layout(
        xaxis_title="Distance X (m)",
        yaxis_title="Anomalie gravimétrique gz (mGal)"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Les données de terrain
    """)
    return


@app.cell
def _(mo):
    temperature = mo.ui.number(start=-40,stop=100,label="Température (°F)",value=0)
    temperature

    return (temperature,)


@app.cell
def _(geophys, pd, temperature):

    data_header=['pos','elevation', 'temps','lecture-1','lecture-2','lecture-3','lecture-4'] 
    data = pd.read_csv('./data/grav-data.csv',sep=',',names=data_header,header=None,skiprows=9) # read the raw data 
    data.columns = data_header # Assign the column names to the data frame
    average_reading = data.loc[:,'lecture-1':'lecture-4'].mean(axis=1) # Average at each station
    std_reading = data.loc[:,'lecture-1':'lecture-4'].std(axis=1) # Standard deviation at each station
    field_data_raw = average_reading*geophys.grav_worden_cal(t=temperature.value) # convert the readings to mGal using the Worden calibration
    return data, field_data_raw


@app.cell
def _(data, field_data_raw, go, make_subplots, sim_data):
    fig = make_subplots(rows=1, cols=2)

    fig.add_trace(
        go.Scatter(
            x=sim_data['X(m)'], 
            y=sim_data['gz(mGal)'],mode='lines', name='Modèle'), row=1, col=1)

    fig.add_trace(
        go.Scatter(
            x=data['pos'],
            y=field_data_raw,mode='markers',name='Données brutes',marker=dict(symbol='circle',size=5,color='red')),row=1, col=2)

    fig.update_layout(
        title_text="Modélisation et données de terrain",
        xaxis_title="Distance X (m)",
        yaxis_title="Anomalie gravimétrique gz (mGal)",
        xaxis2_title="Distance X (m)",
        yaxis2_title="Données brutes du gravimètre Worden",
    )

    fig.show()

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Conversion des données en mGal
    """)
    return


@app.cell
def _(field_data_raw):
    field_data_raw

    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
