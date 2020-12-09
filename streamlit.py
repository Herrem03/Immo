# Packages
import streamlit as st
import pandas as pd
import altair as alt

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
    st.subheader('Analyse macro')
    df = pd.read_csv ('BdD.csv')
    st.dataframe(df) 

if page == "A propos":
    st.write('Auteur : Rémi Martinie')
    st.write('Version : v1.0.0')
