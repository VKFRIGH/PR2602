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
Primerjaj rast kvalitete življenja med državami.
""")

df_qol, df_analysis = load_data_BK()


all_countries = sorted(df_qol['Country Name'].unique().tolist())

with st.sidebar:
    st.header("Nastavitve")

    selected_countries = st.multiselect(
        "Izberi države:",
        options=all_countries,
        default=['Norway', 'Finland', 'Iceland'],
        max_selections=3,
    )

    
    chart_type = st.radio("Tip grafa:", ["Samo rast", "Rast in trend"])

if not selected_countries:
    st.warning("Izberi vsaj eno državo.")
    st.stop()

fig = go.Figure()
for country in selected_countries:
    country_data = df_qol[df_qol['Country Name'] == country].sort_values('Year')
    country_data = country_data[country_data['Year'] >= 2017]
    trace = go.Scatter(x=country_data['Year'], y=country_data['Quality of Life Index'], mode='lines+markers', name=country)
    fig.add_trace(trace)
    if chart_type == "Rast in trend":
        X = country_data['Year'].values
        y = country_data['Quality of Life Index'].values
        if len(X) > 3:
            model = LinearRegression()
            model.fit(X.reshape(-1, 1), y)
            fig.add_trace(go.Scatter(x=X, y=model.predict(X.reshape(-1, 1)), mode='lines', name=f"{country} trend", line=dict(dash='dash')))

    
st.plotly_chart(fig, use_container_width=True)




