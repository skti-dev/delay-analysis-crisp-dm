import streamlit as st
import kagglehub
import pandas as pd
import os

st.set_page_config(page_title="Previsão de atrasos e padrões de entregas em logística com CRISP DM", layout="wide")

st.title("📊 Previsão de atrasos e padrões de entregas em logística com CRISP DM")

@st.cache_data
def load_data():
    path = kagglehub.dataset_download("sujalsuthar/amazon-delivery-dataset")
    csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
    if csv_files:
        df = pd.read_csv(os.path.join(path, csv_files[0]))
        return df, csv_files[0]
    return None, None

# Carregar dados e armazenar em session_state para acesso global
if 'df' not in st.session_state:
    df, dataset_name = load_data()
    st.session_state.df = df
    st.session_state.dataset_name = dataset_name
else:
    df = st.session_state.df
    dataset_name = st.session_state.dataset_name

if df is not None:
    st.subheader("🔍 Análise Exploratória - Visão Geral do Dataset")
    
    # Visão geral em métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Dataset", dataset_name)
        st.metric("Número de Linhas", df.shape[0])
    with col2:
        st.metric("Número de Colunas", df.shape[1])
        st.metric("Entregas Totais", df['Order_ID'].nunique())
    with col3:
        st.metric("Tempo Médio de Entrega", f"{df['Delivery_Time'].mean():.2f} min")
        st.metric("Desvio Padrão", f"{df['Delivery_Time'].std():.2f} min")
    
    st.write(f"**Colunas:** {', '.join(df.columns)}")
    
    # Valores únicos em expander
    with st.expander("📋 Valores Únicos por Categoria"):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Climas diferentes:** {df['Weather'].nunique()}")
            st.write(f"Valores: {', '.join(map(str, df['Weather'].unique()))}")
            st.write(f"**Tráfegos diferentes:** {df['Traffic'].nunique()}")
            st.write(f"Valores: {', '.join(map(str, df['Traffic'].unique()))}")
        with col2:
            st.write(f"**Tipos de veículos:** {df['Vehicle'].nunique()}")
            st.write(f"Valores: {', '.join(map(str, df['Vehicle'].unique()))}")
            st.write(f"**Áreas de entrega:** {df['Area'].nunique()}")
            st.write(f"Valores: {', '.join(map(str, df['Area'].unique()))}")
    
    # Estatísticas de entrega em expander
    with st.expander("⏱️ Estatísticas de Tempo de Entrega"):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Tempo Máximo", f"{df['Delivery_Time'].max()} min")
            st.metric("Tempo Mínimo", f"{df['Delivery_Time'].min()} min")
        with col2:
            st.metric("Tempo Médio", f"{df['Delivery_Time'].mean():.2f} min")
            st.metric("Desvio Padrão", f"{df['Delivery_Time'].std():.2f} min")
    
    # Amostra dos dados
    with st.expander("📄 Amostra dos Dados"):
        st.dataframe(df.head())
    
    # Estatísticas descritivas
    with st.expander("📊 Estatísticas Descritivas"):
        st.dataframe(df.describe())
    
    # Valores ausentes
    with st.expander("⚠️ Valores Ausentes"):
        missing = df.isnull().sum()
        st.dataframe(missing[missing > 0] if missing.sum() > 0 else pd.DataFrame({"Mensagem": ["Nenhum valor ausente encontrado!"]}))
