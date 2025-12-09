import gradio as gr
from pathlib import Path
import json
from datetime import datetime
import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Configuration
DATA_FILE = Path("appels_offres.json")

# CSS personnalisé
custom_css = """
.gradio-container {
    font-family: 'Inter', sans-serif;
}
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 12px;
    color: white;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
h1 {
    color: #1e3a8a;
    font-weight: 700;
}
"""

def init_data_file():
    """Initialise le fichier JSON s'il n'existe pas"""
    if not DATA_FILE.exists():
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump({"appels_offres": []}, f, ensure_ascii=False, indent=2)

def load_data():
    """Charge les données depuis le fichier JSON"""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_questions():
    """Génère 20 questions standards avec leurs réponses"""
    questions = [
        {"question": "Quelle est la durée du contrat proposé ?", "reponse": "36 mois avec possibilité de renouvellement"},
        {"question": "Quel est le budget estimé pour ce projet ?", "reponse": "Entre 500K€ et 1M€"},
        {"question": "Quels sont les délais de réalisation ?", "reponse": "6 mois après notification"},
        {"question": "Quelles sont les modalités de paiement ?", "reponse": "Paiement mensuel sur présentation de facture"},
        {"question": "Quelles sont les pénalités de retard ?", "reponse": "0,1% du montant par jour de retard"},
        {"question": "Quelle est la date limite de soumission ?", "reponse": "30 jours à compter de la publication"},
        {"question": "Quels sont les critères de sélection ?", "reponse": "Prix (40%), qualité technique (40%), délais (20%)"},
        {"question": "Y a-t-il des conditions de sous-traitance ?", "reponse": "Sous-traitance autorisée jusqu'à 30%"},
        {"question": "Quelles sont les garanties demandées ?", "reponse": "Garantie bancaire de 5% du montant"},
        {"question": "Quel est le mode de consultation ?", "reponse": "Appel d'offres ouvert"},
        {"question": "Y a-t-il une visite de site obligatoire ?", "reponse": "Oui, visite prévue le 15 du mois"},
        {"question": "Quelles sont les assurances requises ?", "reponse": "RC Pro et décennale obligatoires"},
        {"question": "Quel est le délai de validité des offres ?", "reponse": "120 jours à compter de la date limite"},
        {"question": "Y a-t-il des variantes autorisées ?", "reponse": "Oui, variantes techniques acceptées"},
        {"question": "Quelles sont les modalités de livraison ?", "reponse": "Livraison échelonnée selon planning"},
        {"question": "Y a-t-il une période de garantie ?", "reponse": "Garantie de 24 mois minimum"},
        {"question": "Quels sont les documents obligatoires ?", "reponse": "DC1, DC2, KBIS, attestations fiscales"},
        {"question": "Y a-t-il des critères environnementaux ?", "reponse": "Certification ISO 14001 souhaitée"},
        {"question": "Quelle est la forme juridique requise ?", "reponse": "Toute forme juridique acceptée"},
        {"question": "Y a-t-il une clause de réexamen ?", "reponse": "Révision annuelle des prix possible"}
    ]
    return questions

def generate_tables_for_document(doc_name):
    """Génère des tableaux aléatoires pour un document"""
    categories = ["DAB", "VAM", "SIN", "Autre"]
    num_tables = random.randint(2, 5)
    tables = []
    
    for i in range(num_tables):
        category = random.choice(categories)
        rows = random.randint(3, 8)
        cols = random.randint(3, 6)
        
        table = {
            "nom": f"Tableau_{i+1}_{doc_name}",
            "categorie": category,
            "lignes": rows,
            "colonnes": cols,
            "contenu": f"Données du tableau {i+1} - Catégorie: {category}"
        }
        tables.append(table)
    
    return tables

