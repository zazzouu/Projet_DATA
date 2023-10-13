#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Importe mes données 
import geopandas as gpd
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px 
import ipywidgets as widgets
from IPython.display import display, clear_output
import plotly.graph_objects as go
from ipywidgets import interact


################################################################################################################################################
# Liste des années de mes fichiers CSV
annees = [2017, 2018, 2019, 2020, 2021, 2022]

# Liste des fédérations à garder
federations_a_conserver = [
    'Fédération Française de Football',
    'Fédération Française de Basketball',
    'Fédération Française de Tennis',
    'Fédération Française de Handball',
    'Fédération Française de Gymnastique',
    'Fédération Française de Rugby',
]

# Créez une liste vide pour stocker les DataFrames de chaque année
dfs = []

# Boucle pour traiter chaque année
for annee in annees:
    # Construire le nom du fichier CSV en fonction de l'année
    nom_fichier = f"Lics_{annee}.csv"
    
    # Lire le fichier CSV
    df_temp = pd.read_csv(nom_fichier, sep=";")
    
    # Nettoyer le DataFrame temporaire
    df_temp = df_temp.dropna()
    df_temp = df_temp.drop_duplicates()
    colonnes_a_supprimer = ["Code année N", "Code 2022", "Codes 2016-2022", "Région"]
    df_temp = df_temp.drop(columns=colonnes_a_supprimer)
    df_temp = df_temp[~(df_temp == 'NR - Non réparti').any(axis=1)]
    df_temp['GrandeTrancheAge'] = df_temp['GrandeTrancheAge'].astype(str)
    df_temp['TrancheAge'] = df_temp['TrancheAge'].astype(str)
    df_temp['Numéro département'] = df_temp['Département'].str.extract(r'(\d+)')
    df_temp = df_temp[df_temp['Numéro département'].astype(float).between(1, 95)]
        
    df_temp = df_temp[df_temp['Fédération'].isin(federations_a_conserver)] # Filtrer les lignes en ne conservant que celles avec les fédérations spécifiées
    
    dfs.append(df_temp)

# Mettre toutes mes données dans df
df = pd.concat(dfs, ignore_index=True)

#st.write(df)

##############################################################################################################################################
#ma banière
st.image("Bannière.jpg",  use_column_width=True)

# titre cintré
st.markdown(
    "<h1 style='text-align: center;'>Projet Data Visualisation</h1>",
    unsafe_allow_html=True
)

# Mettre mon sommaire sur le coté
with st.sidebar:
    st.header("Sommaire")
    st.markdown("- [Problématique](#Problématique)")
    st.markdown("- [Data](#Data)")
    st.markdown("- [Part 1](#section-1)")
    st.markdown("- [Part 2](#section-2)")
    st.markdown("- [Part 3](#section-3)")
    st.markdown("- [Part 4](#section-4)")
    st.markdown("- [Conclusion](#Conclusion)")

# Contenu principal de la page
st.markdown("""
<div style="text-align: justify; text-justify: inter-word;">

Qu’est-ce que l’activité sportive et qui l’a pratique ?
L'activité sportive, englobant diverses actions physiques et athlétiques, trouve sa place tant dans le cadre compétitif que récréatif. Elle implique des efforts physiques coordonnés et réguliers visant à améliorer la condition physique, à développer des compétences sportives et à promouvoir la santé. Au-delà de l'aspect physique, le sport incarne une source inestimable de bien-être, de santé et d'épanouissement. Il permet de maintenir le corps en forme, de renforcer l'esprit, et de cultiver des valeurs essentielles telles que la discipline, la persévérance et le travail d'équipe. Il agit comme un catalyseur des relations sociales, favorisant l'établissement de liens solides au sein de communautés passionnées. 
Quant à la répartition par tranche d'âge, les niveaux d'activité sportive varient, les enfants et adolescents étant souvent les plus actifs, tandis que les adultes maintiennent un intérêt constant. Avec l'âge, le niveau d'activité peut diminuer, mais de plus en plus de personnes âgées reconnaissent les avantages du sport pour la santé. Concernant la différence entre les sexes, les statistiques montrent que les hommes ont historiquement participé davantage au sport de manière compétitive. Cependant, ces disparités tendent à s'atténuer, car de plus en plus de femmes s'engagent dans diverses activités sportives. La participation féminine s'étend de la gymnastique à l'athlétisme, du tennis au football, avec des facteurs culturels et sociaux jouant un rôle de plus en plus prépondérant. L'égalité des sexes dans le sport est devenue un objectif majeur pour de nombreuses organisations sportives et gouvernements à travers le monde. En somme, le sport est bien plus qu'une simple activité, il constitue une clé vers une vie équilibrée, saine et enrichissante pour tous.

</div>
""", unsafe_allow_html=True)



