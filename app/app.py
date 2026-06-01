import streamlit as st

st.title("Izberi stran")

if st.button("🗺️ Zemljevid"):
    st.switch_page("pages/1_Zemljevid.py")

if st.button("📊 Primerjava"):
    st.switch_page("pages/2_Primerjava.py")

if st.button("📊 Rast QOL in dejavniki"):
    st.switch_page("pages/3_Rast_in_dejavniki.py")

if st.button("📈 Primerjava trendov"):
    st.switch_page("pages/4_Primerjava_Trendov.py")