# ============= PAGE 1: UPLOAD =============
def upload_appel_offres(nom_appel, etat, files):
    """Crée un nouvel appel d'offres"""
    if not nom_appel:
        return "⚠️ Veuillez saisir un nom pour l'appel d'offres", None
    
    if not files:
        return "⚠️ Veuillez déposer au moins un document", None
    
    # Charger les données existantes
    data = load_data()
    
    # Préparer les documents avec leurs tableaux
    documents = []
    for file in files:
        file_name = Path(file.name).name
        file_type = Path(file.name).suffix[1:]
        file_size = Path(file.name).stat().st_size if Path(file.name).exists() else 0
        
        tables = generate_tables_for_document(file_name)
        documents.append({
            "nom": file_name,
            "type": file_type,
            "taille": file_size,
            "tableaux": tables
        })
    
    # Créer le nouvel appel d'offres
    nouvel_appel = {
        "id": len(data["appels_offres"]) + 1,
        "nom": nom_appel,
        "date_ajout": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "etat": etat,
        "documents": documents,
        "nombre_documents": len(documents),
        "questions": generate_questions()
    }
    
    # Ajouter à la liste
    data["appels_offres"].append(nouvel_appel)
    
    # Sauvegarder
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    total_tables = sum(len(doc["tableaux"]) for doc in documents)
    
    summary = f"""
✅ **Appel d'offres créé avec succès!**

📋 **Résumé:**
- **Nom:** {nom_appel}
- **État:** {etat}
- **Nombre de documents:** {len(documents)}
- **Date de création:** {nouvel_appel['date_ajout']}
- **Questions générées:** {len(nouvel_appel['questions'])}
- **Tableaux générés:** {total_tables}

👉 Consultez le Tableau de Bord pour visualiser vos données
"""
    
    return summary, None

