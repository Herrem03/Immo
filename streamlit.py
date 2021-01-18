# Packages
import streamlit as st
import pandas as pd
import altair as alt
import os, sys
import numpy as np
import plotly.graph_objects as go

os.getcwd()
reload(sys)
sys.setdefaultencoding('utf8')

# --------------Data-------------#
data_vente = pd.read_csv ('BdD_vente.csv')


data_loc = pd.read_csv ('BdD_location.csv')

#Fonctions simulation

def mensualite(capital, taux_mensuel, duree):
    mensualite = capital * (taux_mensuel/100 / (1 - (1 + taux_mensuel/100) ** (-duree*12)))
    return mensualite

def credit(travaux, prix, apport, notaire, taux, duree):
    capital = travaux + prix * (1 + notaire/100) - apport
    taux_mensuel = (np.power(1 + taux / 100, 0.083333333333333) - 1)*100 #error 1/12 = 0.083333 not working

    rng = pd.RangeIndex(0, stop = duree * 12 +1, step = 1)
    data = pd.DataFrame(index=rng, columns=['mensualite', 'montant remboursé', 'charge intérêt', 'capital dû'], dtype='float')
    data['mensualite'] = round(mensualite(capital, taux_mensuel, duree),3)
    data.loc[0,'charge intérêt'] = 0
    data.loc[0, 'montant remboursé'] = 0
    data.loc[0, 'capital dû'] = capital

    for x in range(1,len(data)):
        data.loc[x, 'charge intérêt'] = round(data.loc[x-1, 'capital dû'] * taux_mensuel / 100,3)
        data.loc[x, 'montant remboursé'] = round(data.loc[x, "mensualite"] - data.loc[x, "charge intérêt"],3)
        if data.loc[x-1, 'capital dû'] < data.loc[x, 'mensualite']:
            data.loc[x, 'montant remboursé'] = data.loc[x-1, 'capital dû'] - data.loc[x, 'charge intérêt']
            data.loc[x, 'capital dû'] = 0
            continue
        elif data.loc[x, 'montant remboursé'] <= data.loc[x-1, 'capital dû']:
            data.loc[x, 'capital dû'] = round(data.loc[x-1, 'capital dû'] - data.loc[x, 'montant remboursé'],3)

    return data

# --------------Application Streamlit-------------#

# Sidebar
st.sidebar.title("Analyse projet immobilier")
page = st.sidebar.selectbox("Menu", ["Accueil", "Analyse macro", "Simulation", 'README'])

#Page d'accueil
if page == "Accueil":
    st.header('Avant-propos')
    st.markdown("Cet outil permet de simuler différents projets d'investissement immobilier ")

#Page analyse macro
if page == "Analyse macro":
    st.header('Analyse macro vente')
    if st.button('Voir le tableau de vente'):
        st.dataframe(data_vente)
        if st.button('Cacher le tableau'):
            None

    st.vega_lite_chart(data_vente, {
        "width": 800,
        "height": 600,
        'mark': {'type': 'circle', 'tooltip': {"content": "df"}},
        'encoding': {
            'x': {'field': ['Surface totale'], 'type': 'quantitative'},
            'y': {'field': ['Prix de vente'], 'type': 'quantitative'},
            'size': {'field': 'Note localisation', 'type': 'quantitative'},
            "color": {
                "field": "Commune",
                "type": "nominal",
            },
        },
    })

    macro_vente = data_vente.groupby('Commune').agg(
        {
         'Autres coûts /an': 'mean',
         'Coût copro /an': 'mean',
         'Coût charge /an': 'mean',
         'Prix de vente': 'mean',
         'Surface totale' : 'mean'
        })
    st.table(macro_vente)
    st.subheader('€/m² en vente')
    e_m2_vente = macro_vente['Prix de vente'] / macro_vente['Surface totale']
    st.table(e_m2_vente)


    st.header('Analyse macro location')
    if st.button('Voir le tableau de location'):
        st.dataframe(data_loc)
        if st.button('Cacher le tableau'):
            None

    st.vega_lite_chart(data_loc, {
        "width": 800,
        "height": 600,
        'mark': {'type': 'circle', 'tooltip': {"content": "df"}},
        'encoding': {
            'x': {'field': ['Surface totale m²'], 'type': 'quantitative'},
            'y': {'field': ['Loyer colocation €/mois'], 'type': 'quantitative'},
            'size': {'field': 'Note localisation', 'type': 'quantitative'},
            "color": {
                "field": "Commune",
                "type": "nominal",
            },
        },
    })

    macro_loc = data_loc.groupby('Commune').agg(
        {
         'Loyer location €/mois avec charges': 'mean',
         'Coût charge /chambre (si coloc) /an': 'mean',
         'Loyer colocation €/mois': 'mean',
         'Surface totale m²' : 'mean'
        })
    st.table(macro_loc)
    st.subheader('€/m² en location par an')
    e_m2_loc = macro_loc['Loyer colocation €/mois'] *12 / macro_loc['Surface totale m²']
    st.table(e_m2_loc)

    st.header('Rentabilité brute')
    st.write(':warning: La rentabilité brute ne tient pas compte des charges mensuelles à déduire. Elle est affichée ci-dessous en %.')
    st.table(e_m2_loc * 100/e_m2_vente)

