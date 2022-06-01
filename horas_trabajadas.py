# -*- coding: utf-8 -*-
"""
Created on Tue May 31 17:36:40 2022

@author: javil
"""

import streamlit as st
import pandas as pd
import cufflinks as cf
import plotly.express as px

cf.set_config_file(sharing='private',theme='white',offline=True)

st.title('Haz tus propios análisis')

st.markdown("""
Con esta aplicación puedes hacer tus propios análisis, escoge el rango de años, los países y la variable que quieres analizar
""")

# Descarga datos
@st.cache
def load_data():
    df = pd.read_excel("BBDD (final).xlsx", sheet_name='BBDD (final)')
    return df
df = load_data()

# Sidebar - Selección de años
st.sidebar.header('Selecciones del usuario')
ano_min = st.sidebar.selectbox('Año comienzo', list(range(1950,2020)))
ano_max = st.sidebar.selectbox('Año final', list(reversed(range(1950,2020))))
ran_anual = list(range(ano_min, ano_max+1))

# Sidebar - Selección variable
dic_var = {'Horas anuales trabajadas por ocupados':'avh',
           'Horas anuales trabajadas por semana':'avh_week',
           'GDP del lado del gasto (millones)':'rgdpe',
           'GDP del lado del gasto per capita':'rgdpe_cap',
           'GDP del lado de la producción (millones)':'rgdpo',
           'GDP del lado de la producción per capita':'rgdpo_cap',
           'Población (millones)':'pop',
           'Personas contratadas (millones)':'emp',
           'Índice de capital humano':'hc',
           'Nivel de ingresos o consumo diario':'inc_con',
           'Días de vacaciones y festivos':'days_vac',
           'Productividad':'prod',
           'Índice de desarrollo humano':'idh',
           'Posición en el World Happiness Report':'happ',
           'PIB por hora trabajada':'GDP_hour',
           'GDP per capita':'eco',
           'Esperanza de vida':'life_exp',
           'Libertad':'freed',
           'Confianza en el Gobierno':'trust',
           'Generosidad':'gen'}
selected_var = st.sidebar.selectbox('Variables', dic_var.keys())

# Acote años y variable
df_anos = df[df.year.isin(ran_anual)]
ev = df_anos.loc[:,['continent','country','year', dic_var[selected_var]]]
ev.dropna(axis='rows', how='any', inplace=True)

#Sidebar - Autoselección país por continente
st.sidebar.markdown('Puedes elegir todos los países de uno o más continentes')
sorted_unique_cont = sorted(ev.continent.unique())
selected_continent = st.sidebar.multiselect('Continentes', sorted_unique_cont, [])
ev_cont = ev[ev.continent.isin(selected_continent)]

# Sidebar - Selección país
st.sidebar.markdown('O escogerlos uno a uno')
sorted_unique_country = sorted(ev.country.unique())
al_selected_country = sorted(ev_cont.country.unique())
selected_country = st.sidebar.multiselect('Países', sorted_unique_country, al_selected_country)

# Acote país
ev = ev[ev.country.isin(selected_country)]

# Ploteo gráfico de líneas
ev_lin = ev.pivot(index='year', columns='country', values=dic_var[selected_var])
st.subheader('Gráfico de líneas')
fig = ev_lin.iplot(asFigure=True, kind='line', title=selected_var)
st.plotly_chart(fig)

# Selección año para gráfico de barras
st.subheader('Gráfico de barras')
st.markdown('Elige el año en el que quieres comparar los países')
selected_year = st.selectbox('Año para comparar', list(reversed(sorted(ev.year.unique()))))

# Ploteo gráfico de barras
ev_mask = ev['year']==selected_year
ev_comp = ev[ev_mask]
ev_bar = ev_comp.loc[:,['country', dic_var[selected_var]]]
ev_bar = ev_bar.sort_values(by=dic_var[selected_var],ascending=False)
ev_bar = ev_bar.set_index('country')
bar = ev_bar.iplot(asFigure=True, kind='bar', xTitle='Países',yTitle=selected_var,color='blue')
st.plotly_chart(bar)
st.markdown('*Si al añadir un país, este no aparece, se debe a que no hay datos para ese año')

# Selección variable para comparar
st.subheader('Comparación de variables')
st.markdown('Elige la variable con la que quieres comparar la variable seleccionada anteriormente en el año seleccionado')
dic2 = dic_var.copy()
del dic2[selected_var]
var_comp = st.selectbox('Variable para comparar', dic2.keys())

# Ploteo scatter
ev_scat = df_anos.loc[:,['continent','country','year',dic_var[selected_var],dic_var[var_comp]]]
ev_mask_scat = ev_scat['year']==selected_year
ev_scat = ev_scat[ev_mask_scat]
ev_scat = ev_scat[ev_scat.country.isin(selected_country)]
ev_scat.dropna(axis='rows', how='any', inplace=True)
scat = px.scatter(ev_scat,x=dic_var[selected_var],y=dic_var[var_comp],color='continent',hover_name='country')
st.plotly_chart(scat)
st.markdown('*Si al añadir un país, este no aparece, se debe a que no hay datos para ese año')
