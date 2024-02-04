import streamlit as st

def main():
    # Carregar e Exibir a Logo
    st.image("hapvidalogo.png", width=500)

    # Mensagem de Boas Vindas Alterada
    st.title("Bem-vindo ao Sistema de Gestão Hapvida!")
    st.markdown("""
        ### Acesse as ferramentas de gestão e planejamento:
        - **Planejador de Férias**: Organize suas férias anuais de forma simples e intuitiva.
        - **Quadro Funcional**: Visualize e analise o quadro completo de funcionários.
    """)

    

    # Aqui você pode adicionar mais elementos conforme necessário

if __name__ == '__main__':
    main()