###################################################################################################################################
# Problématique
st.markdown("<a id='Problématique'></a>", unsafe_allow_html=True)
st.header("Problématique")
st.write(" Quelles sont les tendances sportives sur les 6 dernières années ?")


###################################################################################################################################
# Présentation de mes data
st.markdown("<a id='Data'></a>", unsafe_allow_html=True)
st.header("Data")
st.write("Pour mener à bien mon étude, j'ai examiné les données fournies par l'Institut National de la Jeunesse et de l'Education Populaire (INJEP) pour la période allant de 2017 à 2022. Chaque année, la MEDES effectue un recensement des licences et des clubs en collaboration avec les 116 fédérations sportives agréées, conformément aux accords-cadres signés entre l'État et les fédérations. Ces fichiers sont ensuite analysés par l'INJEP afin de générer des tableaux, un par année. Ces tableaux mettent en évidence des données telles que le nombre de licences annuelles, leur répartition par sexe, tranche d'âge et région géographique pour chaque fédération.")
st.write(df.columns)
texte = """
Codé pour afficher ce texte dans Streamlit :
- Fédération : Libellé de la fédération
- Année : Année du recensement des licences. L'année N équivaut à la saison N ou N-1/N en fonction des fédérations.
- Sexe : Genre du détenteur de licence, codé 'H' pour les hommes et 'F' pour les femmes
- Age : Âge au 1er janvier de l'année N
- TrancheAge : Tranche d'âge au 1er janvier de l'année N
    1- Enfants (1-13)
    2- Jeunes (14-20)
    3- Adultes (21-55)
    4- Seniors (56-99)
- GrandeTrancheAge : Grande tranche d'âge au 1er janvier de l'année N
    a - de 1 à 4 ans, 
    b - de 5 à 9 ans,	
    c - de 10 à 14 ans, 
    d - de 15 à 19 ans,
    e - de 20 à 24 ans,
    f - de 25 à 29 ans,
    g - de 30 à 34 ans,
    h - de 35 à 39 ans,
    i - de 40 à 44 ans,
    j - de 45 à 49 ans,
    k - de 50 à 54 ans,
    l - de 55 à 59 ans,
    m - de 60 à 64 ans,
    n - de 65 à 69 ans,
    o - de 70 à 74 ans,
    p - de 75 à 79 ans,
    q - de 80 à 99 ans
- Département : Département de résidence du détenteur de licence
- Licences annuelles : Nombre de licences annuelles

Pour cette analyse, nous nous concentrons sur les données quantitatives :
- Année : Année du recensement des licences
- Âge : Âge au 1er janvier de l'année N
- Licences annuelles : Nombre de licences annuelles

et les données qualitatives :
- Fédération : Libellé de la fédération
- Sexe : Genre du détenteur de licence, codé 'H' pour les hommes et 'F' pour les femmes
- TrancheAge : Tranche d'âge au 1er janvier de l'année N
- GrandeTrancheAge : Grande tranche d'âge au 1er janvier de l'année N

Cependant, nous nous concentrons sur six fédérations spécifiques :
- 'Fédération Française de Football',
- 'Fédération Française de Basketball',
- 'Fédération Française de Gymnastique',
- 'Fédération Française de Handball',
- 'Fédération Française de Tennis',
- 'Fédération Française de Rugby'


Pour pouvoir facilité la lecture et le bon fonctionne de mon ordinateur
"""
st.markdown(texte)
####################################################################################################################################

