import streamlit as st

st.title("Izberi stran")

if st.button("🗺️ Zemljevid"):
    st.switch_page("pages/1_Zemljevid.py")

if st.button("📊 Primerjava"):
    st.switch_page("pages/2_Primerjava.py")

if st.button("📈 Primerjava trendov"):
    st.switch_page("pages/3_Primerjava_Trendov.py")
