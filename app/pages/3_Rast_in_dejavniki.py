import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils import calculate_correlations, load_data_BK

df_qol, df_growth = load_data_BK()

st.set_page_config(page_title="Rast kvalitete življenja in dejavniki", page_icon="📊", layout="wide")
st.title("📊 Rast kvalitete življenja in dejavniki")


tab1, tab3 = st.tabs(["Neto rast", "Faktorji vpliva"])

with tab1:
    st.markdown(
        """
        Ta stran raziskuje, kateri dejavniki so najmočneje povezani z neto rastjo kakovosti življenja
        v stabilnem obdobju 2017-2026. Primerjamo korelacije in strukturne razlike med skupinami.
        """
    )
    tab1_1, tab1_2 = st.tabs(["📊 Bar chart", "🗺️ Zemljevid"])

    with tab1_1:
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                y=df_growth['Country Name'], 
                x=df_growth['Stable Growth'], 
                name='Rast QoL (%)',
                orientation='h',
                marker_color=df_growth['Kategorija'].map({
                    'Visoka rast': '#2ecc71',
                    'Zmerna rast': '#3498db',
                    'Stagnacija': '#e74c3c',
                }),
                customdata=df_growth[['Kategorija']],
                text=df_growth['Stable Growth'].apply(lambda x: f"{x:.2f}"),
                textposition='outside',
                hovertemplate='%{y}<br>Rast QoL: %{x:.2f}%<br>Kategorija: %{customdata[0]}<extra></extra>',
            )
        )
        fig.update_layout(
            title='Rast kvalitete življenja (2017-2026)',
            xaxis_title='Rast QoL (%)',
            yaxis_title='Država',
            yaxis={'categoryorder':'total ascending'},
            height=800,
        )
        st.plotly_chart(fig, use_container_width=True)


    with tab1_2:
        fig = px.choropleth(
                df_growth,
                locations='iso_code',
                locationmode='ISO-3',
                color="Kategorija",
                hover_name='Country Name',
                labels={'Stable Growth': 'Rast QoL (%)', 'Country Name': 'Država'},
                title='Trend kvalitete življenja (2017-2026)',
                hover_data={'iso_code': False, 'Country Name': True, 'Kategorija': True, 'Stable Growth':':.2f'},
                scope='europe',
                color_discrete_map={
                    'Visoka rast': '#2ecc71',
                    'Zmerna rast': '#3498db',
                    'Stagnacija': '#e74c3c',
                },
                custom_data=['Stable Growth'],
                height=600,

        )
        fig.update_traces(hovertemplate='<b>%{hovertext}</b><br>Kategorija: %{z}<br>Rast QoL: %{customdata[0]:.2f}%<extra></extra>')

        st.plotly_chart(fig, use_container_width=True)

