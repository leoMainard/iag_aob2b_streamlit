import streamlit as st
import pandas as pd
from streamlit_extras.metric_cards import style_metric_cards

from iag_aob2b_streamlit.utils.read_fake_data import read_json_to_df
from iag_aob2b_streamlit.utils.streamlit_utils import get_icon_svg

# ----------------------------------------------------
# Chargement des données
# ----------------------------------------------------
fake_data = read_json_to_df("src/iag_aob2b_streamlit/conf/fake_datas.json")

# ----------------------------------------------------
# Styles généraux
# ----------------------------------------------------
st.set_page_config(page_title="AOB2B", layout="wide")

st.markdown("""
<style>
/* Ajustement global */
.main {
    background-color: #F7F9FC;
}

/* Card documents */
.doc-card {
    padding: 12px;
    border-radius: 12px;
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    margin-bottom: 8px;
}

/* Titre documents */
.doc-title {
    font-size: 17px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# Header
# ----------------------------------------------------
st.title("Bienvenue dans AOB2B ! 🚀")
# st.write("Consultez rapidement les AOs, leurs statuts et leurs documents.")

# ----------------------------------------------------
# Selectbox AO
# ----------------------------------------------------
selected_ao = st.selectbox(
    label="🔍 Sélectionner un AO :",
    options=[ao['AO'] for ao in fake_data],
    placeholder="Rechercher un AO",
    index=None
)

st.divider()

# ----------------------------------------------------
# Colonne métriques
# ----------------------------------------------------
col1, col2 = st.columns([1, 5])

# col1.subheader("📊 Statistiques générales")

col1.metric("Nombre d'AO déposés", len(fake_data))

loaded_aos = sum(1 for ao in fake_data if ao["Status"] == "Chargé")
col1.metric("AO Chargés", loaded_aos, f"{loaded_aos/len(fake_data)*100:.1f}%")

total_docs = sum(len(ao["Documents"]) for ao in fake_data)
col1.metric("Documents totaux", total_docs)

style_metric_cards(background_color="#FFFFFF", border_radius_px=12, border_left_color="#D43838")

# ----------------------------------------------------
# Tableau des AO
# ----------------------------------------------------
if selected_ao:
    filtered_data = [ao for ao in fake_data if ao['AO'] == selected_ao]
else:
    filtered_data = fake_data

data_to_show = [
    {
        "AO": ao["AO"],
        "Date ajout": ao["Date ajout"],
        "Status": ao["Status"],
        "Documents": len(ao["Documents"])
    }
    for ao in filtered_data
]

df = pd.DataFrame(data_to_show)

with col2:
    st.subheader("📁 Liste des AOs")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Status": st.column_config.SelectboxColumn(
                "Status",
                options=["Chargé", "En attente"],
                required=True,
                format_func=lambda x: "🟢 Chargé" if x == "Chargé" else "🟠 En attente",
            )
        }
    )

# ----------------------------------------------------
# Liste des documents pour AO sélectionné (corrigé)
# ----------------------------------------------------
if selected_ao:
    col2.divider()
    col2.subheader(f"📄 Documents pour **{selected_ao}**")

    docs = filtered_data[0]["Documents"]

    # CSS + structure HTML
    css = """
    <style>
    .doc-list-container {
        max-height: 300px;
        overflow-y: auto;
        padding-right: 6px;
        margin-top: 8px;
    }
    .doc-card {
        display:flex;
        justify-content:space-between;
        align-items:center;
        padding:10px 12px;
        border-radius:10px;
        background-color:#fff;
        border:1px solid #e6e6e6;
        margin-bottom:8px;
        font-family: "Segoe UI", Roboto, Arial;
    }
    .doc-title {
        font-weight:600;
        font-size:14px;
        display:flex;
        gap:8px;
        align-items:center;
    }
    .doc-type {
        color:#666;
        font-size:13px;
        white-space:nowrap;
    }
    .doc-list-container::-webkit-scrollbar {
        width:8px;
    }
    .doc-list-container::-webkit-scrollbar-thumb {
        background: rgba(0,0,0,0.15);
        border-radius: 8px;
    }
    </style>
    """

    cards = ""
    for doc in docs:
        icon = get_icon_svg(doc["Type"])
        cards += f"""
        <div class="doc-card">
            <div class="doc-title">{icon} {doc['Nom']}</div>
            <div class="doc-type">{doc['Type']}</div>
        </div>
        """

    full_html = css + f"""
    <div class="doc-list-container">
        {cards}
    </div>
    """

    col2.html(full_html)