# Section 1
st.markdown("<a id='section-1'></a>", unsafe_allow_html=True)
st.header("Part 1 : Présentation générale des données")
st.write("Dans un premier temps nous allons faire une présentation rapide des tendances des personnes licenciers dans les différentes fédérations et en fonction des années")

#####

st.write("**1- Analyse de l'évolution du nombre de licencier sur les 6 dernières années**")

# Grouper les données par année et compter le nombre de licences par année
licenses_par_annee = df.groupby(df['Année']).size().reset_index(name='Nombre de licences')

fig = px.bar(licenses_par_annee, x='Année', y='Nombre de licences',
             labels={'Année': 'Année', 'Nombre de licences': 'Nombre de licences'},
             title='Nombre de licences en fonction des années')

st.plotly_chart(fig)

st.write("On peut observer que le nombre de licenciés, toutes fédérations confondues, ne varie pas de manière significative. En effet, au cours des six dernières années, la moyenne du nombre de licenciés s'établit à environ 77 558,33 personnes par an.")

##### 
st.write("**2- Qu'elle sport est le plus populaire toute année cumulée**")
st.write("Nous allons voir les sports les plus pratiquer durant c'est 6 dernières années")

fig2 = px.bar(df,  
             x='Fédération',
             y='Licences annuelles',
             color='Fédération', 
             color_continuous_scale='skyblue',  
             title='Sports les plus populaires sur les 6 dernières années',
             labels={'Fédération': 'Fédération', 'Licences annuelles': 'Nombre total de licences'},
             height=600,  
             width=1000) 

# Mettez à jour la disposition du graphique pour un meilleur affichage
fig2.update_layout(
    xaxis_title='',
    yaxis_title='',
    xaxis_showgrid=False,
    yaxis_showgrid=False,
    xaxis_zeroline=False,
    yaxis_zeroline=False,
)

st.plotly_chart(fig2)

st.write("Ce graphique présente la somme totale des licenciés cumulés au cours des six dernières années. On constate que la Fédération Française de Football a attiré le plus grand nombre de sportifs sur cette période, suivie du tennis et du basket.")

###

st.write("**3- Qu'elle sport est le plus populaire par année**")
st.write("Les fédération les plus présente par année")
annee_dropdown = st.selectbox(
    'Année:',
    [str(annee) for annee in annees],
    index=0  # Sélectionnez la première année par défaut
)

# Fonction de mise à jour du treemap en fonction de l'année sélectionnée
def update_treemap(annee):
    st.write("")  # Efface la sortie précédente

    # Créer le treemap
    fig3 = px.treemap(df, 
                     path=['Fédération'],
                     values='Licences annuelles',
                     color='Licences annuelles',
                     color_continuous_scale='blues',
                     title=f'Treemap des licenciés par fédération en {annee}')

    st.plotly_chart(fig3)

update_treemap(annee_dropdown)

st.markdown(
    "Grâce à ce Treemap interactif, nous avons la possibilité de sélectionner l'année que nous souhaitons étudier. "
    "L'avantage de ce graphique réside dans sa capacité à offrir une compréhension intuitive, "
    "où les fédérations comptant le plus de licenciés sont représentées par les cases les plus grandes, "
    "et une légende est fournie pour une précision accrue.\n\n"
    "Ainsi, d'année en année, nous pouvons observer la fédération qui rassemble le plus de licenciés. "
    "De 2017 à 2022, le football se distingue en tant que la fédération qui compte le plus de licenciés.\n\n"
    "Ces deux graphiques sont complémentaires : le premier offre une vue d'ensemble des six dernières années, "
    "tandis que le deuxième fournit une perspective plus détaillée, année par année."
)
##################################################################################################################################
# Charger les données géographiques (shapefile) 
shapefile = gpd.read_file('departements-version-simplifiee.geojson')  

