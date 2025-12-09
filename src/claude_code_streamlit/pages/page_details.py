import streamlit as st
import json
from pathlib import Path
import pandas as pd

DATA_FILE = Path("appels_offres.json")

def load_data():
    """Charge les données depuis le fichier JSON"""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def show():
    st.title("📄 Détails de l'Appel d'Offres")
    st.markdown("---")
    
    data = load_data()
    appels = data.get("appels_offres", [])
    
    if not appels:
        st.warning("⚠️ Aucun appel d'offres n'a été créé pour le moment.")
        st.info("👉 Rendez-vous sur la page 'Nouvel Appel d'Offres' pour commencer")
        return
    
    # Sélection de l'appel d'offres
    noms_appels = [ao["nom"] for ao in appels]
    selected_appel = st.selectbox(
        "Sélectionnez un appel d'offres",
        noms_appels,
        help="Choisissez l'appel d'offres dont vous souhaitez voir les détails"
    )
    
    appel = next((ao for ao in appels if ao["nom"] == selected_appel), None)
    
    if not appel:
        return
    
    st.markdown("---")
    
    # Onglets pour organiser l'information
    tab1, tab2, tab3 = st.tabs(["❓ Questions & Réponses", "📊 Tableaux", "ℹ️ Informations"])
    
    with tab1:
        st.subheader("Questions & Réponses")
        st.markdown("*20 questions standards avec leurs réponses*")
        st.markdown("")
        
        questions = appel.get("questions", [])
        
        # Afficher les questions dans des expanders élégants
        for i, qa in enumerate(questions, 1):
            with st.expander(f"**Question {i}:** {qa['question']}", expanded=(i==1)):
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%); 
                padding: 1rem; border-radius: 8px; border-left: 4px solid #0284c7;'>
                    <p style='margin: 0; color: #0c4a6e; font-weight: 500;'>
                        {qa['reponse']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        # Statistiques sur les questions
        st.markdown("---")
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric("Total Questions", len(questions))
        with col_stat2:
            avg_length = sum(len(qa['reponse']) for qa in questions) / len(questions) if questions else 0
            st.metric("Longueur moyenne des réponses", f"{avg_length:.0f} caractères")
    
    with tab2:
        st.subheader("Tableaux Classés par Catégorie")
        
        # Organiser les tableaux par catégorie
        tableaux_par_categorie = {"DAB": [], "VAM": [], "SIN": [], "Autre": []}
        
        for doc in appel["documents"]:
            for tableau in doc.get("tableaux", []):
                cat = tableau.get("categorie", "Autre")
                tableau_info = {
                    "Document": doc["nom"],
                    "Tableau": tableau["nom"],
                    "Lignes": tableau["lignes"],
                    "Colonnes": tableau["colonnes"],
                    "Contenu": tableau["contenu"]
                }
                tableaux_par_categorie[cat].append(tableau_info)
        
        # Afficher chaque catégorie
        categories_config = {
            "DAB": {"icon": "🟦", "color": "#667eea"},
            "VAM": {"icon": "🟪", "color": "#f093fb"},
            "SIN": {"icon": "🟩", "color": "#4facfe"},
            "Autre": {"icon": "🟨", "color": "#43e97b"}
        }
        
        for categorie, config in categories_config.items():
            tableaux = tableaux_par_categorie[categorie]
            
            if tableaux:
                st.markdown(f"""
                <div style='background: {config['color']}20; padding: 0.5rem 1rem; 
                border-radius: 8px; border-left: 4px solid {config['color']}; margin: 1rem 0;'>
                    <h3 style='margin: 0; color: {config['color']};'>
                        {config['icon']} {categorie} ({len(tableaux)} tableau{'x' if len(tableaux) > 1 else ''})
                    </h3>
                </div>
                """, unsafe_allow_html=True)
                
                for i, tableau in enumerate(tableaux, 1):
                    with st.expander(f"📊 {tableau['Tableau']}", expanded=(i==1)):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write(f"**Document:** {tableau['Document']}")
                        with col2:
                            st.write(f"**Dimensions:** {tableau['Lignes']} × {tableau['Colonnes']}")
                        with col3:
                            st.write(f"**Catégorie:** {categorie}")
                        
                        st.info(tableau['Contenu'])
            else:
                st.markdown(f"""
                <div style='background: #f3f4f6; padding: 0.5rem 1rem; 
                border-radius: 8px; margin: 1rem 0;'>
                    <p style='margin: 0; color: #6b7280;'>
                        {config['icon']} Aucun tableau dans la catégorie {categorie}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        # Statistiques globales sur les tableaux
        st.markdown("---")
        st.subheader("📈 Statistiques des Tableaux")
        
        total_tableaux = sum(len(tableaux) for tableaux in tableaux_par_categorie.values())
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Tableaux", total_tableaux)
        with col2:
            st.metric("DAB", len(tableaux_par_categorie["DAB"]))
        with col3:
            st.metric("VAM", len(tableaux_par_categorie["VAM"]))
        with col4:
            st.metric("SIN", len(tableaux_par_categorie["SIN"]))
    
    with tab3:
        st.subheader("Informations Générales")
        
        # Carte d'information principale
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        padding: 2rem; border-radius: 12px; color: white; margin: 1rem 0;'>
            <h2 style='margin: 0 0 1rem 0; color: white;'>{appel['nom']}</h2>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;'>
                <div>
                    <p style='margin: 0.5rem 0; opacity: 0.9;'>📅 Date d'ajout</p>
                    <p style='margin: 0; font-size: 1.2rem; font-weight: bold;'>{appel['date_ajout']}</p>
                </div>
                <div>
                    <p style='margin: 0.5rem 0; opacity: 0.9;'>🎯 État</p>
                    <p style='margin: 0; font-size: 1.2rem; font-weight: bold;'>{appel['etat']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📁 Documents")
        
        # Tableau des documents
        docs_data = []
        for doc in appel["documents"]:
            nb_tableaux = len(doc.get("tableaux", []))
            taille_kb = doc.get("taille", 0) / 1024
            
            # Compter les tableaux par catégorie pour ce document
            cat_count = {"DAB": 0, "VAM": 0, "SIN": 0, "Autre": 0}
            for tableau in doc.get("tableaux", []):
                cat = tableau.get("categorie", "Autre")
                cat_count[cat] += 1
            
            docs_data.append({
                "📄 Nom": doc["nom"],
                "📦 Type": doc["type"].upper(),
                "💾 Taille": f"{taille_kb:.1f} KB",
                "📊 Tableaux": nb_tableaux,
                "🟦 DAB": cat_count["DAB"],
                "🟪 VAM": cat_count["VAM"],
                "🟩 SIN": cat_count["SIN"],
                "🟨 Autre": cat_count["Autre"]
            })
        
        df_docs = pd.DataFrame(docs_data)
        st.dataframe(df_docs, use_container_width=True, hide_index=True)
        
        # Résumé global
        st.markdown("### 📊 Résumé Global")
        
        total_tableaux = sum(len(doc.get("tableaux", [])) for doc in appel["documents"])
        total_taille = sum(doc.get("taille", 0) for doc in appel["documents"]) / (1024 * 1024)
        
        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        
        with col_r1:
            st.markdown("""
            <div style='background: #dbeafe; padding: 1rem; border-radius: 8px; text-align: center;'>
                <h3 style='margin: 0; color: #1e40af;'>{}</h3>
                <p style='margin: 0.5rem 0 0 0; color: #1e40af;'>Documents</p>
            </div>
            """.format(appel["nombre_documents"]), unsafe_allow_html=True)
        
        with col_r2:
            st.markdown("""
            <div style='background: #fce7f3; padding: 1rem; border-radius: 8px; text-align: center;'>
                <h3 style='margin: 0; color: #9f1239;'>{}</h3>
                <p style='margin: 0.5rem 0 0 0; color: #9f1239;'>Tableaux</p>
            </div>
            """.format(total_tableaux), unsafe_allow_html=True)
        
        with col_r3:
            st.markdown("""
            <div style='background: #dcfce7; padding: 1rem; border-radius: 8px; text-align: center;'>
                <h3 style='margin: 0; color: #14532d;'>{}</h3>
                <p style='margin: 0.5rem 0 0 0; color: #14532d;'>Questions</p>
            </div>
            """.format(len(appel.get("questions", []))), unsafe_allow_html=True)
        
        with col_r4:
            st.markdown("""
            <div style='background: #fef3c7; padding: 1rem; border-radius: 8px; text-align: center;'>
                <h3 style='margin: 0; color: #78350f;'>{:.2f} MB</h3>
                <p style='margin: 0.5rem 0 0 0; color: #78350f;'>Taille totale</p>
            </div>
            """.format(total_taille), unsafe_allow_html=True)