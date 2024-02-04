
import streamlit as st

# URL do Power BI
power_bi_url = 'https://app.powerbi.com/reportEmbed?reportId=2d9c682b-7788-47c5-abe5-8d176913a074&autoAuth=true&ctid=77d68323-6f4b-460f-8aae-d32c654ec490'

def main():
    st.write("# Clique no Incone Abaixo")
    
    # Exibindo a imagem maior
    st.image("print.png", width=800)  # Aumentando a largura da imagem

    # Criando um container com um link clicável para o Power BI
    with st.container():
        st.markdown(f'[Acessar o Power BI]({power_bi_url})', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
