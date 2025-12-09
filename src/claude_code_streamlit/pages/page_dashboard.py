import streamlit as st
import json
from pathlib import Path
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

DATA_FILE = Path("appels_offres.json")

def load_data():
    """Charge les données depuis le fichier JSON"""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def show():
    st.title("📊 Tableau de Bord")
    st.markdown("---")
    
    data = load_data()
    appels = data.get("appels_offres", [])
    
    if not appels:
        st.warning("⚠️ Aucun appel d'offres n'a été créé pour le moment.")
        st.info("👉 Rendez-vous sur la page 'Nouvel Appel d'Offres' pour commencer")
        return
    
    # KPIs
    st.subheader("📈 Indicateurs Clés")
    
    total_appels = len(appels)
    total_documents = sum(ao["nombre_documents"] for ao in appels)
    appels_en_cours = len([ao for ao in appels if ao["etat"] == "En cours"])
    appels_traites = len([ao for ao in appels if ao["etat"] == "Traité"])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        padding: 1.5rem; border-radius: 12px; color: white; text-align: center;'>
            <h1 style='margin: 0; color: white;'>{}</h1>
            <p style='margin: 0.5rem 0 0 0; font-size: 0.9rem;'>Total Appels d'Offres</p>
        </div>
        """.format(total_appels), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
        padding: 1.5rem; border-radius: 12px; color: white; text-align: center;'>
            <h1 style='margin: 0; color: white;'>{}</h1>
            <p style='margin: 0.5rem 0 0 0; font-size: 0.9rem;'>Total Documents</p>
        </div>
        """.format(total_documents), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
        padding: 1.5rem; border-radius: 12px; color: white; text-align: center;'>
            <h1 style='margin: 0; color: white;'>{}</h1>
            <p style='margin: 0.5rem 0 0 0; font-size: 0.9rem;'>En Cours</p>
        </div>
        """.format(appels_en_cours), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
        padding: 1.5rem; border-radius: 12px; color: white; text-align: center;'>
            <h1 style='margin: 0; color: white;'>{}</h1>
            <p style='margin: 0.5rem 0 0 0; font-size: 0.9rem;'>Traités</p>
        </div>
        """.format(appels_traites), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Graphiques
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.subheader("📅 Évolution dans le temps")
        
        # Préparer les données pour le graphique
        dates_dict = {}
        for ao in appels:
            date = datetime.strptime(ao["date_ajout"], "%Y-%m-%d %H:%M:%S").date()
            date_str = date.strftime("%Y-%m-%d")
            if date_str not in dates_dict:
                dates_dict[date_str] = {"appels": 0, "documents": 0}
            dates_dict[date_str]["appels"] += 1
            dates_dict[date_str]["documents"] += ao["nombre_documents"]
        
        # Trier par date
        sorted_dates = sorted(dates_dict.items())
        
        df_evolution = pd.DataFrame([
            {"Date": date, "Appels d'offres": values["appels"], "Documents": values["documents"]}
            for date, values in sorted_dates
        ])
        
        # Calculer les cumuls
        df_evolution["Appels d'offres (Cumul)"] = df_evolution["Appels d'offres"].cumsum()
        df_evolution["Documents (Cumul)"] = df_evolution["Documents"].cumsum()
        
        fig_line = go.Figure()
        
        fig_line.add_trace(go.Scatter(
            x=df_evolution["Date"],
            y=df_evolution["Appels d'offres (Cumul)"],
            mode='lines+markers',
            name='Appels d\'offres',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8)
        ))
        
        fig_line.add_trace(go.Scatter(
            x=df_evolution["Date"],
            y=df_evolution["Documents (Cumul)"],
            mode='lines+markers',
            name='Documents',
            line=dict(color='#f5576c', width=3),
            marker=dict(size=8)
        ))
        
        fig_line.update_layout(
            xaxis_title="Date",
            yaxis_title="Nombre cumulé",
            hovermode='x unified',
            height=400,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        
        st.plotly_chart(fig_line, use_container_width=True)
    
    with col_g2:
        st.subheader("🎯 Répartition par état")
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=['En cours', 'Traité'],
            values=[appels_en_cours, appels_traites],
            hole=.4,
            marker=dict(colors=['#4facfe', '#43e97b'])
        )])
        
        fig_pie.update_layout(
            height=400,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("---")
    
    # Sélection d'un appel d'offres
    st.subheader("🔍 Rechercher un Appel d'Offres")
    
    noms_appels = [ao["nom"] for ao in appels]
    selected_appel = st.selectbox(
        "Sélectionnez un appel d'offres",
        [""] + noms_appels,
        format_func=lambda x: "Choisir..." if x == "" else x
    )
    
    if selected_appel:
        appel_selectionne = next((ao for ao in appels if ao["nom"] == selected_appel), None)
        
        if appel_selectionne:
            st.markdown("---")
            
            col_info1, col_info2, col_info3 = st.columns(3)
            
            with col_info1:
                st.metric("État", appel_selectionne["etat"])
            with col_info2:
                st.metric("Documents", appel_selectionne["nombre_documents"])
            with col_info3:
                st.metric("Date d'ajout", appel_selectionne["date_ajout"].split()[0])
            
            st.markdown("### 📁 Liste des Documents")
            
            # Créer un DataFrame pour l'affichage
            docs_data = []
            for doc in appel_selectionne["documents"]:
                nb_tableaux = len(doc.get("tableaux", []))
                taille_kb = doc.get("taille", 0) / 1024
                docs_data.append({
                    "Nom": doc["nom"],
                    "Type": doc["type"].upper(),
                    "Taille": f"{taille_kb:.1f} KB",
                    "Tableaux": nb_tableaux
                })
            
            df_docs = pd.DataFrame(docs_data)
            st.dataframe(df_docs, use_container_width=True, hide_index=True)
            
            # Statistiques sur les tableaux par catégorie
            st.markdown("### 📊 Répartition des Tableaux par Catégorie")
            
            categories_count = {"DAB": 0, "VAM": 0, "SIN": 0, "Autre": 0}
            for doc in appel_selectionne["documents"]:
                for tableau in doc.get("tableaux", []):
                    cat = tableau.get("categorie", "Autre")
                    categories_count[cat] = categories_count.get(cat, 0) + 1
            
            fig_bar = go.Figure(data=[
                go.Bar(
                    x=list(categories_count.keys()),
                    y=list(categories_count.values()),
                    marker=dict(color=['#667eea', '#f093fb', '#4facfe', '#43e97b'])
                )
            ])
            
            fig_bar.update_layout(
                xaxis_title="Catégorie",
                yaxis_title="Nombre de tableaux",
                height=300,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("---")
    
    # Liste complète des appels d'offres
    st.subheader("📋 Liste Complète des Appels d'Offres")
    
    liste_appels = []
    for ao in appels:
        liste_appels.append({
            "Nom": ao["nom"],
            "État": ao["etat"],
            "Documents": ao["nombre_documents"],
            "Date": datetime.strptime(ao["date_ajout"], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
        })
    
    df_liste = pd.DataFrame(liste_appels)
    st.dataframe(df_liste, use_container_width=True, hide_index=True)