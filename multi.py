# multi.py (ajustado)
import streamlit as st
from tela import main as tela_main
from quadro import main as quadro_main
from relatorios import main as relatorios_main
from Powerbi import main as powerbi_main  # Correção aqui: Powerbi_main para powerbi_main
from solicitacao import main as solicitacao_main

def main():
    st.sidebar.title("Navegação")
    page = st.sidebar.radio("Escolha uma página", ["Inicio", "Quadro", "Relatórios Férias", "Solicitação", "Power bi"])

    if page == "Inicio":
        tela_main()
    elif page == "Quadro":
        quadro_main()
    elif page == "Relatórios Férias":
        relatorios_main()
    elif page == "Solicitação":
        solicitacao_main()
    elif page == "Power bi":  # Correção aqui: PowerBi para Power bi
        powerbi_main()

if __name__ == "__main__":
    main()
