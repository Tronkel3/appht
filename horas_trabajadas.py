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

st.title('Realiza tus análisis sobre horas de trabajo')

st.markdown("""
En esta aplicación puedes escoger que tipo de análisis quieres hacer
""")

# Descarga datos
@st.cache
def load_data():
    #df = pd.read_csv("BBDD (final).csv", delimiter=',')
    df = pd.read_excel("BBDD (final).xlsx", sheet_name='BBDD (final)')
    return df
df = load_data()

# Sidebar - Selección de años
st.sidebar.header('Selecciones del usuario')
ano_min = st.sidebar.selectbox('Año de comienzo', list(range(1950,2020)))
ano_max = st.sidebar.selectbox('Año final', list(reversed(range(1950,2020))))
ran_anual = list(range(ano_min, ano_max+1))

# Sidebar - Selección variable
dic_var = {'Promedio de las horas anuales trabajadas por personas ocupadas':'avh',
           'Promedio de las horas anuales trabajadas por semana':'avh_week',
           'GDP real del lado del gasto (en millones de US$ de 2011)':'rgdpe',
           'GDP real del lado del gasto per capita':'rgdpe_cap',
           'GDP real del lado de la producción (en millones de US$ de 2011)':'rgdpo',
           'GDP real del lado de la producción per capita':'rgdpo_cap',
           'Población (millones)':'pop',
           'Número de personas contratadas (en millones)':'emp',
           'Índice de capital humano, basado en años de escolaridad y retornos a la educación':'hc',
           'Percentil 50 (mediana): nivel de ingresos o consumo diario':'inc_con',
           'Días de vacaciones y festivos para los trabajadores de la producción a tiempo completo en actividades no agrícolas':'days_vac',
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

# Sidebar - Selección país
sorted_unique_country = sorted(ev.country.unique())
selected_country = st.sidebar.multiselect('Países', sorted_unique_country, [])

# Acote país
ev = ev[ev.country.isin(selected_country)]

# Ploteo gráfico de líneas
ev_lin = ev.pivot(index='year', columns='country', values=dic_var[selected_var])
st.markdown(selected_var)
fig = ev_lin.iplot(asFigure=True, kind='line')
st.plotly_chart(fig)

# Sidebar - Selección año para gráfico de barras
selected_year = st.selectbox('Año para comparar', list(reversed(sorted(ev.year.unique()))))

# Ploteo gráfico de barras
ev_mask = ev['year']==selected_year
ev_comp = ev[ev_mask]
ev_bar = ev_comp.loc[:,['country', dic_var[selected_var]]]
ev_bar = ev_bar.sort_values(by=dic_var[selected_var],ascending=False)
ev_bar = ev_bar.set_index('country')
bar = ev_bar.iplot(asFigure=True, kind='bar', xTitle='Continentes',yTitle=dic_var[selected_var],color='blue')
st.plotly_chart(bar)

# Sidebar - Selección variable para comparar
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
