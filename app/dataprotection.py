import streamlit as st
import dataprotection_translation

# Dialog definition
@st.dialog("Data Protection Declaration")
def show_data_protection_dialog(lang):
    st.markdown(dataprotection_translation.dataprotection_translations[lang])

