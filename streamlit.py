# Packages
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests
from lxml import html

# Fonctions
def get_data():
    return []


def scrap(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tree = html.fromstring(page.content)
    soup.prettify()
    surface = tree.xpath('//*[@id="grid"]/article/div[2]/div/div/div[2]/div/p[2]/text()')
    return surface


# --------------Application Streamlit-------------#
# Sidebar
st.sidebar.title("Analyse projet immobilier")
page = st.sidebar.selectbox("Menu", ["Accueil", "Analyse macro", "Simulation", "A propos"])
st.sidebar.text('2020 v1.0.0')

if page == "Accueil":
    st.header('Avant-propos')
    st.markdown(
        "Cet outil permet de simuler différents projets d'investissement immobilier à partir d'offres leboncoin.fr et seloger.com: ")
    st.markdown("- SCI ")
    st.markdown("- LMNP ")
    st.markdown("Le quartier est déterminé à partir de l'analyse sémantique de la description")

if page == "Simulation":
    st.subheader('Bien à analyser')
    choice = st.radio('Choisissez le mode de saisie', ['A la mano', "A partir de l'URL"])
    if choice == 'A la mano':
        st.write('Non disponible')
    if choice == "A partir de l'URL":
        url = st.text_input("Collez ici l'adresse url de l'annonce")
        st.markdown(':warning: Vérifiez la validité des informations extraites')
        #@st.cache(allow_output_mutation=True)
        if st.button("Sauvegarder annonce"):
            get_data().append({"URL ": url})

        annonce = pd.DataFrame(get_data())
        st.write(annonce)
        st.write(scrap(url))

    st.subheader('Paramètres simulation')
    st.selectbox('Statut Fiscal', ['SCI', 'LMNP', 'SCCV'])
    st.slider("Nombre d'investisseurs", min_value=1, max_value=6, value=5, step=1)

if page == "Analyse macro":
    st.subheader('Analyse macro')

if page == "A propos":
    st.write('Auteur : Rémi Martinie')
    st.write('Version : v1.0.0')