# Section 2
st.markdown("<a id='section-2'></a>", unsafe_allow_html=True)
st.header("Part 2 : Répartition spatiale")
st.write("Nous allons étudier la répartition des fédérations en France métropolitaine")

st.write("**1- Répartition des licenciers, toutes fédérations confondus en France par année**")

def update_map1(year1):
    
    # Sommez le nombre de licences annuelles pour chaque département
    somme_licences_par_code = df.groupby('Numéro département')['Licences annuelles'].sum().reset_index()

    somme_licences_par_code = somme_licences_par_code.rename(columns={'Licences annuelles': f'Total des licences annuelles_{year1}'})
    
    # Somme totale des licences en France pour l'année en cours
    somme_licences_france = somme_licences_par_code[f'Total des licences annuelles_{year1}'].sum()

    # Rassembler les données par département
    shapefile_temp = shapefile.merge(somme_licences_par_code, left_on='code', right_on='Numéro département', how='left')

    shapefile_temp[f'Pourcentage des licences_{year1}'] = (shapefile_temp[f'Total des licences annuelles_{year1}'] / somme_licences_france) * 100

    
    fig31 = px.choropleth(shapefile_temp, geojson=shapefile_temp.geometry, locations=shapefile_temp.index,
                        color=f'Pourcentage des licences_{year1}',
                        hover_name='nom',
                        title=f'Choroplèthe des Pourcentages de Licences en {year1}',
                        labels={f'Pourcentage des licences_{year1}': f'Pourcentage des Licences {year1}'},
                        color_continuous_scale='Reds',
                        scope='europe')

    st.plotly_chart(fig31, use_container_width=False, width=800, height=600)  #J'ai changé ca !!!!!!!!!!!!!!!!!!!!!!!!

    #Barre déroulante
year_dropdown = st.selectbox('Sélectionnez une année:', annees)
update_map1(year_dropdown)

st.markdown("À travers cette carte, on peut examiner la coloration des départements, allant du plus sombre pour les départements comptant le pourcentage le plus élevé de licenciés, aux teintes plus claires pour ceux avec des pourcentages plus bas.")
st.markdown("Nous pouvons noter que de 2017 à 2022, les fédérations qui ont le plus de licenciés sont principalement réparties dans les départements qui abritent de grandes villes françaises. Par exemple, le département du Nord avec Lille, la Gironde avec Bordeaux, ou le Rhône avec Lyon.")
st.markdown("Il est également intéressant de noter que le département du Nord est en tête en termes de nombre de licenciés en France, bien qu'il ne représente qu'environ 4 % de la population totale de licenciés français. Les raisons de cette concentration sont complexes et pourraient être liées à des facteurs tels que la présence de grandes villes étudiantes attirant des jeunes dynamiques et intéressés par la pratique sportive. Cependant, il est difficile de définir une seule cause à cette répartition sans effectuer une analyse plus approfondie.")

#####
st.write("**2- Répartition des licenciers par fédération**")

def update_map2(year1, federation):
    
    somme_licences_par_code = df.groupby('Numéro département')['Licences annuelles'].sum().reset_index()

    somme_licences_par_code = somme_licences_par_code.rename(columns={'Licences annuelles': f'Total des licences annuelles_{year1}'})
    
    somme_licences_france = somme_licences_par_code[f'Total des licences annuelles_{year1}'].sum()

    shapefile_temp = shapefile.merge(somme_licences_par_code, left_on='code', right_on='Numéro département', how='left')

    shapefile_temp[f'Pourcentage des licences_{year1}'] = (shapefile_temp[f'Total des licences annuelles_{year1}'] / somme_licences_france) * 100

    fig32 = px.choropleth(shapefile_temp, geojson=shapefile_temp.geometry, locations=shapefile_temp.index,
                        color=f'Pourcentage des licences_{year1}',
                        hover_name='nom',
                        title=f'Choroplèthe des Pourcentages de Licences en {year1} - {federation}',
                        labels={f'Pourcentage des licences_{year1}': f'Pourcentage des Licences {year1}'},
                        color_continuous_scale='Reds',
                        scope='europe')

    st.plotly_chart(fig32)


