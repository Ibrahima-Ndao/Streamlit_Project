import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings 
warnings.filterwarnings('ignore')



st.set_page_config(page_title='Dashboard', page_icon=':bar_chart:', layout='wide')

st.title(':bar_chart: Dashboard sur les ventes')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Utiliser un chemin relatif
data_directory = os.path.join(os.getcwd(), 'donnees_ventes_etudiants.csv')
df = pd.read_csv(data_directory)

col1, col2 = st.columns((2))

df['order_date'] = pd.to_datetime(df['order_date'])




#getting min and max
start_date = pd.to_datetime(df['order_date']).min()
end_date = pd.to_datetime(df['order_date']).max()

with col1:
    date1 = pd.to_datetime(st.date_input('Start Date', start_date))
    
with col2:
    date2 = pd.to_datetime(st.date_input('End Date', end_date))
    
df = df[(df['order_date']>=date1) & (df['order_date']<=date2)].copy()

# Prétraitement des données
# Remplacer les noms d'état abrégés par des noms complets
state_map = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
    "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
    "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
    "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
    "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
    "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
    "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
    "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming"
}
df['State Complet'] = df['State'].map(state_map)
    


st.sidebar.header('Choisi ton filter :')

#create for Region
region = st.sidebar.multiselect('Région', sorted(df['Region'].unique()))
if not region:
    df2 = df.copy()
else:
    df2 = df[df['Region'].isin(region)]

