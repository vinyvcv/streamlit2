import streamlit as st

def main():
    
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    
    # Configurando a página
    
    # Função para carregar os dados
    st.cache_data 
    def load_data():
        data = pd.read_excel("quadro.xlsx")
        # Convertendo todas as colunas para string para evitar problemas de serialização
        for col in data.columns:
            data[col] = data[col].astype(str)
        return data
    
    df = load_data()
    
    # Logo
    st.image("hapvidalogo.png", width=500)
    
    # Filtros
    st.sidebar.header("Filtros")
    nome = st.sidebar.text_input("Nome")
    matricula = st.sidebar.number_input("Matrícula", step=1, format="%d")
    responsavel = st.sidebar.selectbox("Responsável Direto", [''] + list(df['RESPONSAVEL DIRETO'].unique()))
    cargo = st.sidebar.selectbox("Cargo", [''] + list(df['CARGO'].unique()))
    status = st.sidebar.selectbox("Status", [''] + list(df['STATUS'].unique()))
    servico = st.sidebar.selectbox("Serviço", [''] + list(df['SERVIÇO'].unique()))
    
    # Seleção de Sede para Filtragem
    st.sidebar.header("")
    sede_selecionada = st.sidebar.selectbox("Sede", ['Todas'] + list(df['SEDE'].unique()))
    
    # Novo Filtro por Turno
    turno_selecionado = st.sidebar.selectbox("Turno", ['Todos'] + sorted(df['TURNO'].unique()))
    
    # Aplicando filtros aos dados
    mask = pd.Series([True]*len(df)) # Initialize mask to all True
    if nome:
        mask &= df['COLABORADOR (A)'].str.contains(nome, case=False, na=False)
    if matricula > 0: # Assuming matricula 0 is not used and implies 'any'
        mask &= df['MAT'] == str(matricula)
    if responsavel:
        mask &= df['RESPONSAVEL DIRETO'] == responsavel
    if cargo:
        mask &= df['CARGO'] == cargo
    if status:
        mask &= df['STATUS'] == status
    if servico:
        mask &= df['SERVIÇO'] == servico
    if sede_selecionada != 'Todas':
        mask &= df['SEDE'] == sede_selecionada
    if turno_selecionado != 'Todos':
        mask &= df['TURNO'] == turno_selecionado
    
    filtered_data = df[mask]
    
    # Exibição dos dados filtrados com tamanho aumentado
    st.dataframe(filtered_data, height=600)
    
    # Gráfico de barras para quantidade de funcionários por serviço (filtrado por sede)
    st.header("Quantidade de Funcionários por Serviço (Filtrado por Sede)")
    service_counts = filtered_data['SERVIÇO'].value_counts()
    fig_service = px.bar(service_counts, x=service_counts.index, y=service_counts.values, 
                         labels={'x':'Serviço', 'y':'Quantidade de Funcionários'})
    st.plotly_chart(fig_service, use_container_width=True)
    
    # Gráfico de pizza para distribuição de gênero (filtrado por sede)
    st.header("Distribuição de Gênero (Filtrado por Sede)")
    gender_counts = filtered_data['SEXO'].value_counts().reindex(['M', 'F'])
    fig_genero = px.pie(values=gender_counts, names=gender_counts.index, color=gender_counts.index,
                        color_discrete_map={'M':'blue', 'F':'pink'})
    st.plotly_chart(fig_genero, use_container_width=True)
    

if __name__ == '__main__':
    main()
