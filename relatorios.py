import streamlit as st

def main():
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    
    # Configurações iniciais do Streamlit
    st.sidebar.image("hapvidalogo.png", width=200)
    
    # Carregar dados do Excel
    excel_path = 'Quadro_Combinado_Atualizado_Com_Anos.xlsx'
    df = pd.read_excel(excel_path)
    
    # Preparação dos dados
    df['LIMITE'] = pd.to_datetime(df['LIMITE'])
    # Adicionando a coluna de ano aos dados
    df['ANO LIMITE'] = df['LIMITE'].dt.year
    
    df['ANO LIMITE'] = df['ANO LIMITE'].fillna(0)  # Ou outra lógica de tratamento que preferir
    df['ANO LIMITE'] = df['ANO LIMITE'].astype(int)
    
    # Sidebar com filtros
    st.sidebar.header("Filtros")
    servicos = st.sidebar.multiselect("Selecione o Serviço", options=df['SERVIÇO'].unique())
    gerentes = st.sidebar.multiselect("Selecione o Gerente", options=df['GERENTE'].unique())
    meses = st.sidebar.multiselect("Selecione o Mês", options=df['MÊS LIMITE'].unique())
    turnos = st.sidebar.multiselect("Selecione o Turno", options=df['TURNO'].unique())
    
    
    anos = st.sidebar.multiselect("Selecione o Ano", options=sorted(df['ANO LIMITE'].unique()))
    
    # Função para obter detalhes dos funcionários com base na seleção de serviço e mês
    def get_employee_details(df, service, month, year):
        # Filtra os dados conforme o serviço, o mês e o ano do limite
        filtered_data = df[(df['SERVIÇO'] == service) & (df['MÊS LIMITE'] == month) & (df['ANO LIMITE'] == year)]
    
        # Converte as colunas de data para o formato datetime e remove a hora
        filtered_data['LIMITE'] = pd.to_datetime(filtered_data['LIMITE']).dt.strftime('%d/%m/%Y')
        filtered_data['INÍCIO'] = pd.to_datetime(filtered_data['INÍCIO']).dt.strftime('%d/%m/%Y')
        filtered_data['FIM'] = pd.to_datetime(filtered_data['FIM']).dt.strftime('%d/%m/%Y')
    
        # Retorna as colunas selecionadas
        return filtered_data[['NOME', 'SERVIÇO', 'GERENTE', 'LIMITE', 'INÍCIO', 'FIM','QUANTIDADE']]
    
    
    # Seletor de serviço
    selected_service = st.selectbox('Selecione o Serviço', options=df['SERVIÇO'].unique())
    
    # Seletor de mês
    selected_month = st.selectbox('Selecione o Mês', options=df['MÊS LIMITE'].unique())
    
    #SELECIONE O ANO 
    selected_year = st.selectbox('Selecione o Ano', options=df['ANO LIMITE'].unique())
    
    # Botão para exibir detalhes
    # Botão para exibir detalhes
    if st.button('Mostrar Detalhes dos Funcionários'):
        # Passando o ano selecionado como um argumento adicional para a função
        employee_details = get_employee_details(df, selected_service, selected_month, selected_year)
        st.write(employee_details)
    
    # Filtragem de dados
    filtered_df = df.copy()
    
    
    if servicos:
        filtered_df = filtered_df[filtered_df['SERVIÇO'].isin(servicos)]
    
    if anos:
        filtered_df = filtered_df[filtered_df['ANO LIMITE'].isin(anos)]
    if gerentes:
        filtered_df = filtered_df[filtered_df['GERENTE'].isin(gerentes)]
    if meses:
        filtered_df = filtered_df[filtered_df['MÊS LIMITE'].isin(meses)]
    if turnos:
        filtered_df = filtered_df[filtered_df['TURNO'].isin(turnos)]
    # Contagem de funcionários por mês de férias
    count_df = filtered_df.groupby('MÊS LIMITE', observed=True).size().reset_index(name='CONTA')
    
    # Gráfico de barras
    
    # Mapeamento dos meses para a ordenação correta
    meses_ordem = {
        'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4, 'Maio': 5, 'Junho': 6,
        'Julho': 7, 'Agosto': 8, 'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12
    }
    
    # Adicionando uma coluna temporária para ordenar
    # ... [seu código anterior até a criação do count_df] ...
    
    # Mapeamento dos meses para a ordenação correta (isso é necessário apenas uma vez)
    meses_ordem = {
        'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4, 'Maio': 5, 'Junho': 6,
        'Julho': 7, 'Agosto': 8, 'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12
    }
    
    # Adicionando uma coluna de ordem ao DataFrame agrupado
    count_df['MÊS ORDEM'] = count_df['MÊS LIMITE'].map(meses_ordem)
    
    # Ordenando o DataFrame agrupado pela coluna de ordem dos meses
    count_df.sort_values('MÊS ORDEM', inplace=True)
    
    # Criando o gráfico de barras com os meses na ordem correta
    fig = px.bar(
        count_df,
        x='MÊS LIMITE',
        y='CONTA',
        text='CONTA',
        title='Distribuição de Férias por Mês',
        category_orders={'MÊS LIMITE': ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
                                        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']}
    )
    
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)
    
    # ... [resto do seu código] ...
    
    
    # Removendo a coluna de ordem após a criação do gráfico
    # (isso será feito após a criação do gráfico no script)
    
    category_orders = {'MÊS LIMITE': ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
                                      'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']}
    
    # Agora, criamos o gráfico com os meses na ordem correta, especificando a ordem de categorias
    fig = px.bar(df, x='MÊS LIMITE', y='CONTAGEM', category_orders=category_orders) # Ajuste o nome 'CONTAGEM' conforme necessário
    
    
    
    # Ordenando o count_df pela coluna 'MÊS ORDEM' que foi adicionada para manter a ordem dos meses
    # Adicionando uma coluna temporária para ordenar
    count_df['MÊS ORDEM'] = count_df['MÊS LIMITE'].map(meses_ordem)
    
    # Ordenando o DataFrame pela nova coluna antes de criar o gráfico de pizza
    count_df.sort_values('MÊS ORDEM', inplace=True)
    
    # Agora, criamos o gráfico de pizza com os meses na ordem correta
    pie_fig = px.pie(count_df, names='MÊS LIMITE', values='CONTA', title='Distribuição de Férias por Mês')
    st.plotly_chart(pie_fig, use_container_width=True)
    
    
    
    

if __name__ == '__main__':
    main()
