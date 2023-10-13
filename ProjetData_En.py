#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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
    "<h1 style='text-align: center;'>Data Visualization Project</h1>",
    unsafe_allow_html=True
)


# Mettre mon sommaire sur le coté
with st.sidebar:
    st.header("Sommaire")
    st.markdown("- [Problem Statement](#Problem-Statement)")
    st.markdown("- [Data](#Data)")
    st.markdown("- [Part 1: General Data Presentation](#section-1)")
    st.markdown("- [Part 2: Spatial Distribution](#section-2)")
    st.markdown("- [Part 3: Do Age and Gender Factors Impact Licensees?](#section-3)")
    st.markdown("- [Part 4: Do Major Sporting Events Influence Engagement?](#section-4)")
    st.markdown("- [Conclusion](#Conclusion)")
    
    st.markdown("- [My Linkedin : BENEZECH Camille](www.linkedin.com/in/camille-benezech)")
    st.markdown("- [My Github : BENEZECH Camille](https://github.com/zazzouu/Projet_DATA.git)")
    st.markdown("- [INJEP data](https://injep.fr/donnee/recensement-des-licences-et-clubs-sportifs-2022/)")

# Contenu principal de la page
st.markdown("""
<div style="text-align: justify; text-justify: inter-word;">

What is physical activity, and who engages in it?
Physical activity, encompassing various physical and athletic actions, finds its place in both competitive and recreational settings. It involves coordinated and regular physical efforts aimed at improving physical fitness, developing athletic skills, and promoting health. Beyond the physical aspect, sports embody an invaluable source of well-being, health, and fulfillment. It helps maintain the body's shape, strengthen the mind, and cultivate essential values such as discipline, perseverance, and teamwork. It acts as a catalyst for social relationships, fostering strong connections within passionate communities.

Regarding age distribution, levels of physical activity vary, with children and adolescents often being the most active, while adults maintain a consistent interest. With age, the level of activity may decrease, but more and more elderly people recognize the health benefits of sports. As for gender differences, statistics show that men have historically participated more in competitive sports. However, these disparities are diminishing as more women engage in various sports activities. Female participation ranges from gymnastics to athletics, tennis to football, with cultural and social factors playing an increasingly significant role. Gender equality in sports has become a major goal for many sports organizations and governments worldwide. In summary, sports are much more than just an activity; they are a key to a balanced, healthy, and enriching life for everyone.

</div>
""", unsafe_allow_html=True)



###################################################################################################################################
# Problématique
st.markdown("<a id='Problem-Statement'></a>", unsafe_allow_html=True)
st.header("What are the trends in sports?")

###################################################################################################################################
# Présentation de mes data
st.markdown("<a id='Data'></a>", unsafe_allow_html=True)
st.header("Data")
st.write("To conduct my study, I examined data provided by the National Institute for Youth and Popular Education (INJEP) for the period from 2017 to 2022. Each year, the MEDES conducts a census of licenses and clubs in collaboration with 116 accredited sports federations, in accordance with framework agreements signed between the state and the federations. These files are then analyzed by INJEP to generate tables, one for each year. These tables highlight data such as the number of annual licenses, their distribution by gender, age group, and geographical region for each federation.")





####################################################################################################################################
# Section 1
# Section 1
st.markdown("<a id='section-1'></a>", unsafe_allow_html=True)
st.header("Part 1: General Data Presentation")
st.write("First, we will provide a quick overview of the trends of licensed individuals in various federations and over the years.")

#####
st.write("**1- Analysis of the evolution of the number of licensees over the past 6 years**")


# Grouper les données par année et compter le nombre de licences par année
licenses_par_annee = df.groupby(df['Année']).size().reset_index(name='Nombre de licences')

fig = px.bar(licenses_par_annee, x='Année', y='Nombre de licences',
             labels={'Année': 'Année', 'Nombre de licences': 'Nombre de licences'},
             title='Number of licenses over the years')

st.plotly_chart(fig)

