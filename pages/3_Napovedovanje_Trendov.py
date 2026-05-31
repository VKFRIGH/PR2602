import streamlit as st
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from utils import load_time_series_data

st.set_page_config(page_title="Napovedovanje", layout="wide")
st.title("Napovedovanje trendov kakovosti življenja")

st.markdown(
    """
    Ta stran uporablja linearno regresijo na podatkih od leta 2017 naprej.
    Prikazujemo napoved do leta 2030 z intervalom zaupanja, ki narašča z oddaljenostjo.
    """
)

@st.cache_data
def load_data():
    return load_time_series_data(chunksize=10000)


df = load_data()

countries = sorted(df['Country'].unique())
current_year = int(df['Year'].max())

st.sidebar.header('Nastavitve')
selected_country = st.sidebar.selectbox(
    'Izberi državo',
    countries,
    index=countries.index('Slovenia') if 'Slovenia' in countries else 0,
)
predict_until = st.sidebar.slider('Napoved do leta', min_value=current_year + 1, max_value=2030, value=2030)

country_data = df[df['Country'] == selected_country].sort_values('Year')
filtered = country_data[country_data['Year'] >= 2017].copy()

if len(filtered) >= 3:
    X = filtered['Year'].to_numpy()
    y = filtered['Quality of Life Index'].to_numpy()

    model = LinearRegression()
    model.fit(X.reshape(-1, 1), y)
    y_pred_hist = model.predict(X.reshape(-1, 1))
    r_squared = r2_score(y, y_pred_hist)

    all_years = np.arange(2017, predict_until + 1)
    all_preds = model.predict(all_years.reshape(-1, 1))

    residuals = y - y_pred_hist
    dof = max(len(y) - 2, 1)
    mse = np.sum(residuals ** 2) / dof
    x_mean = X.mean()
    ssx = np.sum((X - x_mean) ** 2)
    se_prediction = np.sqrt(mse * (1 / len(X) + (all_years - x_mean) ** 2 / ssx))
    z_value = 1.96
    ci_band = z_value * se_prediction

    upper = all_preds + ci_band
    lower = all_preds - ci_band

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=all_years,
            y=upper,
            mode='lines',
            line=dict(width=0),
            hoverinfo='skip',
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=all_years,
            y=lower,
            mode='lines',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(46, 204, 113, 0.2)',
            name='Interval zaupanja',
        )
    )
    fig.add_trace(
        go.Scatter(
            x=all_years,
            y=all_preds,
            mode='lines',
            name='Linearna napoved',
            line=dict(color='#2ecc71', width=3),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=filtered['Year'],
            y=y,
            mode='markers',
            name='Zgodovinski podatki',
            marker=dict(color='black', size=8),
        )
    )

    fig.update_layout(
        title=f'Napoved kakovosti življenja za {selected_country} (R² = {r_squared:.2f})',
        xaxis_title='Leto',
        yaxis_title='Quality of Life Index',
        height=560,
        template='plotly_white',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(l=50, r=50, t=80, b=50),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Optional: show faceted predictions for many countries (small multiples)
    if st.checkbox('Prikaži mrežno napoved za več držav (small-multiples)'):
        countries_all = sorted(df['Country'].unique())
        default_n = min(36, len(countries_all))
        max_n = min(60, len(countries_all))
        n_show = st.slider('Število držav v mreži', min_value=9, max_value=max_n, value=default_n, step=3)
        selected_list = countries_all[:n_show]
        n_cols = 5
        n_rows = math.ceil(len(selected_list) / n_cols)
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 3, n_rows * 2.4), sharex=True, sharey=True)
        axes = axes.flatten()

        qmin = df['Quality of Life Index'].min() - 5
        qmax = df['Quality of Life Index'].max() + 5

        for i, country in enumerate(selected_list):
            ax = axes[i]
            cdata = df[df['Country'] == country].sort_values('Year')
            filt = cdata[cdata['Year'] >= 2017]
            if len(filt) < 3:
                ax.text(0.5, 0.5, 'Premalo podatkov', ha='center', va='center', fontsize=8)
                ax.set_title(country, fontsize=8)
                ax.set_ylim(qmin, qmax)
                continue
            Xc = filt['Year'].to_numpy()
            yc = filt['Quality of Life Index'].to_numpy()
            model_c = LinearRegression().fit(Xc.reshape(-1, 1), yc)
            years_all = np.arange(2017, predict_until + 1)
            preds_c = model_c.predict(years_all.reshape(-1, 1))

            residuals = yc - model_c.predict(Xc.reshape(-1, 1))
            dof_c = max(len(yc) - 2, 1)
            mse_c = np.sum(residuals ** 2) / dof_c
            x_mean_c = Xc.mean()
            ssx_c = np.sum((Xc - x_mean_c) ** 2)
            se_pred_c = np.sqrt(mse_c * (1 / len(Xc) + (years_all - x_mean_c) ** 2 / ssx_c))
            z = 1.96
            upper_c = preds_c + z * se_pred_c
            lower_c = preds_c - z * se_pred_c

            ax.plot(years_all, preds_c, color='#2ecc71', linewidth=1)
            ax.fill_between(years_all, lower_c, upper_c, color='lightgreen', alpha=0.35)
            ax.scatter(filt['Year'], yc, color='black', s=10)
            ax.set_title(country, fontsize=8)
            ax.set_ylim(qmin, qmax)

        # remove any unused axes
        for j in range(len(selected_list), len(axes)):
            fig.delaxes(axes[j])

        plt.tight_layout()
        st.pyplot(fig)

    future_years = all_years[all_years > current_year]
    future_preds = all_preds[all_years > current_year]

    st.subheader('Napovedane vrednosti')
    prediction_table = pd.DataFrame(
        {
            'Leto': future_years,
            'Napovedani Quality of Life Index': np.round(future_preds, 1),
        }
    )
    st.dataframe(prediction_table, use_container_width=True)

    slope = model.coef_[0]
    st.markdown(
        f'- Linearni model ocenjuje povprečno spremembo kakovosti življenja za **{slope:.2f} točke na leto**.'
        f'\n- R² = **{r_squared:.2f}** pomeni, da model pojasni večino linearnega trenda v zgodovinskih podatkih.'
        '\n- Interval zaupanja se širi, ker so napovedi dlje od zgodovinskega obdobja manj zanesljive.'
    )
else:
    st.warning('Premalo zgodovinskih podatkov od leta 2017 dalje za zanesljivo napoved.')
