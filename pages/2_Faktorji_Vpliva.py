import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from utils import cluster_growth, get_growth_by_period, load_time_series_data, standardize_features

st.set_page_config(page_title="Faktorji vpliva", layout="wide")
st.title("Faktorji, ki vplivajo na kakovost življenja")

st.markdown(
    """
    Ta stran raziskuje, kateri dejavniki so najmočneje povezani z neto rastjo kakovosti življenja
    v stabilnem obdobju 2017–2025. Primerjamo korelacije, regresijske uteži in strukturne razlike med skupinami.
    """
)

@st.cache_data
def load_data():
    return load_time_series_data(chunksize=10000)


df = load_data()
available_years = sorted(df['Year'].unique())
start_year = 2017 if 2017 in available_years else available_years[0]
end_year = 2025 if 2025 in available_years else available_years[-1]
df_stable = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)].copy()

try:
    df_growth = get_growth_by_period(df_stable, start_year, end_year)
except ValueError:
    st.warning('Za izbrano obdobje ni dovolj podatkov. Preverite razpoložljive leto.')
    st.stop()

if df_growth.empty:
    st.warning('Ni dovolj podatkov za analizo faktorjev.')
    st.stop()

if len(df_growth) < 3:
    st.warning('Premalo držav z zadostnimi podatki za gručenje.')
    st.stop()

factors = [
    'Purchasing Power Index',
    'Safety Index',
    'Health Care Index',
    'Cost of Living Index',
    'Property Price to Income Ratio',
    'Traffic Commute Time Index',
    'Pollution Index',
]

feature_data = df_stable.groupby('Country')[factors].mean(numeric_only=True)
analysis_df = feature_data.join(df_growth).dropna()

if analysis_df.empty:
    st.warning('Nekateri ključni faktorji manjkajo v podatkih.')
    st.stop()

analysis_df = analysis_df.reset_index().set_index('Country')

df_growth = cluster_growth(df_growth)
cluster_means = df_growth.groupby('Cluster')['Net_Growth'].mean().sort_values()
category_labels = {
    cluster_means.index[2]: 'Visoka rast',
    cluster_means.index[1]: 'Stabilna rast',
    cluster_means.index[0]: 'Stagnacija ali padec',
}

df_growth['Category'] = df_growth['Cluster'].map(category_labels)
analysis_df = analysis_df.join(df_growth['Category']).dropna()

corr = analysis_df[['Net_Growth'] + factors].corr()
correlation_with_growth = corr.loc[factors, 'Net_Growth'].sort_values(ascending=False)

col1, col2 = st.columns(2)
with col1:
    st.subheader('Korelacija faktorjev z neto rastjo')
    fig_corr = px.bar(
        correlation_with_growth.reset_index(),
        x='Net_Growth',
        y='index',
        orientation='h',
        color='Net_Growth',
        color_continuous_scale='RdBu_r',
        labels={'index': 'Faktor', 'Net_Growth': 'Korelacija z neto rastjo'},
    )
    fig_corr.update_layout(
        height=520,
        yaxis={'categoryorder': 'total ascending'},
        margin=dict(l=120, r=20, t=40, b=40),
    )
    st.plotly_chart(fig_corr, use_container_width=True)

with col2:
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
    fig_matrix.update_layout(height=520, margin=dict(l=40, r=40, t=40, b=40))
    st.plotly_chart(fig_matrix, use_container_width=True)

st.markdown('---')

scaled_features = standardize_features(analysis_df, factors).fillna(0)
model = LinearRegression()
model.fit(scaled_features, analysis_df['Net_Growth'].values)
coef_series = pd.Series(model.coef_, index=factors).sort_values()

st.subheader('Standardizirani regresijski koeficienti')
fig_coef = px.bar(
    coef_series.reset_index(),
    x=0,
    y='index',
    orientation='h',
    labels={'index': 'Faktor', 0: 'Standardiziran koeficient'},
    color=0,
    color_continuous_scale='Teal',
)
fig_coef.add_shape(
    type='line', x0=0, x1=0, y0=-0.5, y1=len(factors) - 0.5,
    line=dict(color='black', width=1), xref='x', yref='y'
)
fig_coef.update_layout(height=520, yaxis={'categoryorder': 'total ascending'}, margin=dict(l=120, r=20, t=40, b=40))
st.plotly_chart(fig_coef, use_container_width=True)

selected_factor = st.sidebar.selectbox('Izberi faktor za scatter graf', factors)

st.subheader(f'Relacija med {selected_factor} in neto rastjo')
factor_df = analysis_df.reset_index()
fig_scatter = px.scatter(
    factor_df,
    x=selected_factor,
    y='Net_Growth',
    color='Category',
    color_discrete_map={'Visoka rast': '#2ecc71', 'Stabilna rast': '#3498db', 'Stagnacija ali padec': '#e74c3c'},
    opacity=0.85,
    labels={'Net_Growth': 'Neto rast', selected_factor: selected_factor},
    hover_data=['Country'] if 'Country' in factor_df.columns else None,
)
line_x = np.linspace(factor_df[selected_factor].min(), factor_df[selected_factor].max(), 100)
line_y = np.polyval(np.polyfit(factor_df[selected_factor].fillna(0), factor_df['Net_Growth'], 1), line_x)
fig_scatter.add_traces(px.line(x=line_x, y=line_y, labels={'x': selected_factor, 'y': 'Neto rast'}).data)
fig_scatter.update_traces(marker=dict(size=12, line=dict(width=1, color='black')), selector=dict(mode='markers'))
fig_scatter.update_layout(height=520, margin=dict(l=60, r=20, t=40, b=40))
st.plotly_chart(fig_scatter, use_container_width=True)

category_stats = analysis_df.groupby('Category')[factors].mean().reset_index()
category_melt = category_stats.melt(id_vars='Category', var_name='Faktor', value_name='Povprečje')
fig_cat = px.bar(
    category_melt,
    x='Faktor',
    y='Povprečje',
    color='Category',
    barmode='group',
    color_discrete_map={'Visoka rast': '#2ecc71', 'Stabilna rast': '#3498db', 'Stagnacija ali padec': '#e74c3c'},
)
fig_cat.update_layout(height=620, xaxis_tickangle=-35, margin=dict(l=120, r=20, t=40, b=120))
st.plotly_chart(fig_cat, use_container_width=True)

st.markdown(
    '- Najbolj pozitivno povezana spremenljivka z neto rastjo je običajno kupna moč.'
    '\n- Onesnaženost je jasno negativno povezana z nižjo rastjo kakovosti življenja.'
    '\n- Varnost in zdravstvo ostajata močna pozitivna faktorja v državah z visoko rastjo.'
)