# Barre déroulante des fédérations
federation_dropdown = st.selectbox('Sélectionnez une fédération:', federations_a_conserver)

update_map2(year_dropdown, federation_dropdown)

st.write("Sur cette carte, on peut voir que la répartition des licenciés par fédération suit le même schéma que la carte précédente. Le département du Nord compte toujours le plus grand pourcentage de personnes dans les fédérations de football, de basket ou de handball")


##################################################################################################################################
# Section 3
st.markdown("<a id='section-3'></a>", unsafe_allow_html=True)
st.header("Part 3 : Les facteurs age et sexe jouent ils sur les licenciers")
st.write("Nous allons étudier la répartition du sexe et de l'age dans les différentes fédérations sportives")

st.write("**1- Répartition des licenciés par fédération et en fonction du sexe (H/F)**")

def plot_graph(year):
    filtered_data = df[df['Année'] == year]
    
    result = filtered_data.groupby(['Fédération', 'Sexe'])['Licences annuelles'].sum().reset_index()

    # Classez les fédérations par ordre décroissant du nombre de licenciés
    result = result.sort_values(by='Licences annuelles', ascending=True)

    fig4 = px.bar(result, x='Sexe', y='Licences annuelles', color='Fédération',
                 color_discrete_sequence=px.colors.qualitative.Set1,
                 labels={'Licences annuelles': 'Nombre de Licenciés'},
                 title=f'Nombre de Licenciés par Fédération et Sexe en {year}',
                 hover_name='Fédération',
                 hover_data={'Licences annuelles': ':.2f%'},
                 text='Licences annuelles')

    # Ajoutez des pourcentages sur les barres
    fig4.update_traces(texttemplate='%{text}', textposition='outside')

    fig4.update_xaxes(title_text='Sexe')
    fig4.update_yaxes(title_text='Nombre de Licenciés')

    st.plotly_chart(fig4)

years = df['Année'].unique()

year_selector = st.selectbox('Sélectionnez une année:', years, key="year_selector1")

plot_graph(year_selector)

st.write("Ce graphique nous permet de voir la répartion homme/femme en fonction des fédérations et de l'année. Sur l'ensemble des années on observe que dans la majorité des sports sont pratiqués par les hommes. Seul la gymnastique est majoritairement pratiquer par les filles.")

#####

st.write("**2- Répartition des licenciés par fédération et en fonction du sexe (H/F) et de l'age (GrandeTrancheAge)**")

def update_graph(year):
    filtered_df = df[df['Année'] == year]
    result = filtered_df.groupby(['Fédération', 'Sexe', 'GrandeTrancheAge'])['Licences annuelles'].sum().reset_index()
    result = result.sort_values(by='Licences annuelles', ascending=False)

    fig5 = px.bar(result, x='GrandeTrancheAge', y='Licences annuelles', color='Fédération',
                 color_discrete_sequence=px.colors.qualitative.Set1,
                 labels={'Licences annuelles': 'Nombre de Licenciés'},
                 title=f'Nombre de Licenciés par Fédération, Sexe et GrandeTrancheAge - Année {year}',
                 hover_name='Fédération',
                 hover_data={'Licences annuelles': ':.2f%'},
                 text='Licences annuelles',
                 facet_col='Sexe')
    
    fig5.update_traces(texttemplate='%{text}', textposition='outside')
    fig5.update_xaxes(title_text='GrandeTrancheAge')
    fig5.update_yaxes(title_text='Nombre de Licenciés')
    
    st.plotly_chart(fig5)
    
update_graph(year_selector)

