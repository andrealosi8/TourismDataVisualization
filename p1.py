import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors as pc

# Percorso del file CSV
file_path = "datasets/staticon.csv"

# Carica il dataset con il separatore corretto
df = pd.read_csv(file_path, sep=';')

# Stampa i Paesi riconosciuti da Plotly
# countries_plotly = px.data.gapminder()['country'].unique()
# print("Paesi riconosciuti da Plotly:")
# print("Numero di paesi riconosciuti da Plotly:", len(countries_plotly))
# print(countries_plotly)

# Stampa i Paesi riconosciuti dal dataset
# print("Paesi presenti nel dataset:")
# print("Numero di paesi presenti nel dataset:", len(df['Stati parti'].unique()))
# print(df['Stati parti'].unique())

country_mapping = {
    'Afganistan': 'Afghanistan',
    'Albania': 'Albania',
    'Algeria': 'Algeria',
    'Andorra': 'Andorra',
    'Angola': 'Angola',
    'Antigua e Barbuda': 'Antigua and Barbuda',
    'Argentina': 'Argentina',
    'Armenia': 'Armenia',
    'Australia': 'Australia',
    'Austria': 'Austria',
    'Azerbaigian': 'Azerbaijan',
    'Bahrein': 'Bahrain',
    'Bangladesh': 'Bangladesh',
    'Barbados': 'Barbados',
    'Bielorussia': 'Belarus',
    'Belgio': 'Belgium',
    'Belize': 'Belize',
    'Benin': 'Benin',
    'Bolivia (Stato Plurinazionale di)': 'Bolivia',
    'Bosnia ed Erzegovina': 'Bosnia and Herzegovina',
    'Botswana': 'Botswana',
    'Brasile': 'Brazil',
    'Bulgaria': 'Bulgaria',
    'Burkina Faso': 'Burkina Faso',
    'Capo Verde': 'Cape Verde',
    'Cambogia': 'Cambodia',
    'Camerun': 'Cameroon',
    'Canada': 'Canada',
    'Repubblica Centrafricana': 'Central African Republic',
    'Chad': 'Chad',
    'Chile': 'Chile',
    'Cina': 'China',
    'Colombia': 'Colombia',
    'Congo': 'Congo, Rep.',
    'Costa Rica': 'Costa Rica',
    "Costa d'Avorio": "Cote d'Ivoire",
    'Croazia': 'Croatia',
    'Cuba': 'Cuba',
    'Cipro': 'Cyprus',
    'Repubblica Ceca': 'Czech Republic',
    'Repubblica Popolare Democratica di Corea': 'North Korea',
    'Repubblica Democratica del Congo': 'Congo, Dem. Rep.',
    'Danimarca': 'Denmark',
    'La dominica': 'Dominica',
    'Repubblica Dominicana': 'Dominican Republic',
    'Ecuador': 'Ecuador',
    'Egitto': 'Egypt',
    'El Salvador': 'El Salvador',
    'Eritrea': 'Eritrea',
    'Estonia': 'Estonia',
    'Etiopia': 'Ethiopia',
    'Figi': 'Fiji',
    'Finlandia': 'Finland',
    'Francia': 'France',
    'Gabon': 'Gabon',
    'Gambia': 'Gambia',
    'Georgia': 'Georgia',
    'Germania': 'Germany',
    'Ghana': 'Ghana',
    'Grecia': 'Greece',
    'Guatemala': 'Guatemala',
    'Guinea': 'Guinea',
    'Haiti': 'Haiti',
    'Santa Sede': 'Holy See',
    'Honduras': 'Honduras',
    'Ungheria': 'Hungary',
    'Islanda': 'Iceland',
    'India': 'India',
    'Indonesia': 'Indonesia',
    "Iran (Repubblica Islamica dell')": 'Iran',
    'Iraq': 'Iraq',
    'Irlanda': 'Ireland',
    'Israele': 'Israel',
    'Italia': 'Italy',
    'Giamaica': 'Jamaica',
    'Giappone': 'Japan',
    'Giordania': 'Jordan',
    'Kazakistan': 'Kazakhstan',
    'Kenia': 'Kenya',
    'Kiribati': 'Kiribati',
    'Kirghizistan': 'Kyrgyzstan',
    'Repubblica Democratica Popolare del Laos': 'Laos',
    'Lettonia': 'Latvia',
    'Libano': 'Lebanon',
    'Lesoto': 'Lesotho',
    'Libia': 'Libya',
    'Lituania': 'Lithuania',
    'Lussemburgo': 'Luxembourg',
    'Madagascar': 'Madagascar',
    'Malawi': 'Malawi',
    'Malaysia': 'Malaysia',
    'Mali': 'Mali',
    'Malta': 'Malta',
    'Isole Marshall': 'Marshall Islands',
    'Mauritania': 'Mauritania',
    'Maurizio': 'Mauritius',
    'Messico': 'Mexico',
    'Micronesia (Stati Federati di)': 'Micronesia',
    'Mongolia': 'Mongolia',
    'Montenegro': 'Montenegro',
    'Marocco': 'Morocco',
    'Mozambico': 'Mozambique',
    'Birmania': 'Myanmar',
    'La Namibia': 'Namibia',
    'Nepal': 'Nepal',
    'Paesi Bassi (Regno dei)': 'Netherlands',
    'Nuova Zelanda': 'New Zealand',
    'Nicaragua': 'Nicaragua',
    'Niger': 'Niger',
    'Nigeria': 'Nigeria',
    'Macedonia del Nord': 'North Macedonia',
    'Norvegia': 'Norway',
    'Oman': 'Oman',
    'Pakistan': 'Pakistan',
    'Palau': 'Palau',
    'Panama': 'Panama',
    'Papua Nuova Guinea': 'Papua New Guinea',
    'Il Paraguay': 'Paraguay',
    'Perù': 'Peru',
    'Filippine': 'Philippines',
    'Polonia': 'Poland',
    'Portogallo': 'Portugal',
    'Qatar': 'Qatar',
    'Repubblica di Corea': 'South Korea',
    'Repubblica di Moldavia': 'Moldova',
    'Romania': 'Romania',
    'Federazione Russa': 'Russia',
    'Ruanda': 'Rwanda',
    'Saint Kitts e Nevis': 'Saint Kitts and Nevis',
    'Santa Lucia': 'Saint Lucia',
    'San Marino': 'San Marino',
    'Arabia Saudita': 'Saudi Arabia',
    'Senegal': 'Senegal',
    'Serbia': 'Serbia',
    'Le Seychelles': 'Seychelles',
    'Singapore': 'Singapore',
    'Slovacchia': 'Slovakia',
    'Slovenia': 'Slovenia',
    'Isole Salomone': 'Solomon Islands',
    'Sudafrica': 'South Africa',
    'Spagna': 'Spain',
    'Sri Lanka': 'Sri Lanka',
    'Stato di Palestina': 'Palestine',
    'Sudan': 'Sudan',
    'Suriname': 'Suriname',
    'Svezia': 'Sweden',
    'Svizzera': 'Switzerland',
    'Repubblica araba siriana': 'Syria',
    'Tagikistan': 'Tajikistan',
    'Thailandia': 'Thailand',
    'Togo': 'Togo',
    'Tunisia': 'Tunisia',
    'Turchia': 'Turkey',
    'Turkmenistan': 'Turkmenistan',
    'Uganda': 'Uganda',
    'Ucraina': 'Ukraine',
    'Emirati Arabi Uniti': 'United Arab Emirates',
    'Regno Unito di Gran Bretagna e Irlanda del Nord': 'United Kingdom',
    'Repubblica Unita di Tanzania': 'Tanzania',
    "Stati Uniti d'America": 'United States',
    'Uruguay': 'Uruguay',
    'Uzbekistan': 'Uzbekistan',
    'Vanuatu': 'Vanuatu',
    'Venezuela (Repubblica Bolivariana del)': 'Venezuela',
    'Vietnam': 'Vietnam',
    'Yemen': 'Yemen',
    'Zambia': 'Zambia',
    'Zimbabwe': 'Zimbabwe'
}

