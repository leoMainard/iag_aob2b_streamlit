import streamlit as st
from pathlib import Path
import json

# Configuration de la page
st.set_page_config(
    page_title="Gestion d'Appels d'Offres",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS personnalisés
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #0066cc;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #0052a3;
    }
    h1 {
        color: #1e3a8a;
        font-weight: 700;
    }
    h2, h3 {
        color: #3b82f6;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Initialisation du fichier JSON
DATA_FILE = Path("appels_offres.json")

def init_data_file():
    if not DATA_FILE.exists():
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump({"appels_offres": []}, f, ensure_ascii=False, indent=2)

init_data_file()

# Navigation
st.sidebar.title("📋 Navigation")
page = st.sidebar.radio(
    "Aller à",
    ["🏠 Accueil", "📤 Nouvel Appel d'Offres", "📊 Tableau de Bord", "📄 Détails"],
    label_visibility="collapsed"
)

# Import des pages
if page == "🏠 Accueil":
    st.title("🏠 Bienvenue dans le Système de Gestion d'Appels d'Offres")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        padding: 2rem; border-radius: 12px; color: white; text-align: center;'>
            <h2>📤</h2>
            <h3>Ajouter</h3>
            <p>Créez un nouvel appel d'offres</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
        padding: 2rem; border-radius: 12px; color: white; text-align: center;'>
            <h2>📊</h2>
            <h3>Analyser</h3>
            <p>Visualisez vos statistiques</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
        padding: 2rem; border-radius: 12px; color: white; text-align: center;'>
            <h2>📄</h2>
            <h3>Consulter</h3>
            <p>Accédez aux détails</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("👈 Utilisez le menu latéral pour naviguer entre les différentes sections")

elif page == "📤 Nouvel Appel d'Offres":
    from pages import page_upload
    page_upload.show()

elif page == "📊 Tableau de Bord":
    from pages import page_dashboard
    page_dashboard.show()

elif page == "📄 Détails":
    from pages import page_details
    page_details.show()