st.write("Ce graphique nous permet de voir la répartion des tranches d'age (GrandeTrancheAge) et du genre (homme/femme) en fonction des fédérations et de l'année. En core une fois, sur l'ensemble des années on observe que dans la majorité des sports sont pratiqués par les hommes. Seul la gymnastique est majoritairement pratiquer par les filles. Cependant, on peut afficher notre étude grace au tranche d'age")
st.write("Si l'on prend l'exemple de la gymnastique, on peut voir que la plus grande tranche d'age représenter homme et femme confondu, c'est dans la tranche d'age des enfants où il y a le plus de licenciée.")
st.write("On observe un phénomène dans tous les sports pour les hommes: il y a un fort engagement chez les enfants, puis une diminution au moment de la tranche 'Jeunes' pour revnir au moment de la phase 'Adultes'  ")
st.write("Le meme phénomène est observé chez les femmes pour tous les années (sauf pour le rugby ou le taux de licenciée est au plus haut moment de la phase 'Adulte')")
st.write("Une piste intérressante qui pourrait être étudier, à quoi est du ce phénomène de désengagement chez les 14-20 ans")


#####
st.write("**3- Répartition des licenciés par fédération l'age (TrancheAge)**")

def generate_pie_chart(federation):
    data = df[df['Fédération'] == federation]
    age_counts = data['TrancheAge'].value_counts()
    
    fig = px.pie(age_counts, names=age_counts.index, values=age_counts, title=f'Répartition de la fédération {federation} par grande tranche d\'âge')
    st.plotly_chart(fig)

federation_dropdown = st.selectbox('Fédération:', df['Fédération'].unique())

generate_pie_chart(federation_dropdown)

st.write("la légende classe les valeurs par ordre décroissant de % de licenciée")
st.write("On apporte avec ce camembert une lecture plus précise de l'age à laquelle le sport est pratiquer.")
st.write("On peut voir pour le basket que sur toutes les années confondue, ce sont les jeunes de 10 à 14 ans qui pratique le plus le basket.")
st.write("On peut voir pour le foot se sont les tranches d'age de 5 à 14 qui pratique le plus.")
st.write("Pour la gymnastique se sont les 5-9 ans, pour le rugby et le handball c'est le 10-14 ans mais les 5-9 ans sont la troisième tranche d'age à pratiquer le plus")
st.write("En revanche pour le Tennis ce sont les 80-99 ans qui pratique le plus le tennis au sein d'une fédération")
st.write("En résumer, on peut remarquer que les sports sont en majoritairement pratiquer par les jeunes enfants et les très jeunes, à l'exception du tennis où la première tranche d'age à pratiquer sont les plus vieux mais en deuxième position ca reste les enfants")

##################################################################################################################################
# Section 4
st.markdown("<a id='section-4'></a>", unsafe_allow_html=True)
st.header("Part 4 : Les grands événements sportifs influent-ils sur l'engagement")
st.write("Dans ce chapitre on va s'intéresser à l'influence des grands événements sportif sur l'engagement dans le sport.")
st.write("Je cherche à savoir, au travers des différentes coupe du monde, si elles ont une influence sur le nombre de licencié dans les fédérations.")

st.write("Les graphiques suivant représentent la somme de licencié dans les fédérations concerner ainsi que le nombre de femme et d'homme")

st.write("**1- Coupe du monde de Foot**")

# Prendre que la Fédération Française de Foot
df_fff = df[df['Fédération'] == 'Fédération Française de Football']

total_licences_par_annee_fff = df_fff.groupby('Année')['Licences annuelles'].sum().reset_index()

# Groupez également les données pour les licenciés hommes et femmes
licencies_hommes_fff = df_fff[df_fff['Sexe'] == 'H'].groupby('Année')['Licences annuelles'].sum().reset_index()
licencies_femmes_fff = df_fff[df_fff['Sexe'] == 'F'].groupby('Année')['Licences annuelles'].sum().reset_index()

# Créez le graphique à barres
fig_fff = go.Figure()

# Ajoutez les barres pour le graphique à barres
fig_fff.add_trace(go.Bar(x=total_licences_par_annee_fff['Année'], y=total_licences_par_annee_fff['Licences annuelles'], name='Total'))