st.write("We can observe that the number of licensees, across all federations, does not vary significantly. Indeed, over the past six years, the average number of licensees has remained at approximately 77,558.33 people per year.")

##### 
st.write("**2- Most Popular Sport Cumulatively Over the Years**")
st.write("We will examine the most practiced sports during these past 6 years.")


fig2 = px.bar(df,  
             x='Fédération',
             y='Licences annuelles',
             color='Fédération', 
             color_continuous_scale='skyblue',  
             title='Most Popular Sports Over the Past 6 Years',
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

st.write("This chart shows the total sum of cumulative licensees over the past six years. It can be observed that the French Football Federation attracted the largest number of athletes during this period, followed by tennis and basketball")

#####

st.write("**3- Most Popular Sport by Year**")
st.write("The most prevalent federations each year")

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
                     title=f'Treemap of Licensees by Federation in {annee}')

    st.plotly_chart(fig3)

update_treemap(annee_dropdown)

st.markdown(
    "Thanks to this interactive Treemap, we have the opportunity to select the year we want to study. "
    "The advantage of this chart is its ability to provide an intuitive understanding, "
    "where federations with the most licensees are represented by the largest boxes, "
    "and a legend is provided for increased accuracy.\n\n"
    "Thus, year by year, we can observe the federation that gathers the most licensees. "
    "From 2017 to 2022, football stands out as the federation with the most licensees.\n\n"
    "These two charts complement each other: the first offers an overview of the past six years, "
    "while the second provides a more detailed perspective, year by year."
)

##################################################################################################################################
# Charger les données géographiques (shapefile) 
shapefile = gpd.read_file('departements-version-simplifiee.geojson')  

# Section 2
st.markdown("<a id='section-2'></a>", unsafe_allow_html=True)
st.header("Part 2: Spatial Distribution")
st.write("We will study the distribution of federations in metropolitan France.")

st.write("**1- Distribution of licensees, all federations combined in France by year**")

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
                        title=f'Choropleth of License Percentages in {year1}',
                        labels={f'Pourcentage des licences_{year1}': f'Pourcentage des Licences {year1}'},
                        color_continuous_scale='Reds',
                        scope='europe'
    )

    st.plotly_chart(fig31, use_container_width=False, width=800, height=600)  #J'ai changé ca !!!!!!!!!!!!!!!!!!!!!!!!

    #Barre déroulante
year_dropdown = st.selectbox('Select a year:', annees)
update_map1(year_dropdown)

st.markdown("Through this map, we can examine the coloring of the departments, ranging from darker shades for departments with the highest percentage of licensees to lighter hues for those with lower percentages.")
st.markdown("We can observe that from 2017 to 2022, federations with the most licensees are primarily distributed in departments that host major French cities. For example, the Nord department with Lille, Gironde with Bordeaux, or Rhône with Lyon.")
st.markdown("It is also interesting to note that the Nord department leads in terms of the number of licensees in France, although it represents only about 4% of the total French licensee population. The reasons for this concentration are complex and could be related to factors such as the presence of large student cities attracting dynamic youth interested in sports. However, defining a single cause for this distribution without a more in-depth analysis is challenging.")

#####
st.write("**2- Distribution of Licensees by Federation**")


def update_map2(year1, federation):
    
    somme_licences_par_code = df.groupby('Numéro département')['Licences annuelles'].sum().reset_index()

    somme_licences_par_code = somme_licences_par_code.rename(columns={'Licences annuelles': f'Total des licences annuelles_{year1}'})
    
    somme_licences_france = somme_licences_par_code[f'Total des licences annuelles_{year1}'].sum()

    shapefile_temp = shapefile.merge(somme_licences_par_code, left_on='code', right_on='Numéro département', how='left')

    shapefile_temp[f'Pourcentage des licences_{year1}'] = (shapefile_temp[f'Total des licences annuelles_{year1}'] / somme_licences_france) * 100

    fig32 = px.choropleth(shapefile_temp, geojson=shapefile_temp.geometry, locations=shapefile_temp.index,
                        color=f'Pourcentage des licences_{year1}',
                        hover_name='nom',
                        title=f'Choropleth of License Percentages in {year1} - {federation}',
                        labels={f'Pourcentage des licences_{year1}': f'Pourcentage des Licences {year1}'},
                        color_continuous_scale='Reds',
                        scope='europe')

    st.plotly_chart(fig32)