# ============= PAGE 2: DASHBOARD =============
def create_dashboard():
    """Crée le tableau de bord avec KPIs et graphiques"""
    data = load_data()
    appels = data.get("appels_offres", [])
    
    if not appels:
        return "⚠️ Aucun appel d'offres disponible", None, None, None, []
    
    # Calcul des KPIs
    total_appels = len(appels)
    total_documents = sum(ao["nombre_documents"] for ao in appels)
    appels_en_cours = len([ao for ao in appels if ao["etat"] == "En cours"])
    appels_traites = len([ao for ao in appels if ao["etat"] == "Traité"])
    
    kpi_text = f"""
# 📊 Indicateurs Clés

<div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 2rem 0;'>
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 12px; color: white; text-align: center;'>
        <h1 style='margin: 0; color: white;'>{total_appels}</h1>
        <p style='margin: 0.5rem 0 0 0;'>Total Appels d'Offres</p>
    </div>
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 1.5rem; border-radius: 12px; color: white; text-align: center;'>
        <h1 style='margin: 0; color: white;'>{total_documents}</h1>
        <p style='margin: 0.5rem 0 0 0;'>Total Documents</p>
    </div>
    <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 1.5rem; border-radius: 12px; color: white; text-align: center;'>
        <h1 style='margin: 0; color: white;'>{appels_en_cours}</h1>
        <p style='margin: 0.5rem 0 0 0;'>En Cours</p>
    </div>
    <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 1.5rem; border-radius: 12px; color: white; text-align: center;'>
        <h1 style='margin: 0; color: white;'>{appels_traites}</h1>
        <p style='margin: 0.5rem 0 0 0;'>Traités</p>
    </div>
</div>
"""
    
    # Graphique d'évolution
    dates_dict = {}
    for ao in appels:
        date = datetime.strptime(ao["date_ajout"], "%Y-%m-%d %H:%M:%S").date()
        date_str = date.strftime("%Y-%m-%d")
        if date_str not in dates_dict:
            dates_dict[date_str] = {"appels": 0, "documents": 0}
        dates_dict[date_str]["appels"] += 1
        dates_dict[date_str]["documents"] += ao["nombre_documents"]
    
    sorted_dates = sorted(dates_dict.items())
    df_evolution = pd.DataFrame([
        {"Date": date, "Appels": values["appels"], "Documents": values["documents"]}
        for date, values in sorted_dates
    ])
    
    df_evolution["Appels (Cumul)"] = df_evolution["Appels"].cumsum()
    df_evolution["Documents (Cumul)"] = df_evolution["Documents"].cumsum()
    
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df_evolution["Date"],
        y=df_evolution["Appels (Cumul)"],
        mode='lines+markers',
        name="Appels d'offres",
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
        title="📅 Évolution dans le temps",
        xaxis_title="Date",
        yaxis_title="Nombre cumulé",
        height=400,
        hovermode='x unified'
    )
    
    # Graphique circulaire
    fig_pie = go.Figure(data=[go.Pie(
        labels=['En cours', 'Traité'],
        values=[appels_en_cours, appels_traites],
        hole=.4,
        marker=dict(colors=['#4facfe', '#43e97b'])
    )])
    fig_pie.update_layout(
        title="🎯 Répartition par état",
        height=400
    )
    
    # Liste des appels
    noms_appels = [ao["nom"] for ao in appels]
    
    # DataFrame de la liste complète
    liste_appels = []
    for ao in appels:
        liste_appels.append({
            "Nom": ao["nom"],
            "État": ao["etat"],
            "Documents": ao["nombre_documents"],
            "Date": datetime.strptime(ao["date_ajout"], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
        })
    
    df_liste = pd.DataFrame(liste_appels)
    
    return kpi_text, fig_line, fig_pie, df_liste, noms_appels

def show_appel_details(nom_appel):
    """Affiche les détails d'un appel d'offres sélectionné"""
    if not nom_appel:
        return "Veuillez sélectionner un appel d'offres", None, None
    
    data = load_data()
    appels = data.get("appels_offres", [])
    appel = next((ao for ao in appels if ao["nom"] == nom_appel), None)
    
    if not appel:
        return "Appel d'offres introuvable", None, None
    
    # Informations générales
    info_text = f"""
## 📋 {appel['nom']}

**📅 Date d'ajout:** {appel['date_ajout']}  
**🎯 État:** {appel['etat']}  
**📄 Nombre de documents:** {appel['nombre_documents']}
"""
    
    # DataFrame des documents
    docs_data = []
    for doc in appel["documents"]:
        nb_tableaux = len(doc.get("tableaux", []))
        taille_kb = doc.get("taille", 0) / 1024
        docs_data.append({
            "Nom": doc["nom"],
            "Type": doc["type"].upper(),
            "Taille (KB)": f"{taille_kb:.1f}",
            "Tableaux": nb_tableaux
        })
    
    df_docs = pd.DataFrame(docs_data)
    
    # Graphique des catégories
    categories_count = {"DAB": 0, "VAM": 0, "SIN": 0, "Autre": 0}
    for doc in appel["documents"]:
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
        title="📊 Répartition des Tableaux par Catégorie",
        xaxis_title="Catégorie",
        yaxis_title="Nombre de tableaux",
        height=300
    )
    
    return info_text, df_docs, fig_bar

# ============= PAGE 3: DETAILS =============
def show_questions_reponses(nom_appel):
    """Affiche les questions/réponses"""
    if not nom_appel:
        return "Veuillez sélectionner un appel d'offres"
    
    data = load_data()
    appels = data.get("appels_offres", [])
    appel = next((ao for ao in appels if ao["nom"] == nom_appel), None)
    
    if not appel:
        return "Appel d'offres introuvable"
    
    questions = appel.get("questions", [])
    
    output = f"# ❓ Questions & Réponses - {appel['nom']}\n\n"
    output += "*20 questions standards avec leurs réponses*\n\n"
    
    for i, qa in enumerate(questions, 1):
        output += f"### Question {i}: {qa['question']}\n"
        output += f"**Réponse:** {qa['reponse']}\n\n"
    
    return output

