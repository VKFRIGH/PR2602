import pandas as pd
import numpy as np
import os
import streamlit as st
import country_converter as coco

import warnings
warnings.filterwarnings('ignore')

_CACHE_PATH = 'app/data/processed_final.parquet'


def _build_data():
    
    cc = coco.CountryConverter()

    df_happiness = pd.read_excel('app/data/WHR23_Data_Figure_2.1.xls')
    df_happiness['iso_code'] = cc.convert(names=df_happiness['Country name'], to='ISO3')

    df_hdi = pd.read_excel('app/data/HDR25_Statistical_Annex_HDI_Table.xlsx', header=4)
    df_hdi.columns.values[0] = 'HDI rank'
    df_hdi.columns.values[1] = 'Country'
    df_hdi.drop(df_hdi.columns[[3, 5, 7, 9, 11, 13]], axis=1, inplace=True)
    df_hdi = df_hdi.iloc[:-70]
    df_hdi['iso_code'] = cc.convert(names=df_hdi['Country'], to='ISO3')

    # WDI — 78 MB Excel, slow first load; result is cached to parquet
    df_wb = pd.read_excel('app/data/WDIEXCEL.xlsx')
    df_wb.rename(columns={'Country Code': 'iso_code'}, inplace=True)
    needed_indicators = {
        'GDP per capita, PPP (current international $)',
        'Life expectancy at birth, total (years)',
        'Individuals using the Internet (% of population)',
        'School enrollment, primary (% net)',
    }
    df_wb = df_wb[df_wb['Indicator Name'].isin(needed_indicators)]

    modern_indicators = [
        'GDP per capita, PPP (current international $)',
        'Life expectancy at birth, total (years)',
        'Individuals using the Internet (% of population)',
    ]
    pivot_modern = df_wb[df_wb['Indicator Name'].isin(modern_indicators)].pivot(
        index='iso_code', columns='Indicator Name', values='2023'
    ).reset_index()
    pivot_edu = df_wb[df_wb['Indicator Name'] == 'School enrollment, primary (% net)'].pivot(
        index='iso_code', columns='Indicator Name', values='2017'
    ).reset_index()
    wb_final = pd.merge(pivot_modern, pivot_edu, on='iso_code', how='inner')

    whr_cols = [
        'iso_code', 'Country name', 'Ladder score', 'Logged GDP per capita',
        'Social support', 'Healthy life expectancy', 'Freedom to make life choices',
        'Generosity', 'Perceptions of corruption',
    ]
    skupno = pd.merge(df_happiness[whr_cols], df_hdi, on='iso_code', how='left')
    skupno = pd.merge(skupno, wb_final, on='iso_code', how='left')

    skupno_clean = skupno.dropna().copy()
    df_temp = skupno_clean.loc[:, ~skupno_clean.columns.duplicated()].copy()

    redundant = [
        'Country', 'Life expectancy at birth', 'Life expectancy at birth, total (years)',
        'GDP per capita, PPP (current international $)',
        'Gross national income (GNI) per capita', 'GNI per capita rank minus HDI rank',
    ]
    df_final = df_temp.drop(columns=redundant).copy()

    df_final.columns = [c.strip() for c in df_final.columns]
    for col in df_final.columns:
        if col not in ('iso_code', 'Country name'):
            df_final[col] = pd.to_numeric(df_final[col], errors='coerce')
    df_final = df_final.dropna().copy()

    df_final.to_parquet(_CACHE_PATH, index=False)
    return df_final

def _build_data_BK():
    cc = coco.CountryConverter()
    #majhne datoteke, ni potrebe po parquetu
    df_qol = pd.read_csv('app/data/quality_of_life_indices_by_country.csv')
    df_growth = pd.read_csv('app/data/growth_analysis.csv')
    df_growth['iso_code'] = cc.convert(names=df_growth['Country Name'], to='ISO3')
    # Coerce Year to a four-digit integer (e.g. '2014/2' -> 2014) and ensure numeric QoL
    df_qol['Year'] = df_qol['Year'].astype(str).str.extract(r'(\d{4})')[0]
    df_qol['Year'] = pd.to_numeric(df_qol['Year'], errors='coerce')
    df_qol = df_qol.groupby(['Country Name', 'Year'], as_index=False, sort=False).mean(numeric_only=True)
    df_qol['Quality of Life Index'] = pd.to_numeric(df_qol['Quality of Life Index'], errors='coerce')
    df_qol = df_qol.dropna(subset=['Year', 'Quality of Life Index']).copy()
    df_qol['Year'] = df_qol['Year'].astype(int)
    return (df_qol, df_growth)


@st.cache_data
def load_data():
    if os.path.exists(_CACHE_PATH):
        return pd.read_parquet(_CACHE_PATH)
    return _build_data()

@st.cache_data
def load_data_BK():
    return _build_data_BK()

@st.cache_data
def calculate_correlations():
    df_qol, df_growth = load_data_BK()

    factors = [
    'Purchasing Power Index',
    'Safety Index',
    'Health Care Index',
    'Cost of Living Index',
    'Property Price to Income Ratio',
    'Traffic Commute Time Index',
    'Pollution Index',
    ]

    features = df_qol.groupby('Country Name')[factors].mean(numeric_only=True)
    analysis_df = features.join(df_growth.set_index('Country Name')[['Stable Growth', "Kategorija"]]).dropna()
    analysis_df = analysis_df.reset_index().set_index('Country Name')

    corr_matrix = analysis_df[factors + ['Stable Growth']].corr()

    correlation_with_growth = corr_matrix.loc[factors, 'Stable Growth'].sort_values(ascending=False)

    return correlation_with_growth, corr_matrix, analysis_df


NUMERIC_COLS = [
    'Ladder score',
    'Logged GDP per capita',
    'Social support',
    'Healthy life expectancy',
    'Freedom to make life choices',
    'Generosity',
    'Perceptions of corruption',
    'Individuals using the Internet (% of population)',
    'School enrollment, primary (% net)',
    'Human Development Index (HDI)',
    'Expected years of schooling',
    'Mean years of schooling',
]

COL_LABELS = {
    'Ladder score': 'Indeks sreče',
    'Logged GDP per capita': 'BDP na preb. (log)',
    'Social support': 'Socialna podpora',
    'Healthy life expectancy': 'Zdrava življenjska doba',
    'Freedom to make life choices': 'Svoboda',
    'Generosity': 'Radodarnost',
    'Perceptions of corruption': 'Zaznava korupcije',
    'Individuals using the Internet (% of population)': 'Dostop do interneta (%)',
    'School enrollment, primary (% net)': 'Vpis v osnovno šolo (%)',
    'Human Development Index (HDI)': 'HDI',
    'Expected years of schooling': 'Pričakovana leta šolanja',
    'Mean years of schooling': 'Povpr. leta šolanja',
    'HDI rank': 'HDI rang',
}

# Columns where lower = better (reversed in Borda)
REVERSE_COLS = {'Perceptions of corruption'}


def borda_count(df, cols):
    df_b = df.copy()
    rank_cols = []
    for col in cols:
        asc = col not in REVERSE_COLS
        df_b[f'__rank_{col}'] = df_b[col].rank(ascending=asc)
        rank_cols.append(f'__rank_{col}')
    df_b['Borda score'] = df_b[rank_cols].sum(axis=1)
    df_b = df_b.drop(columns=rank_cols)
    return df_b.sort_values('Borda score', ascending=False).reset_index(drop=True)