# Barre déroulante des fédérations
federation_dropdown = st.selectbox('Select a federation:', federations_a_conserver)

update_map2(year_dropdown, federation_dropdown)

st.write("On this map, we can see that the distribution of licensees by federation follows the same pattern as the previous map. The Nord department still has the highest percentage of people in football, basketball, or handball federations.")

##################################################################################################################################
# Section 3
st.markdown("<a id='section-3'></a>", unsafe_allow_html=True)
st.header("Part 3: Do Age and Gender Factors Impact Licensees?")
st.write("We will study the distribution of gender and age in various sports federations.")

st.write("**1- Distribution of Licensees by Federation and Gender (M/F)**")

def plot_graph(year):
    filtered_data = df[df['Année'] == year]
    
    result = filtered_data.groupby(['Fédération', 'Sexe'])['Licences annuelles'].sum().reset_index()

    # Classez les fédérations par ordre décroissant du nombre de licenciés
    result = result.sort_values(by='Licences annuelles', ascending=True)

    fig4 = px.bar(result, x='Sexe', y='Licences annuelles', color='Fédération',
                 color_discrete_sequence=px.colors.qualitative.Set1,
                 labels={'Licences annuelles': 'Nombre de Licenciés'},
                 title=f'Number of Licensees by Federation and Gender in {year}',
                 hover_name='Fédération',
                 hover_data={'Licences annuelles': ':.2f%'},
                 text='Licences annuelles')

    # Ajoutez des pourcentages sur les barres
    fig4.update_traces(texttemplate='%{text}', textposition='outside')

    fig4.update_xaxes(title_text='Sexe')
    fig4.update_yaxes(title_text='Nombre de Licenciés')

    st.plotly_chart(fig4)

years = df['Année'].unique()

year_selector = st.selectbox('Select year:', years, key="year_selector1")

plot_graph(year_selector)

st.write("This chart allows us to see the distribution of men and women by federation and year. Over the years, we observe that in the majority of sports, men are the predominant participants. Only gymnastics is predominantly practiced by girls.")

#####

st.write("**2- Distribution of Licensees by Federation, Gender (M/F), and Age Group (Large Age Group)**")

def update_graph(year):
    filtered_df = df[df['Année'] == year]
    result = filtered_df.groupby(['Fédération', 'Sexe', 'GrandeTrancheAge'])['Licences annuelles'].sum().reset_index()
    result = result.sort_values(by='Licences annuelles', ascending=False)

    fig5 = px.bar(result, x='GrandeTrancheAge', y='Licences annuelles', color='Fédération',
                 color_discrete_sequence=px.colors.qualitative.Set1,
                 labels={'Licences annuelles': 'Nombre de Licenciés'},
                 title=f'Number of Licensees by Federation, Gender, and Large Age Group {year}',
                 hover_name='Fédération',
                 hover_data={'Licences annuelles': ':.2f%'},
                 text='Licences annuelles',
                 facet_col='Sexe')
    
    fig5.update_traces(texttemplate='%{text}', textposition='outside')
    fig5.update_xaxes(title_text='GrandeTrancheAge')
    fig5.update_yaxes(title_text='Nombre de Licenciés')
    
    st.plotly_chart(fig5)
    
update_graph(year_selector)

