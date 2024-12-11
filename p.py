import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors as pc

# Carica i dati dal file CSV come stringhe
columns = ['Country', 'Latitude', 'Longitude', '1996', '1998', '2000', '2002', '2004', 
           '2006', '2008', '2010', '2012', '2014', '2016', '2018', '2020', '2022']
df = pd.read_csv('datasets/normalized_completo.csv', delimiter=';', header=None, dtype=str)
df.columns = columns

# Converti Latitude e Longitude in float, gestendo eventuali "?"
df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')

# Funzione per convertire i visitatori moltiplicando per 1.000
def convert_visitors(value):
    if pd.isna(value) or value == '..':
        return np.nan
    try:
        value = value.replace('.', '')  # Rimuove il separatore delle migliaia
        return int(value) * 1000  # Moltiplica per 1.000
    except ValueError:
        return np.nan

# Applica la conversione alle colonne degli anni
for year in columns[3:]:
    df[year] = df[year].apply(convert_visitors)

# Range e colori per i visitatori
visitor_bins = [0, 10_000, 500_000, 1_000_000, 5_000_000, 15_000_000, 30_000_000, 50_000_000, float('inf')]
colors = ['#d3d3d3', '#b6d7a8', '#76a5af', '#6fa8dc', '#3d85c6', '#ff9900', '#cc0000', '#660000']
bin_labels = []
for i in range(len(visitor_bins) - 1):
    start = visitor_bins[i]
    end = visitor_bins[i + 1]
    label = f"{start:,} - {int(end-1):,}".replace(',', '.') if end != float('inf') else f"Oltre {start:,}".replace(',', '.')
    bin_labels.append(label)

# Funzione di scaling per le dimensioni dei marker
def scale_marker_size(visitors, min_size=6, max_size=18):
    if pd.isna(visitors) or visitors <= 0:
        return min_size
    max_visitors = df.iloc[:, 3:].max().max()
    scaled_size = min_size + (max_size - min_size) * (np.cbrt(visitors) / np.cbrt(max_visitors))
    return scaled_size

# Funzione per assegnare i bin ai visitatori
def assign_visitor_bin(visitors):
    for i in range(len(visitor_bins) - 1):
        if visitor_bins[i] <= visitors < visitor_bins[i + 1]:
            return i
    return None

# Inizializza le tracce per ogni bin di visitatori
traces = []
for i in range(len(visitor_bins) - 1):
    trace = go.Scattergeo(
        lon=[],
        lat=[],
        text=[],
        marker=dict(
            size=[],
            color=colors[i],
            line_width=0,
            showscale=False
        ),
        hoverinfo='text',
        name=bin_labels[i],
        legendgroup=bin_labels[i],
        showlegend=True
    )
    traces.append(trace)

# Anno iniziale
initial_year = '1996'

# Funzione per aggiornare i dati delle tracce per un anno specifico
def update_traces(year_data):
    data = []
    for i in range(len(visitor_bins) - 1):
        bin_data = year_data[year_data['VisitorBin'] == i]
        data_dict = dict(
            type='scattergeo',
            lon=bin_data['Longitude'].tolist() if not bin_data.empty else [],
            lat=bin_data['Latitude'].tolist() if not bin_data.empty else [],
            text=bin_data['Text'].tolist() if not bin_data.empty else [],
            marker=dict(size=bin_data['Size'].tolist() if not bin_data.empty else [])
        )
        data.append(data_dict)
    return data

# Prepara i dati per l'anno iniziale
year_data = df[df[initial_year].notna()].copy()
year_data['Size'] = year_data[initial_year].apply(scale_marker_size)
year_data['Text'] = year_data.apply(
    lambda row: f"{row['Country']}: {int(row[initial_year]):,} visitatori".replace(',', '.'),
    axis=1
)
year_data['VisitorBin'] = year_data[initial_year].apply(assign_visitor_bin)

# Aggiorna le tracce iniziali con i dati dell'anno iniziale
initial_data = update_traces(year_data)
for i in range(len(traces)):
    traces[i].lon = initial_data[i]['lon']
    traces[i].lat = initial_data[i]['lat']
    traces[i].text = initial_data[i]['text']
    traces[i].marker.size = initial_data[i]['marker']['size']

# Crea i frame per gli altri anni
frames = []
for year in columns[4:]:
    year_data = df[df[year].notna()].copy()
    year_data['Size'] = year_data[year].apply(scale_marker_size)
    year_data['Text'] = year_data.apply(
        lambda row: f"{row['Country']}: {int(row[year]):,} visitatori".replace(',', '.'),
        axis=1
    )
    year_data['VisitorBin'] = year_data[year].apply(assign_visitor_bin)
    frame_data = update_traces(year_data)
    frames.append(go.Frame(data=frame_data, name=year, traces=list(range(len(traces)))))

# Crea la figura
fig = go.Figure(data=traces, frames=frames)

# Imposta layout della mappa
fig.update_layout(
    title_text="Paesi destinazione scelti dai turisti dal 1996 al 2022",
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='equirectangular',
        showland=True,
        landcolor='white',
        showocean=True,
        # grigio chiarissimo per l'oceano in esadecimale
        oceancolor='#f0f0f0',
        showcountries=True,
        countrycolor='black',
        countrywidth=0.5
    ),
    legend=dict(
        title="Range di visitatori",
        x=1.05,
        y=0.5,
        traceorder="normal",
        itemsizing='constant'
    ),
    updatemenus=[
        {
            'type': 'buttons',
            'showactive': False,
            'x': 1,
            'y': 0,
            'xanchor': 'right',
            'yanchor': 'top',
            'buttons': [
                {
                    'label': 'Play',
                    'method': 'animate',
                    'args': [
                        None,
                        {'frame': {'duration': 1000, 'redraw': True}, 'fromcurrent': True}
                    ]
                },
                {
                    'label': 'Pause',
                    'method': 'animate',
                    'args': [
                        [None],
                        {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate'}
                    ]
                }
            ]
        }
    ]
)

# Aggiungi lo slider per cambiare anno
fig.update_layout(
    sliders=[{
        'steps': [
            {
                'method': 'animate',
                'label': str(year),
                'args': [
                    [str(year)],
                    {'frame': {'duration': 500, 'redraw': True}, 'mode': 'immediate'}
                ]
            }
            for year in columns[3:]
        ],
        'transition': {'duration': 500},
        'x': 0.1,
        'xanchor': 'left',
        'y': -0.05,
        'yanchor': 'top'
    }]
)

# Mostra la mappa
fig.show()