import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_growth_by_period, load_time_series_data

st.set_page_config(page_title="Uvod", layout="wide")
st.title("Uvod: pregled kakovosti življenja")

st.markdown(
    """
    **Kaj obravnavamo:** Ta stran predstavlja državo z najvišjo trenutno kakovostjo življenja in pokaže, kateri dejavniki so jo izpostavili.
    Za analizo uporabljamo uradne podatke zbranih indeksov in neto rast med začetnim in trenutnim letom.
    """
)

@st.cache_data
def load_data():
    return load_time_series_data(chunksize=10000)


df = load_data()
years = sorted(df['Year'].unique())
selected_year = st.sidebar.slider('Izberi leto za primerjavo', min_value=years[0], max_value=years[-1], value=years[-1])

latest = df[df['Year'] == selected_year].sort_values('Quality of Life Index', ascending=False)
if latest.empty:
    st.warning('Za izbrano leto ni podatkov.')
    st.stop()

best_country = latest.iloc[0]

st.markdown(f"## Najboljša država v letu {selected_year}: **{best_country['Country']}**")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric('Kakovost življenja', f"{best_country['Quality of Life Index']:.1f}")
with col2:
    st.metric('Kupna moč', f"{best_country['Purchasing Power Index']:.1f}")
with col3:
    st.metric('Zdravstveni indeks', f"{best_country['Health Care Index']:.1f}")

st.markdown(
    'Država z najvišjo kakovostjo življenja izstopa po dobri kombinaciji **varnosti**, **zdravstva** in **kupne moči**. Spodaj je primerjava z mediano vseh držav.'
)

factors = [
    'Purchasing Power Index',
    'Safety Index',
    'Health Care Index',
    'Cost of Living Index',
    'Property Price to Income Ratio',
    'Traffic Commute Time Index',
    'Pollution Index',
]
median_values = df[df['Year'] == selected_year][factors].median()

profile = pd.DataFrame({
    'Faktor': factors,
    'Izbrana država': [best_country[f] for f in factors],
    'Mediana držav': [median_values[f] for f in factors],
})
profile_melted = profile.melt(id_vars='Faktor', var_name='Skupina', value_name='Vrednost')

fig_profile = px.line_polar(
    profile_melted,
    r='Vrednost',
    theta='Faktor',
    color='Skupina',
    line_close=True,
    markers=True,
)
fig_profile.update_layout(title=f'Profil faktorjev: {best_country["Country"]} vs. mediana {selected_year}')
st.plotly_chart(fig_profile, use_container_width=True)

st.markdown('---')

start_year = years[0]
try:
    growth = get_growth_by_period(df, start_year, selected_year)
except ValueError:
    st.warning('Za izbrano obdobje ni dovolj podatkov za izračun rasti.')
    st.stop()

if not growth.empty:
    top_gainers = growth['Net_Growth'].sort_values(ascending=False).head(5).reset_index()
    top_fallers = growth['Net_Growth'].sort_values(ascending=True).head(5).reset_index()

    col4, col5 = st.columns(2)
    with col4:
        st.subheader(f'Top 5 držav z največjo rastjo ({start_year} → {selected_year})')
        st.dataframe(top_gainers.rename(columns={
            'Country': 'Država',
            'Net_Growth': 'Net Growth'
        }), use_container_width=True)
    with col5:
        st.subheader(f'Top 5 držav z največjim upadom ({start_year} → {selected_year})')
        st.dataframe(top_fallers.rename(columns={
            'Country': 'Država',
            'Net_Growth': 'Net Growth'
        }), use_container_width=True)

    st.markdown(
        '- Države z največjo rastjo pogosto izboljšujejo **varnost**, **zdravstvo** in **kupno moč**.'
        ' Čeprav ima določena država visoko začetno vrednost, je trend rasti najboljši pokazatelj njihovega premika navzgor.'
    )
else:
    st.warning('Za izbrano obdobje ni bilo dovolj podatkov, da bi izračunali neto rast.')