#Create for state
state = st.sidebar.multiselect('État', df2["State Complet"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["State Complet"].isin(state)]
    
#Create for Country
Country = st.sidebar.multiselect('pays', df2["Country"].unique())
if not Country:
    df0 = df3.copy()
else:
    df0 = df3[df3["Country"].isin(Country)]
    
#Create for city
city = st.sidebar.multiselect('ville', sorted(df0['City'].unique()))
if not city:
    df5 = df0.copy()
else:
    df5 = df0[df0['City'].isin(city)]
    
#Create for Status
status = st.sidebar.multiselect('Status', sorted(df5['status'].unique()))
if not status:
    df4 = df5.copy()
else:
    df4 = df5[df['status'].isin(status)]

# 3. KPI : Nombre total de vente, nombre distincts de clients, nombre total de commandes
line1, line2, line3 = st.columns((3))
with line1:
    st.metric("Nombre total de vente", int(df4["total"].sum()))
with line2:
    st.metric("Nombre distincts de clients", df4["cust_id"].nunique())
with line3:
    st.metric("Nombre total de commandes", df4["order_id"].nunique())
    
    


# 8. Carte pour le nombre total de ventes par état (Bonus)
# Créer des colonnes pour la latitude et la longitude
# Remplir ces colonnes en fonction du State Complet en utilisant des données de latitude et de longitude

df4['latitude'] = df4['State Complet'].map({
    'Alabama': 32.806671, 'Alaska': 61.370716, 'Arizona': 33.729759, 'Arkansas': 34.969704, 
    'California': 36.116203, 'Colorado': 39.059811, 'Connecticut': 41.597782, 'Delaware': 39.318523, 
    'Florida': 27.766279, 'Georgia': 33.040619, 'Hawaii': 21.094318, 'Idaho': 44.240459, 
    'Illinois': 40.349457, 'Indiana': 39.849426, 'Iowa': 42.011539, 'Kansas': 38.526600, 
    'Kentucky': 37.668140, 'Louisiana': 31.169546, 'Maine': 44.693947, 'Maryland': 39.063946, 
    'Massachusetts': 42.230171, 'Michigan': 43.326618, 'Minnesota': 45.694454, 'Mississippi': 32.741646, 
    'Missouri': 38.456085, 'Montana': 46.921925, 'Nebraska': 41.125370, 'Nevada': 38.313515, 
    'New Hampshire': 43.452492, 'New Jersey': 40.298904, 'New Mexico': 34.840515, 'New York': 42.165726, 
    'North Carolina': 35.630066, 'North Dakota': 47.528912, 'Ohio': 40.388783, 'Oklahoma': 35.565342, 
    'Oregon': 44.572021, 'Pennsylvania': 40.590752, 'Rhode Island': 41.680893, 'South Carolina': 33.856892, 
    'South Dakota': 44.299782, 'Tennessee': 35.747845, 'Texas': 31.054487, 'Utah': 40.150032, 
    'Vermont': 44.045876, 'Virginia': 37.769337, 'Washington': 47.400902, 'West Virginia': 38.491226, 
    'Wisconsin': 44.268543, 'Wyoming': 42.755966
})

df4['longitude'] = df4['State Complet'].map({
    'Alabama': -86.791130, 'Alaska': -152.404419, 'Arizona': -111.431221, 'Arkansas': -92.373123, 
    'California': -119.681564, 'Colorado': -105.311104, 'Connecticut': -72.755371, 'Delaware': -75.507141, 
    'Florida': -81.686783, 'Georgia': -83.643074, 'Hawaii': -157.498337, 'Idaho': -114.478828, 
    'Illinois': -88.986137, 'Indiana': -86.258278, 'Iowa': -93.210526, 'Kansas': -96.726486, 
    'Kentucky': -84.670067, 'Louisiana': -91.867805, 'Maine': -69.381927, 'Maryland': -76.802101, 
    'Massachusetts': -71.530106, 'Michigan': -84.536095, 'Minnesota': -93.900192, 'Mississippi': -89.678696, 
    'Missouri': -92.288368, 'Montana': -110.454353, 'Nebraska': -98.268082, 'Nevada': -117.055374, 
    'New Hampshire': -71.563896, 'New Jersey': -74.521011, 'New Mexico': -106.248482, 'New York': -74.948051, 
    'North Carolina': -79.806419, 'North Dakota': -99.784012, 'Ohio': -82.764915, 'Oklahoma': -96.928917, 
    'Oregon': -122.070938, 'Pennsylvania': -77.209755, 'Rhode Island': -71.511780, 'South Carolina': -80.945007, 
    'South Dakota': -99.438828, 'Tennessee': -86.692345, 'Texas': -97.563461, 'Utah': -111.862434, 
    'Vermont': -72.710686, 'Virginia': -78.169968, 'Washington': -121.490494, 'West Virginia': -80.954456, 
    'Wisconsin': -89.616508, 'Wyoming': -107.302490
})


fig_map = px.scatter_mapbox(df4, lat="latitude", lon="longitude", size="total", color="total",
                            title="Répartition des vente par état", mapbox_style="carto-positron", zoom=3)
st.plotly_chart(fig_map, use_container_width=True)



part1, part2 = st.columns((2))

category_df = df4.groupby(by=['category'], as_index=False)['total'].sum()

with part1:
    st.subheader('Répartition des ventes par catégorie')
    fig=px.bar(category_df,
               x='category',
               y='total',
               text=['${:,.2f}'.format(x) for x in category_df['total']],
               template='seaborn',
               labels={'Category': 'Categorie'}
               )
    st.plotly_chart(fig, use_container_width=False, height=200)

with part2:
    st.subheader('Répartition des ventes par région')
    fig=px.pie(df4,
               values='total',
               names='Region',
               hole=0.4
               )
    fig.update_traces(text=df4['Region'], textposition='outside')
    st.plotly_chart(fig, use_container_width=False)
    
#linechart
try:
    df4['month'] = df4['order_date'].dt.to_period('M')
except Exception as e:
    st.error(f"An error occurred: {e}")
    df4['month'] = pd.to_datetime(df4['order_date']).dt.to_period('M')
st.subheader('Courbe d\'évolution des ventes au fil du temps')
linechart = pd.DataFrame(df4.groupby(df4['month'].dt.strftime('%Y: %b'))['total'].sum()).reset_index()
fig2 = px.line(linechart, x='month', y='total', labels={'Total': 'Amount'}, height=500, width=800, template='gridon')
st.plotly_chart(fig2)

#Treemap
st.subheader('TreeMap Vue hiérarchique des ventes')
fig3 = px.treemap(df4, path=['Region', 'category'],
                 color='category')
fig3.update_layout(width=800, height=650)
st.plotly_chart(fig3, use_container_width=True)


chart1, chart2 = st.columns((2))
with chart1:
    st.subheader('Répartition des ventes par genre')
    fig=px.pie(df4,
               values='total',
               names='Gender')
    fig.update_traces(text=df4['Gender'], textposition='inside')
    st.plotly_chart(fig, use_container_width=False)
    
with chart2:
    # 6. Histogramme de la répartition de l'âge des clients
    fig_hist_age = px.histogram(df4, x="age", nbins=20, title="Répartition de l'âge des clients")
    st.plotly_chart(fig_hist_age, use_container_width=True)
    
    

import plotly.figure_factory as ff
st.subheader('Month wise Category price summary')
with st.expander('Summary_Table'):
    df_sample=df[0:5][['price','value','total','category','Country','City','State','Region']]
    fig=ff.create_table(df_sample, colorscale='Cividis')
    st.plotly_chart(fig, use_container_width=True)
    
x1, x2 = st.columns((2))
status_df = df4.groupby(by=['status'], as_index=False)['total'].sum()
with x1:
    # Créer un graphique de dispersion
    st.subheader('Impact des remises')
    fig4 = px.scatter(df4, 
    x='total', 
    y='discount_amount', 
    color='Discount_Percent',
    title='Impact des Remises sur les Ventes Totales',
    labels={'discount_amount': 'Montant de la Remise', 'total': 'Ventes Totales'},
    hover_name='Discount_Percent',
    trendline='ols')  # Ajoute une ligne de tendance

    # Afficher le graphique
    st.plotly_chart(fig4, use_container_width=True)
    
    
with x2:
    top_clients = df4.groupby("full_name")["total"].sum().nlargest(10).reset_index()
    fig_bar_clients = px.bar(top_clients, x="full_name", y="total", title="TOP 10 des meilleurs clients")
    st.plotly_chart(fig_bar_clients, use_container_width=True)


    # Créer un graphique de dispersion
st.subheader('Analyse des prix :')
fig4 = px.scatter(df4, 
x='total', 
y='price',
size='discount_amount',
title='Visualiser la distribution des price et leur impact sur les ventes.',
labels={'price': 'prix d\'un article', 'total': 'Ventes Totales'},
)  # Ajoute une ligne de tendance

    # Afficher le graphique
st.plotly_chart(fig4, use_container_width=True)
    
    
