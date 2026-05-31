import streamlit as st
import pandas as pd
import plotly.express as px
from utils import cluster_growth, get_growth_by_period, load_time_series_data

st.set_page_config(page_title="Trendi rasti in padca", layout="wide")
st.title("Trendi rasti in padca kakovosti življenja")

st.markdown(
    """
    Analiza temelji na stabilnem obdobju 2017–2025, saj so podatki iz zgodnjih let pogosto manj primerljivi.
    Grafi vključujejo neto rast, kvantilno barvno kodiranje in gručne trende.
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
    st.error('Ni dovolj podatkov za stabilno obdobje 2017–2025. Preverite razpoložljive podatke.')
    st.stop()

if df_growth.empty:
    st.warning('Za obdobje ni bilo mogoče izračunati neto rasti.')
    st.stop()

if len(df_growth) < 3:
    st.warning('Premalo držav z zadostnimi podatki za gručenje.')
    st.stop()

low_threshold = df_growth['Net_Growth'].quantile(0.25)
high_threshold = df_growth['Net_Growth'].quantile(0.75)

def growth_category(value):
    if value >= high_threshold:
        return 'Visoka rast'
    if value <= low_threshold:
        return 'Stagnacija / padec'
    return 'Stabilna rast'

df_growth['Growth_Category'] = df_growth['Net_Growth'].apply(growth_category)

df_growth = cluster_growth(df_growth)
cluster_means = df_growth.groupby('Cluster')['Net_Growth'].mean().sort_values()
category_labels = {
    cluster_means.index[0]: 'Stagnacija / padec',
    cluster_means.index[1]: 'Stabilna rast',
    cluster_means.index[2]: 'Visoka rast',
}
df_growth['Category'] = df_growth['Cluster'].map(category_labels)

colors = {'Visoka rast': '#2ecc71', 'Stabilna rast': '#3498db', 'Stagnacija / padec': '#e74c3c'}


st.subheader(f'Neto rast kakovosti življenja ({start_year}–{end_year})')

fig_quartiles = px.bar(
    df_growth.reset_index(),
    x='Net_Growth',
    y='Country',
    orientation='h',
    color='Category',
    color_discrete_map=colors,
    labels={'Net_Growth': 'Neto rast', 'Country': 'Država', 'Category': 'Skupina'},
    text='Net_Growth',
)
fig_quartiles.update_layout(
    yaxis={'categoryorder': 'total ascending'},
    title='Neto rast kakovosti življenja po državah',
    height=650,
)
fig_quartiles.update_traces(texttemplate='%{text:.1f}', textposition='outside')
st.plotly_chart(fig_quartiles, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('**Top 10 držav z največjo rastjo**')
    top_rise = df_growth.sort_values('Net_Growth', ascending=False).head(10).reset_index()
    fig_rise = px.bar(
        top_rise,
        x='Net_Growth',
        y='Country',
        orientation='h',
        color='Category',
        color_discrete_map=colors,
        labels={'Net_Growth': 'Neto rast', 'Country': 'Država'},
    )
    fig_rise.update_layout(yaxis={'categoryorder': 'total ascending'}, height=520)
    st.plotly_chart(fig_rise, use_container_width=True)

with col2:
    st.markdown('**Top 10 držav z najmanjšo rastjo**')
    top_fall = df_growth.sort_values('Net_Growth', ascending=True).head(10).reset_index()
    fig_fall = px.bar(
        top_fall,
        x='Net_Growth',
        y='Country',
        orientation='h',
        color='Category',
        color_discrete_map=colors,
        labels={'Net_Growth': 'Neto rast', 'Country': 'Država'},
    )
    fig_fall.update_layout(yaxis={'categoryorder': 'total ascending'}, height=520)
    st.plotly_chart(fig_fall, use_container_width=True)

st.markdown('---')

category_counts = df_growth['Category'].value_counts().rename_axis('Category').reset_index(name='Count')
st.write('### Število držav v posameznih skupinah rasti')
st.dataframe(category_counts, use_container_width=True)

trend_data = df_stable.merge(df_growth[['Category']], left_on='Country', right_index=True, how='inner')
cluster_avg = trend_data.groupby(['Category', 'Year'])['Quality of Life Index'].mean().reset_index()
fig_cluster = px.line(
    cluster_avg,
    x='Year',
    y='Quality of Life Index',
    color='Category',
    markers=True,
    color_discrete_map=colors,
    labels={'Quality of Life Index': 'QoL indeks'},
)
fig_cluster.update_layout(title='Povprečna pot kakovosti življenja po grupah', height=520)
st.plotly_chart(fig_cluster, use_container_width=True)

highlighted = list(df_growth.sort_values('Net_Growth', ascending=False).head(5).index) + list(df_growth.sort_values('Net_Growth', ascending=True).head(5).index)
highlighted = [country for country in highlighted if country in df['Country'].unique()]
# Allow selecting any country; default to the highlighted top/bottom countries
all_countries = sorted(df['Country'].unique())
selected_countries = st.multiselect('Izberi države za individualni trend', all_countries, default=highlighted)
if selected_countries:
    chart_data = df_stable[df_stable['Country'].isin(selected_countries)]
    fig_lines = px.line(
        chart_data,
        x='Year',
        y='Quality of Life Index',
        color='Country',
        markers=True,
        labels={'Quality of Life Index': 'QoL indeks'},
    )
    fig_lines.update_layout(title='Časovna pot kakovosti življenja za izbrane države', height=520)
    st.plotly_chart(fig_lines, use_container_width=True)

st.markdown(
    '- Podatki za obdobje 2017–2025 so metodološko bolj stabilni.'
    '\n- Barve prikazujejo kvantile rasti: visoka rast, stabilnost in stagnacijo.'
    '\n- K-Means gručenje razvrsti države v tri smiselne skupine glede na neto rast.'
)


# Optional: full dynamics multi-line plot similar to projektB+K (photo 5)
if st.checkbox('Pokaži dinamiko po državah (multi-line overview)'):
    full_start = df['Year'].min()
    full_end = df['Year'].max()
    st.markdown(f'**Dinamika {full_start}–{full_end} po državah**')

    pivot = df.pivot_table(index='Country', columns='Year', values='Quality of Life Index')
    years = [y for y in sorted(pivot.columns) if isinstance(y, int)]
    # restrict to full period
    years = [y for y in years if full_start <= y <= full_end]

    # Get colors per category for countries present in df_growth
    country_category = df_growth['Category'].to_dict()

    fig = px.line()
    for country in pivot.index:
        row = pivot.loc[country]
        vals = [row[y] if y in row.index else None for y in years]
        cat = country_category.get(country, 'Stabilna rast')
        line_color = colors.get(cat, '#777')
        fig.add_scatter(x=years, y=vals, mode='lines+markers', name=country, line=dict(color=line_color, width=1.5), marker=dict(size=4), hoverinfo='name+y')

    # Option to label a few countries (highest final value per cluster)
    label_choice = st.multiselect('Označi države na koncu (izberi do 8)', options=sorted(pivot.index), max_selections=8)
    if label_choice:
        for country in label_choice:
            try:
                last_val = pivot.loc[country, years[-1]]
                fig.add_annotation(x=years[-1], y=last_val, text=country, showarrow=False, xanchor='left')
            except Exception:
                pass

    fig.update_layout(height=700, showlegend=True, legend=dict(traceorder='reversed', itemclick='toggleothers'))
    st.plotly_chart(fig, use_container_width=True)