#Page simulation
if page == "Simulation":
    st.header('Bien à analyser')
    url = st.text_input("Collez ici l'adresse url de l'annonce")

    st.markdown('------------------------------------------------------')
    st.header("""Données d'entrée simulation""")
    st.subheader("""Paramètres immobiliers""")
    ville = st.selectbox('Ville', ['SAINT-ETIENNE', 'CLERMONT-FERRAND', 'GRENOBLE', 'VALENCE'])
    prix = st.number_input('Prix du bien [€]', value = 100000)
    notaire = float(st.number_input('Frais de notaire [%]', value = 8.00))
    surface = st.number_input('Surface du bien [m²]')
    n_chambres = st.number_input('Nombre de chambres',min_value = 0, max_value = 6, value = 3, step = 1)
    loyer_hc = st.number_input('Loyer HC / chambre [€]', min_value=0, max_value=600, value=350, step=1)
    travaux = st.number_input('Travaux [€]')
    tx_occup = st.slider("Taux d'occupation [mois]", min_value=1, max_value=12, value=11, step=1)
    TMI = st.selectbox("Taux Marginal d'Imposition [%]", ['0%', '11%', '30%', '41%', '45%'])
    apport = st.number_input("Montant de l'apport [€/investisseur]")
    provision = st.number_input("Provision pour risques [mois de loyer HC]")
    nego = st.number_input("Négociation du bien [%]")
    st.markdown('**Charges annuelles**')
    st.markdown("*Suggestion automatique de la moyenne issue de la base de donnée pour les 3 champs suivants :*" )
    taxe_fonciere = st.number_input('Taxe foncière [€]')
    cout_copro = st.number_input('Coût copropriété annuel [€]')
    charges = st.number_input('Charges annuelles [€]')
    if st.checkbox("Frais d'agence 5%"):
        agence = 5

    st.subheader("""Paramètres bancaires""")
    st.slider("Nombre d'investisseurs", min_value=1, max_value=6, value=4, step=1)
    duree = st.slider("Durée de l'emprunt [années]", min_value=1, max_value=30, value=20, step=1)
    tx_emprunt = float(st.number_input("TAEG [%]", value = 1.2))

    st.markdown('------------------------------------------------------')
    st.subheader('Simulation')
    st.markdown(':warning: Ne pas lancer la simulation sans avoir rempli tous les champs.')

    if st.button('Lancer la simulation'):
        st.subheader('Crédit bancaire')
        credit_tab = credit(travaux, prix, apport, notaire, tx_emprunt, duree)
        cout_annuel_emprunt = round(credit_tab.loc[2, 'mensualite'] * 12, 2)
        st.write('Coût total emprunt [€] :', round(credit_tab['charge intérêt'].sum(),2))
        st.write('Somme totale empruntée [€] :', round(credit_tab['mensualite'].sum(),2))
        st.write('Coût annuel emprunt [€] :', cout_annuel_emprunt)
        st.write(credit_tab)

        st.subheader('Recettes annuelles')

        st.subheader('Frais annuels')

        st.subheader('Fiscalité')

        st.subheader('Trésorerie SCI')
        EBE = n_chambres * loyer_hc * tx_occup
        benefice_net = (EBE - cout_annuel_emprunt - taxe_fonciere - charges -cout_copro)*(0.85)
        st.write("Excédent brut d'exploitation [€] :", EBE)
        st.write("Bénéfice net annuel [€] :", benefice_net)
        #warnings
        st.header('Synthèse')
        st.button('Télécharger le Business Plan en pdf')

if page == "README":
    st.header('Calcul du crédit bancaire')
    st.subheader(":money_with_wings: Calcul du taux mensuel")
    st.latex(r'''
            t_m = \left(\left((1 + \frac{t_{annuel}}{100}\right)^{\frac{1}{12}} - 1 \right) .100
            ''')
    st.subheader(":money_with_wings: Calcul de la mensualité")
    st.latex(r'''
            m = \frac{C_0.t_m}{1 - (1+t_m)^{-n}}
            ''')
    st.latex( "C_0 : capital~emprunté ")
    st.latex("t_m : taux~mensuel")
    st.latex("n : durée ")
    st.write("Le **capital initial** comprend le prix du bien, des travaux, des frais de notaire. La **durée** est en mois.")

    st.subheader(":money_with_wings: Calcul de la charge mensuelle d'intérêts")
    st.latex(r'''
            CI_{M} = C_{M-1}.t_m
            ''')
    st.write("La **charge d'intérêt** au mois *M* est calculée sur la base du capital restant du mois *M-1*")

    st.subheader(":money_with_wings: Calcul du capital mensuel remboursé ")
    st.latex(r'''
            c_{M} = m - CI_{M}
            ''')
    st.write("Le **capital remboursé** chaque mois équivaut à la charge d'intérêt mensuelle soustraite de la mensualité")

    st.write("----------------------------------------------------------------------------------")
    st.header('Comptabilité SCI')
    st.subheader(":house_with_garden: EBE | Excédent Brut d'Exploitation ")