def show_tableaux(nom_appel):
    """Affiche les tableaux classés par catégorie"""
    if not nom_appel:
        return "Veuillez sélectionner un appel d'offres"
    
    data = load_data()
    appels = data.get("appels_offres", [])
    appel = next((ao for ao in appels if ao["nom"] == nom_appel), None)
    
    if not appel:
        return "Appel d'offres introuvable"
    
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
    
    output = f"# 📊 Tableaux Classés - {appel['nom']}\n\n"
    
    categories_config = {
        "DAB": {"icon": "🟦", "color": "#667eea"},
        "VAM": {"icon": "🟪", "color": "#f093fb"},
        "SIN": {"icon": "🟩", "color": "#4facfe"},
        "Autre": {"icon": "🟨", "color": "#43e97b"}
    }
    
    for categorie, config in categories_config.items():
        tableaux = tableaux_par_categorie[categorie]
        output += f"\n## {config['icon']} Catégorie {categorie} ({len(tableaux)} tableau{'x' if len(tableaux) > 1 else ''})\n\n"
        
        if tableaux:
            for tableau in tableaux:
                output += f"### 📊 {tableau['Tableau']}\n"
                output += f"- **Document:** {tableau['Document']}\n"
                output += f"- **Dimensions:** {tableau['Lignes']} × {tableau['Colonnes']}\n"
                output += f"- **Contenu:** {tableau['Contenu']}\n\n"
        else:
            output += f"*Aucun tableau dans cette catégorie*\n\n"
    
    return output

def show_informations(nom_appel):
    """Affiche les informations complètes"""
    if not nom_appel:
        return "Veuillez sélectionner un appel d'offres", None
    
    data = load_data()
    appels = data.get("appels_offres", [])
    appel = next((ao for ao in appels if ao["nom"] == nom_appel), None)
    
    if not appel:
        return "Appel d'offres introuvable", None
    
    total_tableaux = sum(len(doc.get("tableaux", [])) for doc in appel["documents"])
    total_taille = sum(doc.get("taille", 0) for doc in appel["documents"]) / (1024 * 1024)
    
    info_text = f"""
# ℹ️ Informations Complètes - {appel['nom']}

## 📋 Résumé Global

- **📅 Date d'ajout:** {appel['date_ajout']}
- **🎯 État:** {appel['etat']}
- **📄 Nombre de documents:** {appel['nombre_documents']}
- **📊 Total tableaux:** {total_tableaux}
- **❓ Questions générées:** {len(appel.get('questions', []))}
- **💾 Taille totale:** {total_taille:.2f} MB
"""
    
    # DataFrame des documents détaillé
    docs_data = []
    for doc in appel["documents"]:
        nb_tableaux = len(doc.get("tableaux", []))
        taille_kb = doc.get("taille", 0) / 1024
        
        cat_count = {"DAB": 0, "VAM": 0, "SIN": 0, "Autre": 0}
        for tableau in doc.get("tableaux", []):
            cat = tableau.get("categorie", "Autre")
            cat_count[cat] += 1
        
        docs_data.append({
            "Nom": doc["nom"],
            "Type": doc["type"].upper(),
            "Taille (KB)": f"{taille_kb:.1f}",
            "Tableaux": nb_tableaux,
            "DAB": cat_count["DAB"],
            "VAM": cat_count["VAM"],
            "SIN": cat_count["SIN"],
            "Autre": cat_count["Autre"]
        })
    
    df_docs = pd.DataFrame(docs_data)
    
    return info_text, df_docs

