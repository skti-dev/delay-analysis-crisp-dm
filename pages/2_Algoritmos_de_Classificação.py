import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

st.set_page_config(page_title="Algoritmos de Classificação", layout="wide")

st.title("🤖 Algoritmos de Classificação - Previsão de Atrasos")

df = st.session_state.df

if df is not None:
    st.subheader("🔍 Pré-processamento e Preparação dos Dados")
    
    mean_delivery_time = df['Delivery_Time'].mean()
    std_delivery_time = df['Delivery_Time'].std()
    atraso = mean_delivery_time + std_delivery_time
    df['Delivery_Status'] = df['Delivery_Time'].apply(lambda x: 1 if x > atraso else 0)  # 1 = Atrasado, 0 = No Prazo
    
    with st.expander("📋 Detalhes do Pré-processamento"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Limiar de Atraso", f"{atraso:.2f} min")
        with col2:
            st.metric("Entregas Atrasadas", df['Delivery_Status'].sum())
        with col3:
            st.metric("Entregas No Prazo", len(df) - df['Delivery_Status'].sum())
        
        st.write("**Features selecionadas:** Weather, Traffic, Vehicle, Area")
        st.write("**Target:** Delivery_Status (1 = Atrasado, 0 = No Prazo)")
    
    # Preparar dados
    features = ['Weather', 'Traffic', 'Vehicle', 'Area']
    X = df[features]
    y = df['Delivery_Status']
    
    # Codificar variáveis categóricas
    le = LabelEncoder()
    for col in features:
        X[col] = le.fit_transform(X[col])
    
    # Dividir em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Algoritmos
    models = {
        'K-Nearest Neighbors (KNN)': KNeighborsClassifier(n_neighbors=5),
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Logistic Regression': LogisticRegression(random_state=42)
    }
    
    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        results[name] = {
            'Acurácia': accuracy_score(y_test, y_pred),
            'Precisão': precision_score(y_test, y_pred, zero_division=0),
            'Recall': recall_score(y_test, y_pred, zero_division=0),
            'F1-Score': f1_score(y_test, y_pred, zero_division=0)
        }
    
    # Resultados
    st.subheader("📊 Resultados dos Algoritmos")
    results_df = pd.DataFrame(results).T
    st.dataframe(results_df.style.format({'Acurácia': '{:.4f}', 'Precisão': '{:.4f}', 'Recall': '{:.4f}', 'F1-Score': '{:.4f}'}))
    
    # Melhor modelo
    best_model = results_df['Acurácia'].idxmax()
    st.success(f"**Melhor modelo:** {best_model} com acurácia de {results_df.loc[best_model, 'Acurácia']:.4f}")
    
    # Gráfico de comparação
    st.subheader("📈 Comparação de Acurácia")
    st.bar_chart(results_df['Acurácia'])
    
    # Explicações didáticas
    with st.expander("📚 Explicações dos Algoritmos"):
        st.write("**K-Nearest Neighbors (KNN):** Classifica baseado nos vizinhos mais próximos. Simples, mas pode ser lento com muitos dados.")
        st.write("**Decision Tree:** Cria uma árvore de decisões baseada em regras. Fácil de interpretar, mas pode overfit.")
        st.write("**Logistic Regression:** Modelo linear para classificação binária. Rápido e interpretável, mas assume linearidade.")
        st.write("**Métricas:** Acurácia (taxa de acertos), Precisão (verdadeiros positivos / positivos previstos), Recall (verdadeiros positivos / positivos reais), F1-Score (média harmônica de precisão e recall).")
    
else:
    st.warning("Carregue o dataset na página inicial para aplicar algoritmos de classificação.")