# Verifica se ci sono Paesi nel dataset senza corrispondenza
# missing_countries = df[~df['Stati parti'].isin(country_mapping.keys())]['Stati parti'].unique()
# print("Paesi non mappati:", missing_countries)

df['Stati parti'] = df['Stati parti'].map(country_mapping)
# Stampa i nomi delle colonne per conferma
# print("Colonne disponibili nel dataset:", df.columns)

# Usa la colonna 'Stati parti' per contare i siti UNESCO per Paese
# Se la colonna 'Proprietà iscritte' è il numero di siti, somma i valori per ogni Paese
sites_by_country = df.groupby('Stati parti')['Proprietà iscritte'].sum().reset_index()

# Rinomina le colonne per chiarezza
sites_by_country.columns = ['Country', 'SiteCount']

# Creazione della mappa coropletica
fig_map = px.choropleth(
    sites_by_country,
    locations="Country",  # Nome della colonna per i Paesi
    locationmode="country names",  # Modalità: nomi dei Paesi
    color="SiteCount",  # Valore da visualizzare
    title="Numero di siti UNESCO per Paese",
    color_continuous_scale=px.colors.sequential.Plasma,
    hover_name="Country",  # Mostra il nome del Paese quando si passa sopra
    hover_data=["SiteCount"],  # Mostra anche il conteggio dei siti
)

fig_map.show()

# Creazione del grafico a barre
fig_bar = px.bar(
    sites_by_country.sort_values(by="SiteCount", ascending=False),
    x="Country",
    y="SiteCount",
    title="Numero di siti UNESCO per Paese",
    labels={"SiteCount": "Numero di siti", "Country": "Paese"},
    text="SiteCount",
    color="SiteCount",  # Colorazione in base al numero di siti
    color_continuous_scale=px.colors.sequential.Plasma  # Cambia la scala dei colori
)

# Evidenzia l'Italia in rosso
# fig_bar.update_traces(marker_color=sites_by_country['Country'].apply(
#     lambda x: 'red' if x == 'Italy' else px.colors.sequential.Plasma[0]
# ))

# Aggiungi miglioramenti estetici (rotazione delle etichette e miglioramento del layout)
fig_bar.update_layout(
    xaxis_tickangle=-45,  # Ruota le etichette sull'asse x
    xaxis_title="Paese",
    yaxis_title="Numero di siti",
    title_x=0.5,  # Centra il titolo
    title_y=0.95,  # Aggiusta la posizione del titolo
    title_font_size=18,
    showlegend=False  # Nascondi la legenda
)

fig_bar.show()