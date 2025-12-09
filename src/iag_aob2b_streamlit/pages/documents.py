import streamlit as st

st.title("Ajoutez les documents de vos AO ici ! 📄")

files = st.file_uploader(
    label="Ajoutez les documents de l'AO (PDF, DOCX, etc.) :",
    accept_multiple_files=True,
    type=["pdf", "docx", "txt", "doc","xlsx", "csv", "xls","ods","xlsm"])

col1, col2 = st.columns((6, 1))
AO_name = col1.text_input(
    label="Comment s'appelle l'AO associé à ces documents ?",
    placeholder="Ex : Ville de Niort")

col2.space("small")
submit = col2.button("Ajouter les documents 📂", type="primary")