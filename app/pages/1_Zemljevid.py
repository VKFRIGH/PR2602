import streamlit as st
import plotly.express as px
from utils import load_data, borda_count, NUMERIC_COLS, COL_LABELS

st.set_page_config(page_title="Zemljevid", page_icon="🗺️", layout="wide")

st.title("🗺️ Zemljevid kakovosti življenja")
st.markdown("Vizualizacija vrednosti izbranega atributa ali skupne Borda ocene po svetu.")

df = load_data()

available_cols = [c for c in NUMERIC_COLS if c in df.columns]
label_map = {COL_LABELS.get(c, c): c for c in available_cols}

with st.sidebar:
    st.header("Nastavitve")
    mode = st.radio("Prikaži:", ["Borda score (vsi atributi)", "Posamezen atribut"])

    if mode == "Posamezen atribut":
        sel_label = st.selectbox("Izberi atribut:", list(label_map.keys()))
        color_col = label_map[sel_label]
        color_label = sel_label
        color_scale = 'Blues'
        df_map = df.copy()
    else:
        df_map = borda_count(df, available_cols)
        df_map['Rang'] = range(1, len(df_map) + 1)
        color_col = 'Borda score'
        color_label = 'Borda skupne točke'
        color_scale = 'RdYlGn'

hover_data = {'iso_code': False}
if mode == "Borda score (vsi atributi)":
    hover_data['Rang'] = True
    hover_data['Borda score'] = True
else:
    hover_data[color_col] = ':.3f'
for col in ['Ladder score', 'Human Development Index (HDI)']:
    if col in df_map.columns and col != color_col:
        hover_data[col] = ':.3f'

fig = px.choropleth(
    df_map,
    locations='iso_code',
    color=color_col,
    hover_name='Country name',
    hover_data=hover_data,
    color_continuous_scale=color_scale,
    labels={color_col: color_label},
    title=f'Kakovost življenja — {color_label}',
)
fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0}, height=600)
st.plotly_chart(fig, use_container_width=True)
