import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from utils import load_data, borda_count, NUMERIC_COLS, COL_LABELS, REVERSE_COLS

st.set_page_config(page_title="Primerjava", page_icon="⚖️", layout="wide")

st.title("⚖️ Primerjava držav")
st.markdown("""
Primerjaj poljubne države med seboj. Vrednosti so prikazane kot **z-score** (standardizirane),
kar omogoča neposredno primerjavo atributov z različnimi merskimi enotami.

Pri atributih, kjer je **nižja vrednost boljša** (zaznava korupcije), je vrednost negirana.
""")

df = load_data()
available_cols = [c for c in NUMERIC_COLS if c in df.columns]

all_countries = sorted(df['Country name'].tolist())

with st.sidebar:
    st.header("Nastavitve")

    selected_countries = st.multiselect(
        "Izberi države:",
        options=all_countries,
        default=['Norway', 'Finland', 'Iceland', 'Denmark', 'Sweden'],
    )

    selected_col_labels = st.multiselect(
        "Atributi:",
        options=[COL_LABELS.get(c, c) for c in available_cols],
        default=[COL_LABELS.get(c, c) for c in [
            'Ladder score', 'Logged GDP per capita', 'Social support',
            'Healthy life expectancy', 'Freedom to make life choices',
            'Generosity', 'Perceptions of corruption',
        ] if c in available_cols],
    )

    chart_type = st.radio("Tip grafa:", ["Pajkova mreža (radar)", "Stolpčni diagram (z-score)"])

if not selected_countries:
    st.warning("Izberi vsaj eno državo.")
    st.stop()

if not selected_col_labels:
    st.warning("Izberi vsaj en atribut.")
    st.stop()

rev_label = {COL_LABELS.get(c, c): c for c in available_cols}
selected_cols = [rev_label[l] for l in selected_col_labels if l in rev_label]

df_std = df[selected_cols].copy()
for col in selected_cols:
    mean, std = df_std[col].mean(), df_std[col].std()
    df_std[col] = (df_std[col] - mean) / std if std > 0 else 0
    if col in REVERSE_COLS:
        df_std[col] = df_std[col] * -1

df_std['Country name'] = df['Country name'].values
df_filtered = df_std[df_std['Country name'].isin(selected_countries)]

clean_labels = [COL_LABELS.get(c, c) for c in selected_cols]
colors = px.colors.qualitative.Set2

if chart_type == "Pajkova mreža (radar)":
    fig = go.Figure()
    theta = clean_labels + [clean_labels[0]]

    for i, (_, row) in enumerate(df_filtered.iterrows()):
        values = [row[c] for c in selected_cols] + [row[selected_cols[0]]]
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=theta,
            fill='toself',
            name=row['Country name'],
            line_color=colors[i % len(colors)],
            opacity=0.6,
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        title='Primerjava držav — pajkova mreža (z-score)',
        height=560,
        legend_title='Država',
    )
    st.plotly_chart(fig, use_container_width=True)

else:
    fig = go.Figure()
    for i, (_, row) in enumerate(df_filtered.iterrows()):
        fig.add_trace(go.Bar(
            name=row['Country name'],
            x=clean_labels,
            y=[row[c] for c in selected_cols],
            marker_color=colors[i % len(colors)],
        ))

    fig.add_hline(y=0, line_dash='dash', line_color='black', opacity=0.4)
    fig.update_layout(
        barmode='group',
        title='Primerjava držav — standardizirane vrednosti (z-score)',
        yaxis_title='Z-score (odkloni od povprečja)',
        xaxis_tickangle=0,
        height=520,
        legend_title='Država',
    )
    st.plotly_chart(fig, use_container_width=True)

with st.expander("Surove vrednosti"):
    raw_cols = ['Country name'] + selected_cols
    raw_df = df[df['Country name'].isin(selected_countries)][raw_cols].copy()
    raw_df = raw_df.sort_values('Country name').set_index('Country name')
    st.dataframe(
        raw_df.rename(columns={c: COL_LABELS.get(c, c) for c in selected_cols}).rename_axis('Država'),
        use_container_width=True,
    )
