# Packages
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# Fonctions
def get_data():
    return []

annonces = pd.DataFrame(data={'url' : [], 'surface' : [],'prix' : []})

# --------------Application Streamlit-------------#
# Sidebar
st.sidebar.title("Analyse projet immobilier")
page = st.sidebar.selectbox("Menu", ["Accueil", "Analyse macro", "Simulation", "A propos"])
st.sidebar.text('2020 v1.0.0')

if page == "Accueil":
    st.header('Avant-propos')
    st.markdown("Cet outil permet de simuler différents projets d'investissement immobilier ")
    st.markdown("- SCI ")
    st.markdown("- LMNP ")

if page == "Simulation":
    st.subheader('Bien à analyser')
    url = st.text_input("Collez ici l'adresse url de l'annonce")
    st.markdown(':warning: Vérifiez la validité des informations extraites')
    st.subheader('Paramètres simulation')
    st.selectbox('Statut Fiscal', ['SCI', 'LMNP', 'SCCV'])
    st.slider("Nombre d'investisseurs", min_value=1, max_value=6, value=5, step=1)
    prix = st.number_input('Prix du bien')
    surface = st.number_input('Surface du bien')
    current = pd.DataFrame(data={'url' : [url], 'surface' : [surface],'prix' : [prix]})
    if st.button("Sauvegarder annonce"):
        annonces.append(current)
        st.write(annonces)
    st.selectbox('TMI', ['0%', '11%', '30%', '41%', '45%'])

if page == "Analyse macro":
    st.subheader('Analyse macro vente')
    df = pd.read_csv ('/home/herrem/Documents/Banque/Investissement/Projet immobilier/BdD.csv')
    st.dataframe(df)
    df['Prix de vente'] = df['Prix de vente'].astype(int)
    x = st.selectbox("Variable en abscisse", df.columns)
    y = st.selectbox("Variable en ordonnée", df.columns)
    st.vega_lite_chart(df, {
    "width": 600,
    "height": 600,
    'mark': {'type': 'circle', 'tooltip': {"content": "df"}},
    'encoding': {
    'x': {'field': x, 'type': 'quantitative'},
    'y': {'field': y, 'type': 'quantitative'},
    'size': {'field': 'Note localisation', 'type': 'quantitative'},
    "color": {
        "field": "Commune",
        "type": "nominal",
            },
        },
    })
    ville = st.selectbox('Sélectionner la ville', ['SAINT-ETIENNE', 'CLERMONT-FERRAND', 'GRENOBLE'])

    i= 0
    p_m=[]
    for x in df['Commune']:
        if ville == x:
            p_m.append(df['€/m²'][i])
        i+=1
    st.write('Prix moyen du m² €', round(np.mean(p_m),1))

    st.subheader('Analyse macro location')

if page == "A propos":
    st.write('Auteur : Rémi Martinie')
    st.write('Version : v1.0.0')


