import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt

st.set_page_config(page_title="Árvores de Decisão - CRISP-DM", layout="wide")

st.title("🌳 Árvores de Decisão Aplicando CRISP-DM")

df = st.session_state.df

if df is not None:
    # Fase 1: Business Understanding
    with st.expander("1. 📋 Business Understanding"):
        st.write("**Objetivo:** Prever atrasos em entregas de logística usando árvores de decisão.")
        st.write("**Problema:** Identificar padrões em clima, tráfego, veículo e área para classificar entregas como atrasadas ou no prazo.")
        st.write("**Benefício:** Melhorar eficiência logística e reduzir custos com atrasos.")
    
    # Fase 2: Data Understanding
    with st.expander("2. 🔍 Data Understanding"):
        st.write("**Dataset:** Amazon Delivery com variáveis como Weather, Traffic, Vehicle, Area e Delivery_Time.")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total de Entregas", len(df))
            st.metric("Variáveis Categóricas", len(['Weather', 'Traffic', 'Vehicle', 'Area']))
        with col2:
            st.metric("Tempo Médio de Entrega", f"{df['Delivery_Time'].mean():.2f} min")
            st.metric("Desvio Padrão", f"{df['Delivery_Time'].std():.2f} min")
    
    # Fase 3: Data Preparation
    with st.expander("3. 🛠️ Data Preparation"):
        st.write("**Tratamento de Valores Ausentes:** Preenchendo NaNs com a moda (valor mais comum) para variáveis categóricas.")
        df['Weather'] = df['Weather'].fillna(df['Weather'].mode()[0])
        df['Traffic'] = df['Traffic'].fillna(df['Traffic'].mode()[0])
        
        delivery_time_mean = df['Delivery_Time'].mean()
        delivery_time_std = df['Delivery_Time'].std()
        atraso = delivery_time_mean + delivery_time_std
        df['Delivery_Status'] = df['Delivery_Time'].apply(lambda x: 1 if x > atraso else 0)
        
        features = ['Weather', 'Traffic', 'Vehicle', 'Area']
        X = df[features]
        y = df['Delivery_Status']
        
        le = LabelEncoder()
        for col in features:
            X[col] = le.fit_transform(X[col])
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        st.write("**Pré-processamento:** Definido limiar de atraso, codificadas variáveis categóricas, dividido em treino/teste.")
        st.metric("Limiar de Atraso", f"{atraso:.2f} min")
    
    # Fase 4: Modeling
    with st.expander("4. 🤖 Modeling"):
        model = DecisionTreeClassifier(random_state=42, max_depth=4)
        model.fit(X_train, y_train)
        st.write("**Modelo:** Decision Tree treinada com profundidade máxima de 4 para evitar overfitting.")
        st.write("**Como funciona:** Divide os dados em nós baseados em regras (e.g., se Weather = Stormy, então... ).")
    
    # Fase 5: Evaluation
    with st.expander("5. 📊 Evaluation"):
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Acurácia no Teste", f"{accuracy:.4f}")
        with col2:
            st.write("**Relatório de Classificação:**")
            st.text(classification_report(y_test, y_pred, target_names=['No Prazo', 'Atrasado']))
        
        # Visualização da árvore
        st.subheader("Visualização da Árvore de Decisão")
        fig, ax = plt.subplots(figsize=(12, 8))
        plot_tree(model, feature_names=features, class_names=['No Prazo', 'Atrasado'], filled=True, ax=ax)
        st.pyplot(fig)

    # Fase 6: Simulação
    with st.expander("6. 🚀 Simulação"):
        st.write("**Simulação:** Faça uma previsão para uma nova entrega.")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            weather = st.selectbox("Clima", df['Weather'].unique())
        with col2:
            traffic = st.selectbox("Tráfego", df['Traffic'].unique())
        with col3:
            vehicle = st.selectbox("Veículo", df['Vehicle'].unique())
        with col4:
            area = st.selectbox("Área", df['Area'].unique())
        
        if st.button("Prever"):
            input_data = pd.DataFrame([[weather, traffic, vehicle, area]], columns=features)
            for col in features:
                input_data[col] = le.fit_transform(input_data[col])
            prediction = model.predict(input_data)[0]
            result = "Atrasado" if prediction == 1 else "No Prazo"
            st.success(f"Previsão: {result}")
    
else:
    st.warning("Carregue o dataset na página inicial para aplicar árvores de decisão.")