with tab3:
    correlation_with_growth, corr, analysis_df = calculate_correlations(df_qol, df_growth)

    tab_corr1, tab_corr2 = st.tabs(['Urejena korelacija', 'Korelacijska matrika'])

    with tab_corr1:
        st.subheader('Korelacija faktorjev z neto rastjo')
        fig_corr = px.bar(
            correlation_with_growth.reset_index(),
            x='Stable Growth',
            y='index',
            orientation='h',
            color='Stable Growth',
            color_continuous_scale='RdBu_r',
            labels={'index': 'Faktor', 'Stable Growth': 'Korelacija z neto rastjo'},
        )
        fig_corr.update_layout(
            height=520,
            yaxis={'categoryorder': 'total ascending'},
            margin=dict(l=120, r=20, t=40, b=40),
        )
        st.plotly_chart(fig_corr, use_container_width=True)

    with tab_corr2:
        st.subheader('Korelacijska matrika')
        fig_matrix = px.imshow(
            corr,
            text_auto='.2f',
            aspect='auto',
            color_continuous_scale='RdBu_r',
            zmin=-1,
            zmax=1,
            labels={'x': 'Spremenljivka', 'y': 'Spremenljivka'},
        )
        fig_matrix.update_layout(
            height=520,
            margin=dict(l=40, r=40, t=40, b=40),
            xaxis=dict(tickangle=-45),
            yaxis=dict(tickangle=-45),
        )
        st.plotly_chart(fig_matrix, use_container_width=True)

    factors = [
    'Purchasing Power Index',
    'Safety Index',
    'Health Care Index',
    'Cost of Living Index',
    'Property Price to Income Ratio',
    'Traffic Commute Time Index',
    'Pollution Index',
    ]
    
    selected_factor = st.selectbox('Izberi faktor za scatter graf', factors)

    st.subheader(f'Relacija med {selected_factor} in neto rastjo')

    factor_df = analysis_df.reset_index()
    valid = factor_df[[selected_factor, 'Stable Growth', 'Country Name', 'Kategorija']].dropna()
    fig_scatter = px.scatter(
        valid,
        x=selected_factor,
        y='Stable Growth',
        color='Kategorija',
        color_discrete_map={'Visoka rast': '#2ecc71', 'Zmerna rast': '#3498db', 'Stagnacija': '#e74c3c'},
        opacity=0.85,
        labels={'Stable Growth': 'Neto rast', selected_factor: selected_factor},
        custom_data=['Country Name'],
    )

    if len(valid) > 1:
        coeff = np.polyfit(valid[selected_factor], valid['Stable Growth'], 1)
        slope, intercept = coeff[0], coeff[1]
        line_x = np.linspace(valid[selected_factor].min(), valid[selected_factor].max(), 100)
        line_y = np.polyval(coeff, line_x)
        fig_scatter.add_trace(
            go.Scatter(
                x=line_x,
                y=line_y,
                mode='lines',
                name='Trend',
                line=dict(color='gray',dash='dash'),
            )
        )
        trend_pred = np.polyval(coeff, valid[selected_factor])
        ss_res = np.sum((valid['Stable Growth'] - trend_pred) ** 2)
        ss_tot = np.sum((valid['Stable Growth'] - valid['Stable Growth'].mean()) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
        fig_scatter.add_annotation(
            x=0.99,
            y=0.05,
            xref='paper',
            yref='paper',
            text=f'y = {slope:.2f}x + {intercept:.2f}<br>R² = {r2:.2f}',
            showarrow=False,
            align='right',
            borderwidth=1,
            opacity=0.85,
        )

    fig_scatter.update_traces(
        selector=dict(mode='markers'),
        marker=dict(size=12, line=dict(width=1, color='black')),
    )
    fig_scatter.update_traces(
        hovertemplate='<b>%{customdata[0]}</b><br>' + selected_factor + ': %{x:.2f}<br>Neto rast: %{y:.2f}%<extra></extra>',
        selector=dict(mode='markers'),
    )
    fig_scatter.update_layout(height=520, margin=dict(l=60, r=20, t=40, b=40))
    st.plotly_chart(fig_scatter, use_container_width=True)

    category_stats = analysis_df.groupby('Kategorija')[factors].mean().reset_index()
    category_melt = category_stats.melt(id_vars='Kategorija', var_name='Faktor', value_name='Povprečje')
    fig_cat = px.bar(
        category_melt,
        x='Faktor',
        y='Povprečje',
        color='Kategorija',
        barmode='group',
        color_discrete_map={'Visoka rast': '#2ecc71', 'Zmerna rast': '#3498db', 'Stagnacija': '#e74c3c'},
    )
    fig_cat.update_layout(height=620, xaxis_tickangle=-35, margin=dict(l=120, r=20, t=40, b=120))
    st.plotly_chart(fig_cat, use_container_width=True)

    st.markdown(
        '- Najbolj pozitivno povezana spremenljivka z neto rastjo je običajno kupna moč.'
        '\n- Onesnaženost je jasno negativno povezana z nižjo rastjo kakovosti življenja.'
        '\n- Varnost in zdravstvo ostajata močna pozitivna faktorja v državah z visoko rastjo.'
    )


        