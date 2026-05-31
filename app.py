import streamlit as st

st.set_page_config(page_title="Quality of Life Explorer", layout="wide")
st.title("Projekt: kakovost življenja v državah")

st.markdown(
    """
    Dobrodošli v interaktivni analizi kakovosti življenja.
    Uporabite strani v levi navigaciji za odgovor na glavna vprašanja projekta:

    - **Uvod:** Katera država ima najboljšo kakovost življenja in zakaj?
    - **Trendi rasti in padca:** Kateri so hitrorastoči in upadajoči trgi?
    - **Faktorji vpliva:** Katere dejavnike povežemo s kakovostjo življenja?
    - **Napovedovanje trendov:** Kaj pričakujemo do leta 2030?
    """
)

st.markdown("---")

st.markdown(
    """
    ### Kaj obravnavamo
    - Povezava kakovosti življenja s ključnimi indeksi: kupna moč, varnost, zdravstvo, stroški, onesnaženost.
    - Identifikacija držav z najboljšo trenutno kakovostjo in trendi rasti ali upada.
    - Vizualizacije trendov izbranih držav in model linearne napovedi za prihodnost.
    """
)

st.info(
    "Za polno izkušnjo izberite eno od strani v levi navigaciji. Če želite hitro primerjavo držav ali faktorjev, pobrskajte po zavihki in grafi."
)
