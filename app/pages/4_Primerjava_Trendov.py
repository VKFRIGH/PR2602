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
- Po želji vključi **trendne črte** in **intervale zaupanja**, ki prikazujejo splošno smer razvoja skozi opazovano obdobje.
- Na zemljevidu spodaj so države razvrščene glede na rast kakovosti življenja:
  - 🟢 **Visoka rast**
  - 🔵 **Zmerna rast**
  - 🔴 **Stagnacija**

Analiza omogoča hitro prepoznavanje držav z najhitrejšim izboljšanjem kakovosti življenja ter primerjavo dolgoročnih trendov med posameznimi državami.
""")

df_qol, df_growth = load_data_BK()


all_countries = sorted(df_qol['Country Name'].unique().tolist())

with st.sidebar:
    st.header("Nastavitve")

    trend_crte = st.toggle("Prikaži trendne črte in napoved", value=True)

    if trend_crte:
        predict = st.slider(f"Napoved do leta",2026,2030,2026)
        show_ci = st.toggle("Prikaži interval zaupanja napovedi", value=True)
    else:
        predict = None
        show_ci = False

    
    selected_countries = st.multiselect(
        "Izberi države:",
        options=all_countries,
        default=['Norway', 'Finland', 'Iceland'],
        max_selections=None if trend_crte else 3,
    )

if selected_countries:
    fig = go.Figure()
    palette = px.colors.qualitative.Plotly
    for idx, country in enumerate(selected_countries):
        country_data = df_qol[df_qol['Country Name'] == country].sort_values('Year')
        country_data = country_data[country_data['Year'] >= 2017]
        actual_years = country_data['Year'].values
        if predict:
            years = np.array(range(actual_years.min(), predict + 1))
        else:
            years = actual_years
        color = palette[idx % len(palette)]

        trace = go.Scatter(
            x=actual_years,
            y=country_data['Quality of Life Index'],
            mode='lines+markers',
            name=country,
            line=dict(color=color),
            marker=dict(color=color),
        )
        fig.add_trace(trace)

        if trend_crte:
            X = country_data['Year'].values
            y = country_data['Quality of Life Index'].values

            if len(X) > 3:
                model = LinearRegression()
                model.fit(X.reshape(-1, 1), y)

                y_predicted = model.predict(years.reshape(-1, 1))
                residuals = y - model.predict(X.reshape(-1, 1))
                n = len(X)
                mean_x = np.mean(X)
                s_xx = np.sum((X - mean_x) ** 2)

                if n > 2 and s_xx > 0:
                    sigma = np.sqrt(np.sum(residuals ** 2) / (n - 2))
                    se = sigma * np.sqrt(1 / n + (years - mean_x) ** 2 / s_xx)
                    ci = 1.96 * se
                    upper = y_predicted + ci
                    lower = y_predicted - ci

                    if show_ci:
                        last_actual_year = actual_years[-1]
                        future_mask = years >= last_actual_year
                        future_years = years[future_mask]
                        future_upper = upper[future_mask]
                        future_lower = lower[future_mask]

                        distance_from_last = future_years - last_actual_year
                        expansion_factor = 1 + 0.25 * distance_from_last
                        
                        adjusted_upper = y_predicted[future_mask] + ci[future_mask] * expansion_factor
                        adjusted_lower = y_predicted[future_mask] - ci[future_mask] * expansion_factor

                        if len(future_years) > 0:
                            fig.add_trace(
                                go.Scatter(
                                    x=future_years,
                                    y=adjusted_upper,
                                    mode='lines',
                                    line=dict(width=0, color=color),
                                    showlegend=False,
                                    hoverinfo='skip',
                                )
                            )
                            fig.add_trace(
                                go.Scatter(
                                    x=future_years,
                                    y=adjusted_lower,
                                    mode='lines',
                                    fill='tonexty',
                                    fillcolor=f'rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.2)',
                                    line=dict(width=0, color=color),
                                    name=f"{country} 95% interval",
                                    hoverinfo='skip',
                                    showlegend=True,
                                )
                            )

                fig.add_trace(
                    go.Scatter(
                        x=years,
                        y=y_predicted,
                        mode='lines',
                        name=f"{country} trend",
                        line=dict(dash='dash', color=color),
                    )
                )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Izberi vsaj eno državo.")