st.write("This chart allows us to see the distribution of age groups (Large Age Group) and gender (male/female) by federation and year. Once again, over the years, we observe that the majority of sports are practiced by men. Only gymnastics is predominantly practiced by girls. However, we can view our study based on the age group.")
st.write("If we take the example of gymnastics, we can see that the largest age group representing both men and women is in the children's age group, where there are the most licensees.")
st.write("A phenomenon is observed in all sports for men: there is strong engagement in the children's age group, followed by a decrease in the 'Youth' group, and then a return in the 'Adult' group.")
st.write("The same phenomenon is observed in women for all years (except for rugby, where the percentage of female licensees is highest in the 'Adult' group).")
st.write("An interesting avenue for further study would be to investigate the reasons for this disengagement among 14-20-year-olds.")

#####

st.write("**3- Distribution of Licensees by Federation and Age Group (Age Group)**")


def generate_pie_chart(federation):
    data = df[df['Fédération'] == federation]
    age_counts = data['TrancheAge'].value_counts()
    
    fig = px.pie(age_counts, names=age_counts.index, values=age_counts, title=f'Distribution of the {federation} Federation by Large Age Group')
    st.plotly_chart(fig)

federation_dropdown = st.selectbox('Fédération:', df['Fédération'].unique())

generate_pie_chart(federation_dropdown)

st.write("The legend arranges values in descending order of the percentage of female licensees.")
st.write("With this pie chart, we provide a more precise reading of the age at which sports are practiced.")
st.write("For basketball, it can be seen that over all the years combined, the 10 to 14 age group practices basketball the most.")
st.write("For football, the age groups from 5 to 14 practice the most.")
st.write("For gymnastics, it's the 5-9 age group, for rugby and handball, it's the 10-14 age group, but the 5-9 age group is the third most practiced.")
st.write("In contrast, for tennis, it's the 80-99 age group that practices tennis the most within a federation.")
st.write("In summary, we can observe that sports are predominantly practiced by young children and very young individuals, except for tennis where the first age group to practice is the oldest, but the second position is held by children.")

##################################################################################################################################
# Section 4
st.markdown("<a id='section-4'></a>", unsafe_allow_html=True)
st.header("Part 4: Do Major Sporting Events Influence Engagement?")
st.write("In this chapter, we will focus on the influence of major sporting events on sports engagement.")
st.write("I am looking to determine, through various World Cups, whether they have an impact on the number of licensees in federations.")

st.write("The following graphs represent the total number of licensees in the relevant federations, as well as the number of women and men.")

st.write("**1- FIFA World Cup**")


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

st.write("In general, we can see that the number of licensees in the football federation increased following the FIFA Men's World Cup (in green).")
st.write("For both men and women, the same phenomenon is observed. After the FIFA Men's World Cup, the number of male licensees increases, and the same goes for women after the FIFA Women's World Cup in 2019 (yellow bar).")

#####
st.write("**2- Rugby World Cup**")

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

st.write("Here, we observe the opposite phenomenon to the FIFA World Cup. There is an increase in the number of licensees before the year of the Rugby World Cup (2018 and 2022).")
st.write("We can therefore say that there is no correlation between the Rugby World Cup and the number of licenses.")
st.write("However, we can see that the number of female licensees is on the rise.")

#####
st.write("**3- Handball World Cup**")

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

st.write("For handball, we observe an absence of a connection between the World Cup events and the number of licensees in the federations.")

st.write("Through these graphs, we cannot affirm or confirm that sports events such as the World Cups have an influence on the number of licensees in sports federations.")

##################################################################################################################################
# Conclusion
st.markdown("<a id='Conclusion'></a>", unsafe_allow_html=True)
st.header("Conclusion")
st.write("Through the various graphs we have studied, we can see that the number of licensed individuals does not vary significantly from year to year.")
st.write("We have also observed that football is the most popular sport in France over the past 6 years.")
st.write("However, even though it is the most popular sport in France and among men, gymnastics is the most popular among women.")
st.write("We have also seen that sports are predominantly practiced by children, who represent a large majority in the federations.")
st.write("Federations are most prevalent in departments containing major cities and therefore a high concentration of people.")
st.write("Finally, we have not been able to affirm that sports events are a factor favoring an increase in the number of licensees in the federations.")

#####################################################################################################################################