# ============= INTERFACE GRADIO =============
def create_app():
    init_data_file()
    
    with gr.Blocks(css=custom_css, title="Gestion d'Appels d'Offres", theme=gr.themes.Soft()) as app:
        gr.Markdown("""
        # 📋 Gestion d'Appels d'Offres
        ### Application moderne de gestion et suivi des appels d'offres
        """)
        
        with gr.Tabs() as tabs:
            # TAB 1: UPLOAD
            with gr.Tab("📤 Nouvel Appel d'Offres"):
                gr.Markdown("## Créer un nouvel appel d'offres")
                
                with gr.Row():
                    with gr.Column(scale=2):
                        nom_input = gr.Textbox(
                            label="Nom de l'appel d'offres",
                            placeholder="Ex: Appel d'offres infrastructure 2024",
                            lines=1
                        )
                        etat_input = gr.Radio(
                            choices=["En cours", "Traité"],
                            label="État de l'appel d'offres",
                            value="En cours"
                        )
                    with gr.Column(scale=1):
                        gr.Markdown("""
                        💡 **Conseil**
                        
                        Choisissez un nom clair et unique pour faciliter la recherche ultérieure.
                        """)
                
                files_input = gr.File(
                    label="Déposez vos documents",
                    file_count="multiple",
                    file_types=[".pdf", ".docx", ".xlsx", ".txt", ".doc", ".xls"]
                )
                
                with gr.Row():
                    submit_btn = gr.Button("✅ Valider et Sauvegarder", variant="primary", scale=1)
                    clear_btn = gr.Button("❌ Effacer", scale=1)
                
                output_upload = gr.Markdown()
                
                submit_btn.click(
                    fn=upload_appel_offres,
                    inputs=[nom_input, etat_input, files_input],
                    outputs=[output_upload, files_input]
                )
                
                clear_btn.click(
                    fn=lambda: ("", "En cours", None, ""),
                    outputs=[nom_input, etat_input, files_input, output_upload]
                )
            
            # TAB 2: DASHBOARD
            with gr.Tab("📊 Tableau de Bord"):
                gr.Markdown("## Vue d'ensemble et statistiques")
                
                refresh_btn = gr.Button("🔄 Actualiser", variant="secondary")
                
                kpi_output = gr.Markdown()
                
                with gr.Row():
                    graph_line = gr.Plot(label="Évolution temporelle")
                    graph_pie = gr.Plot(label="Répartition par état")
                
                gr.Markdown("### 🔍 Rechercher un Appel d'Offres")
                
                appel_dropdown = gr.Dropdown(
                    label="Sélectionnez un appel d'offres",
                    choices=[],
                    interactive=True,
                    allow_custom_value=False
                )
                
                details_info = gr.Markdown()
                details_table = gr.Dataframe(label="Documents")
                details_graph = gr.Plot(label="Tableaux par catégorie")
                
                gr.Markdown("### 📋 Liste Complète des Appels d'Offres")
                liste_complete = gr.Dataframe(label="Tous les appels d'offres")
                
                def refresh_dashboard():
                    kpi, line, pie, df, noms = create_dashboard()
                    return kpi, line, pie, df, gr.Dropdown(choices=noms)
                
                refresh_btn.click(
                    fn=refresh_dashboard,
                    outputs=[kpi_output, graph_line, graph_pie, liste_complete, appel_dropdown]
                )
                
                appel_dropdown.change(
                    fn=show_appel_details,
                    inputs=[appel_dropdown],
                    outputs=[details_info, details_table, details_graph]
                )
                
                # Initialisation au chargement
                app.load(
                    fn=refresh_dashboard,
                    outputs=[kpi_output, graph_line, graph_pie, liste_complete, appel_dropdown]
                )
            
            # TAB 3: DETAILS
            with gr.Tab("📄 Détails"):
                gr.Markdown("## Consultation détaillée d'un appel d'offres")
                
                data = load_data()
                noms = [ao["nom"] for ao in data.get("appels_offres", [])]
                
                appel_select = gr.Dropdown(
                    label="Sélectionnez un appel d'offres",
                    choices=noms,
                    interactive=True
                )
                
                with gr.Tabs():
                    with gr.Tab("❓ Questions & Réponses"):
                        questions_output = gr.Markdown()
                        
                        appel_select.change(
                            fn=show_questions_reponses,
                            inputs=[appel_select],
                            outputs=[questions_output]
                        )
                    
                    with gr.Tab("📊 Tableaux"):
                        tableaux_output = gr.Markdown()
                        
                        appel_select.change(
                            fn=show_tableaux,
                            inputs=[appel_select],
                            outputs=[tableaux_output]
                        )
                    
                    with gr.Tab("ℹ️ Informations"):
                        info_output = gr.Markdown()
                        info_table = gr.Dataframe(label="Documents détaillés")
                        
                        appel_select.change(
                            fn=show_informations,
                            inputs=[appel_select],
                            outputs=[info_output, info_table]
                        )
        
        gr.Markdown("""
        ---
        **💡 Astuce:** Utilisez les différents onglets pour naviguer dans l'application
        """)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.launch(share=False, server_name="0.0.0.0", server_port=7860)