# Ajoutez les lignes Scatter
fig_fff.add_trace(go.Scatter(x=licencies_hommes_fff['Année'], y=licencies_hommes_fff['Licences annuelles'], mode='lines+markers', name='Hommes', line=dict(color='blue')))
fig_fff.add_trace(go.Scatter(x=licencies_femmes_fff['Année'], y=licencies_femmes_fff['Licences annuelles'], mode='lines+markers', name='Femmes', line=dict(color='red')))

fig_fff.add_trace(go.Scatter(x=[2018, 2019], y=[90000, 90000], mode='text', text=['Coupe du monde de football (Hommes)', 'Coupe du monde de football (Femmes)'], showlegend=False, textfont=dict(color='green')))

# Mettez en surbrillance l'année 2018 en vert clair (hommes) et l'année 2019 en jaune clair (femmes)
highlight_years_fff = [2018, 2019]

# Mettre la surbrillance pour les années spé
highlight_mask_fff = total_licences_par_annee_fff['Année'].isin(highlight_years_fff)
colors_fff = ['lightgreen' if year == 2018 else 'lightyellow' if year == 2019 else 'lightgrey' for year in total_licences_par_annee_fff['Année']]
fig_fff.update_traces(marker_color=colors_fff)

fig_fff.update_layout(xaxis=dict(tickvals=df_fff['Année'].unique(), ticktext=df_fff['Année'].unique(), tickangle=45),
                     legend_title_text='Légende',
                     height=600)

st.plotly_chart(fig_fff)

st.write("De manière générale, on peut voir que le nombre de licencié dans la fédération de foot a augmenté à la suite de coupe du monde de foot homme (en vert).")
st.write("Chez les hommes et chez les femmes on observe le meme phénomène. Apres la coupe du monde de foot homme, le nombre d'homme augmente et pareil chez les femmes apres la coupe du monde de foot féminine en 2019 (barre jaune)")

#####

st.write("**2- Coupe du monde de rugby**")

df_ffr = df[df['Fédération'] == 'Fédération Française de Rugby']

total_licences_par_annee_ffr = df_ffr.groupby('Année')['Licences annuelles'].sum().reset_index()

licencies_hommes_ffr = df_ffr[df_ffr['Sexe'] == 'H'].groupby('Année')['Licences annuelles'].sum().reset_index()
licencies_femmes_ffr = df_ffr[df_ffr['Sexe'] == 'F'].groupby('Année')['Licences annuelles'].sum().reset_index()

fig_ffr = go.Figure()

fig_ffr.add_trace(go.Bar(x=total_licences_par_annee_ffr['Année'], y=total_licences_par_annee_ffr['Licences annuelles'], name='Total'))

fig_ffr.add_trace(go.Scatter(x=licencies_hommes_ffr['Année'], y=licencies_hommes_ffr['Licences annuelles'], mode='lines+markers', name='Hommes', line=dict(color='blue')))
fig_ffr.add_trace(go.Scatter(x=licencies_femmes_ffr['Année'], y=licencies_femmes_ffr['Licences annuelles'], mode='lines+markers', name='Femmes', line=dict(color='red')))

fig_ffr.add_trace(go.Scatter(x=[2018], y=[90000], mode='text', text=['Coupe du monde de rugby (Hommes)'], showlegend=False, textfont=dict(color='green')))
fig_ffr.add_trace(go.Scatter(x=[2021], y=[90000], mode='text', text=['Coupe du monde de rugby (Femmes)'], showlegend=False, textfont=dict(color='yellow')))

highlight_years_ffr = [2019, 2021]

highlight_mask_ffr = total_licences_par_annee_ffr['Année'].isin(highlight_years_ffr)

colors = ['lightgreen' if year == 2019 else 'lightyellow' if year == 2021 else 'lightgrey' for year in total_licences_par_annee_ffr['Année']]
fig_ffr.update_traces(marker_color=colors)

fig_ffr.update_layout(xaxis=dict(tickvals=df_ffr['Année'].unique(), ticktext=df_ffr['Année'].unique(), tickangle=45),
                     legend_title_text='Légende',
                     height=600)

st.plotly_chart(fig_ffr)

