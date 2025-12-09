import streamlit as st
import json
from datetime import datetime
import random
from pathlib import Path

DATA_FILE = Path("appels_offres.json")

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

def show():
    st.title("📤 Nouvel Appel d'Offres")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Informations générales")
        nom_appel = st.text_input(
            "Nom de l'appel d'offres",
            placeholder="Ex: Appel d'offres infrastructure 2024",
            help="Donnez un nom descriptif à votre appel d'offres"
        )
        
        etat = st.selectbox(
            "État de l'appel d'offres",
            ["En cours", "Traité"],
            help="Sélectionnez l'état actuel"
        )
    
    with col2:
        st.info("💡 **Conseil**\n\nChoisissez un nom clair et unique pour faciliter la recherche ultérieure.")
    
    st.markdown("---")
    st.subheader("Documents")
    
    uploaded_files = st.file_uploader(
        "Déposez vos documents",
        accept_multiple_files=True,
        type=['pdf', 'docx', 'xlsx', 'txt', 'doc', 'xls'],
        help="Formats acceptés: PDF, Word, Excel, TXT"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} document(s) chargé(s)")
        
        with st.expander("📁 Voir les documents"):
            for file in uploaded_files:
                col_a, col_b, col_c = st.columns([3, 2, 1])
                with col_a:
                    st.write(f"📄 {file.name}")
                with col_b:
                    st.write(f"{file.size / 1024:.1f} KB")
                with col_c:
                    st.write(f"✓ {file.type.split('/')[-1].upper()}")
    
    st.markdown("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    
    with col_btn1:
        submit = st.button("✅ Valider et Sauvegarder", type="primary", use_container_width=True)
    
    with col_btn2:
        cancel = st.button("❌ Annuler", use_container_width=True)
    
    if cancel:
        st.rerun()
    
    if submit:
        if not nom_appel:
            st.error("⚠️ Veuillez saisir un nom pour l'appel d'offres")
        elif not uploaded_files:
            st.error("⚠️ Veuillez déposer au moins un document")
        else:
            # Charger les données existantes
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Préparer les documents avec leurs tableaux
            documents = []
            for file in uploaded_files:
                doc_type = file.type.split('/')[-1]
                tables = generate_tables_for_document(file.name)
                documents.append({
                    "nom": file.name,
                    "type": doc_type,
                    "taille": file.size,
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
            
            st.success("✅ Appel d'offres créé avec succès!")
            st.balloons()
            
            # Afficher un résumé
            with st.expander("📋 Résumé de l'appel d'offres créé", expanded=True):
                st.write(f"**Nom:** {nom_appel}")
                st.write(f"**État:** {etat}")
                st.write(f"**Nombre de documents:** {len(documents)}")
                st.write(f"**Date de création:** {nouvel_appel['date_ajout']}")
                st.write(f"**Questions générées:** {len(nouvel_appel['questions'])}")
                
                total_tables = sum(len(doc["tableaux"]) for doc in documents)
                st.write(f"**Tableaux générés:** {total_tables}")
            
            st.info("👉 Rendez-vous sur le Tableau de Bord pour visualiser vos données")