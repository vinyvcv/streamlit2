import streamlit as st
from PIL import Image
import pandas as pd
import requests

def enviar_para_teams(webhook_url, mensagem):
    headers = {"Content-Type": "application/json"}
    data = {"text": mensagem}
    response = requests.post(webhook_url, json=data, headers=headers)
    return response.ok

def main():
    # Configuração da página

    # Carregar e exibir a logo
    logo_path = 'hapvidalogo.png'
    logo = Image.open(logo_path)
    st.image(logo, width=500)

    # Carregar os dados do Excel
    excel_path = 'Quadro_Combinado_Atualizado_Com_Anos.xlsx'
    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo Excel: {e}")
        st.stop()

    # Campo de busca
    busca = st.text_input("Buscar Funcionário por Nome ou Matrícula")

    # Filtrar o DataFrame com base na busca
    if busca:
        funcionarios_filtrados = df[df['NOME'].str.contains(busca, case=False, na=False) | 
                                    df['MATRICULA'].astype(str).str.contains(busca, case=False, na=False)]

        if not funcionarios_filtrados.empty:
            nome_funcionario = st.selectbox("Selecione o Funcionário", 
                                            options=funcionarios_filtrados['NOME'].unique(), 
                                            index=0)

    # Botão de resetar a aplicação
    if st.button('Resetar Aplicativo'):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

    # Exibição dos detalhes do funcionário selecionado
    if busca and nome_funcionario:
        funcionario_selecionado = funcionarios_filtrados[funcionarios_filtrados['NOME'] == nome_funcionario].iloc[0]

        # Exibir os detalhes do funcionário
        st.write(f"Matrícula: {funcionario_selecionado['MATRICULA']}")
        st.write(f"Nome: {funcionario_selecionado['NOME']}")
        st.write(f"Gerente: {funcionario_selecionado['GERENTE']}")
        st.write(f"Serviço: {funcionario_selecionado['SERVIÇO']}")
        st.write(f"Responsável: {funcionario_selecionado['RESPONSAVEL']}")
        st.write(f"Turno: {funcionario_selecionado['TURNO']}")
        st.write(f"Sede: {funcionario_selecionado['SEDE']}")
        st.write(f"Limite de Férias: {funcionario_selecionado['LIMITE'].strftime('%d/%m/%Y')}")
        st.write(f"Conta: {funcionario_selecionado['CONTA']}")
        st.write(f"Início Previsto: {funcionario_selecionado['INICIO'].strftime('%d/%m/%Y') if pd.notnull(funcionario_selecionado['INICIO']) else 'Não informado'}")
        st.write(f"Fim Previsto: {funcionario_selecionado['FIM'].strftime('%d/%m/%Y') if pd.notnull(funcionario_selecionado['FIM']) else 'Não informado'}")
        st.write(f"Quantidade: {funcionario_selecionado['QUANTIDADE']}")

    # Formulário para solicitação de mudança de férias
    if busca and nome_funcionario:
        st.header("Solicitar Mudança de Férias")

        with st.form(key='solicitacao_ferias_form'):
            data_inicio = st.date_input("Nova Data de Início")
            data_fim = st.date_input("Nova Data de Fim")
            comentarios = st.text_area("Comentários")
            submit_button = st.form_submit_button(label='Enviar Solicitação')

        if submit_button:
            mensagem = f"Solicitação de Mudança de Férias:\n- Funcionário: {nome_funcionario}\n- Nova Data de Início: {data_inicio}\n- Nova Data de Fim: {data_fim}\n- Comentários: {comentarios}"
            webhook_url = "https://hapvida.webhook.office.com/webhookb2/0e15b507-bfe6-4264-8238-e820e84d1fb9@77d68323-6f4b-460f-8aae-d32c654ec490/IncomingWebhook/b7b282a887584b4f86f3a0e30f02b839/80fcf3d1-35ef-4d11-83ac-342d18894ef7"
            if enviar_para_teams(webhook_url, mensagem):
                st.success("Sua solicitação foi enviada com sucesso para o Teams!")
            else:
                st.error("Houve um erro ao enviar a solicitação para o Teams.")

if __name__ == "__main__":
    main()