st.write("Ici, on observe le phénomène inverse de la coupe du monde football. On a une augmentation du nombre de licencié avant l'année de la coupe du monde de rugby (2018 et 2022)")
st.write("On peut donc dire qu il n y a pas de corrémation entre la coupe du monde rugby et le nombre de licence")
st.write("En revanche, on peu tvoir que le nombre de licencié chez les femmes est en augmentation")

#####
st.write("**3- Coupe du monde de handball**")

df_ffhb = df[df['Fédération'] == 'Fédération Française de Handball']

total_licences_par_annee_ffhb = df_ffhb.groupby('Année')['Licences annuelles'].sum().reset_index()

licencies_hommes_ffhb = df_ffhb[df_ffhb['Sexe'] == 'H'].groupby('Année')['Licences annuelles'].sum().reset_index()
licencies_femmes_ffhb = df_ffhb[df_ffhb['Sexe'] == 'F'].groupby('Année')['Licences annuelles'].sum().reset_index()

fig_ffhb = go.Figure()

fig_ffhb.add_trace(go.Bar(x=total_licences_par_annee_ffhb['Année'], y=total_licences_par_annee_ffhb['Licences annuelles'], name='Total'))

fig_ffhb.add_trace(go.Scatter(x=licencies_hommes_ffhb['Année'], y=licencies_hommes_ffhb['Licences annuelles'], mode='lines+markers', name='Hommes', line=dict(color='blue')))
fig_ffhb.add_trace(go.Scatter(x=licencies_femmes_ffhb['Année'], y=licencies_femmes_ffhb['Licences annuelles'], mode='lines+markers', name='Femmes', line=dict(color='red')))

fig_ffhb.add_trace(go.Scatter(x=[2018], y=[90000], mode='text', text=['Coupe du monde de handball (Hommes)'], showlegend=False, textfont=dict(color='green')))
fig_ffhb.add_trace(go.Scatter(x=[2021], y=[90000], mode='text', text=['Coupe du monde de handball (Femmes)'], showlegend=False, textfont=dict(color='yellow')))

highlight_years_ffhb = [2019, 2021]

highlight_mask_ffhb = total_licences_par_annee_ffhb['Année'].isin(highlight_years_ffhb)

colors = ['lightgreen' if year == 2019 else 'lightyellow' if year == 2021 else 'lightgrey' for year in total_licences_par_annee_ffhb['Année']]
fig_ffhb.update_traces(marker_color=colors)

fig_ffhb.update_layout(xaxis=dict(tickvals=df_ffhb['Année'].unique(), ticktext=df_ffhb['Année'].unique(), tickangle=45),
                     legend_title_text='Légende',
                     height=600)

st.plotly_chart(fig_ffhb)

st.write("Pour le hanball, on observe un absence de lien entre les coupes du monde et le nombre de licencié dans les fédérations.")


st.write("Au travers de ces graphiques, on ne peut pas affirmer ou confirmer que les évenements sportifs comme les coupes du monde ont une influence sur le nombre licenciés dans les fédérations sportives")

##################################################################################################################################
# Conclusion 
st.markdown("<a id='Conclusion'></a>", unsafe_allow_html=True)
st.header("Conclusion")
st.write("Au travers des différents graphiques que nous avons étudiés, nous pouvons voir que le nombre de personne licencié ne varient pas d'année en année de manière significative.")
st.write("On a pu aussi observé que le foot est le sport le plus populaire en France et ceux sur les 6 dernières années")
st.write("En revanche bien qu'il soit le sport le plus populaire en France et chez les Hommes, c'est la gymnastique qui est le plus populaire chez les femmes.")
st.write("On a pu aussi voir que les sport étaient majoritairement pratiquer par les enfants qui représentaient une grande majoritée dans les fédérations.")
st.write("Et que les fédérations étaient majoritaire dans les départements contenant une grande ville et donc une grande concentration de personne")
st.write("Enfin, nous n'avons pas pu affirmer que les évenements sportifs étaint un facteur favorisant l'augmentation du nombre de licencié dans les fédérations")



#####################################################################################################################################

