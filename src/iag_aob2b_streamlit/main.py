import streamlit as st

st.set_page_config(layout="wide")

pages = [
    st.Page("pages/menu.py", title="Menu", icon="🏠"),
    st.Page("pages/documents.py", title="Ajouter des documents", icon="📄"),
    st.Page("pages/questions.py", title="Questionner un AO", icon="❓")
]

pg = st.navigation(pages, position="top")
pg.run()