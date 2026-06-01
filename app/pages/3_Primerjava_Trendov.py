import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils import load_data_BK
from sklearn.linear_model import LinearRegression


st.set_page_config(page_title="Primerjava Trendov", page_icon="📈", layout="wide")

st.title("📈 Primerjava Trendov")
st.markdown("""
Na tej strani lahko primerjaš gibanje **indeksa kakovosti življenja (Quality of Life Index)** med evropskimi državami v obdobju **2017–2026**.

- Izberi eno ali več držav in primerjaj njihove časovne trende.
- Po želji vključi **trendne črte**, ki prikazujejo splošno smer razvoja skozi opazovano obdobje.
- Na zemljevidu spodaj so države razvrščene glede na rast kakovosti življenja:
  - 🟢 **Visoka rast**
  - 🔵 **Zmerna rast**
  - 🔴 **Stagnacija**

Analiza omogoča hitro prepoznavanje držav z najhitrejšim izboljšanjem kakovosti življenja ter primerjavo dolgoročnih trendov med posameznimi državami.
""")

df_qol, df_analysis = load_data_BK()


all_countries = sorted(df_qol['Country Name'].unique().tolist())

with st.sidebar:
    st.header("Nastavitve")

    chart_type = st.toggle("Prikaži trendne črte", value=True)
    
    selected_countries = st.multiselect(
        "Izberi države:",
        options=all_countries,
        default=['Norway', 'Finland', 'Iceland'],
        max_selections=None if chart_type else 3,
    )

if selected_countries:
    fig = go.Figure()
    for country in selected_countries:
        country_data = df_qol[df_qol['Country Name'] == country].sort_values('Year')
        country_data = country_data[country_data['Year'] >= 2017]
        trace = go.Scatter(x=country_data['Year'], y=country_data['Quality of Life Index'], mode='lines+markers', name=country)
        fig.add_trace(trace)
        if chart_type:
            X = country_data['Year'].values
            y = country_data['Quality of Life Index'].values
            if len(X) > 3:
                model = LinearRegression()
                model.fit(X.reshape(-1, 1), y)
                fig.add_trace(go.Scatter(x=X, y=model.predict(X.reshape(-1, 1)), mode='lines', name=f"{country} trend", line=dict(dash='dash')))

        
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Izberi vsaj eno državo.")


fig = px.choropleth(
        df_analysis,
        locations='iso_code',
        locationmode='ISO-3',
        color="Kategorija",
        hover_name='Country Name',
        labels={'Quality of Life Index Growth (%)': 'Rast QoL (%)'},
        title='Trend kvalitete življenja (2017-2026)',
        hover_data={'iso_code': False, 'Country Name': True, 'Kategorija': True, 'Stable Growth':':.2f'},
        scope='europe',
        color_discrete_map={
            'Visoka rast': '#2ecc71',
            'Zmerna rast': '#3498db',
            'Stagnacija': '#e74c3c',
        },
        height=600,

)

st.plotly_chart(fig, use_container_width=True)

