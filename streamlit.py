#Packages
import streamlit as st
import pandas as pd

#--------------Application Streamlit-------------#
#Sidebar
st.sidebar.title("Analyse projet immobilier")
page = st.sidebar.selectbox("Menu", ["Accueil", "Analyse macro", "Simulation", "A propos"])
st.sidebar.text('2020 v1.0.0')

if page == "Accueil":
    st.header('Avant-propos')
    st.markdown("Cet outil permet de simuler différents projets d'investissement immobilier à partir d'offres leboncoin.fr et seloger.com: ")
    st.markdown("- SCI ")
    st.markdown("- LMNP ")
    st.markdown("Le quartier est déterminé à partir de l'analyse sémantique de la description")

if page == "Simulation":
    st.subheader('Bien à analyser')
    url = st.text_input("Collez ici l'adresse url de l'annonce")
    st.markdown(':warning: Vérifiez la validité des informations extraites')
    st.subheader('Paramètres simulation')
    st.selectbox('Statut Fiscal', ['SCI', 'LMNP', 'SCCV'])
    st.slider("Nombre d'investisseurs", min_value=1, max_value=6, value=5, step=1)
    page = st.button("Aller à l'accueil","Accueil")

    @st.cache(allow_output_mutation=True)
    def get_data():
        return []

    user_id = st.text_input("User ID")
    foo = st.slider("foo", 0, 100)
    bar = st.slider("bar", 0, 100)

    if st.button("Add row"):
        get_data().append({"UserID": user_id, "foo": foo, "bar": bar})

    st.write(pd.DataFrame(get_data()))

if page == "Analyse macro":
    st.subheader('Analyse macro')

if page == "A propos":
    st.write('Auteur : Rémi Martinie')
    st.write('Version : v1.0.0')
