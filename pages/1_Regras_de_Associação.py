import streamlit as st
import pandas as pd

st.set_page_config(page_title="Regras de associação", layout="wide")

st.title("📊 Regras de Associação - Análise de Padrões de Entrega")

df = st.session_state.df

if df is not None:
    st.subheader("🔍 Aplicação de Regras de Associação")
    
    # Pré-processamento com métricas destacadas
    with st.expander("📋 Pré-processamento e Definição de Atraso"):
        delivery_time_mean = df['Delivery_Time'].mean()
        delivery_time_std = df['Delivery_Time'].std()
        atraso = delivery_time_mean + delivery_time_std
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Média do Tempo de Entrega", f"{delivery_time_mean:.2f} min")
        with col2:
            st.metric("Desvio Padrão", f"{delivery_time_std:.2f} min")
        with col3:
            st.metric("Limiar de Atraso", f"{atraso:.2f} min")
        
        st.write("**Definição:** Entregas são consideradas atrasadas se o tempo de entrega exceder a média + 1 desvio padrão.")
        df['Delivery_Status'] = df['Delivery_Time'].apply(lambda x: 'Atrasado' if x > atraso else 'No Prazo')
    
    # Condições analisadas
    bad_weather = ['Stormy', 'Sandstorms']
    bad_traffic = ['High ']
    bad_vehicle = ['bicycle ']
    
    # Cálculos detalhados em expander
    with st.expander("📊 Cálculos das Métricas"):
        stormy_atrasado = df[(df['Weather'].isin(bad_weather)) & (df['Delivery_Status'] == 'Atrasado')]
        high_traffic_atrasado = df[(df['Traffic'].isin(bad_traffic)) & (df['Delivery_Status'] == 'Atrasado')]
        bike_atrasado = df[(df['Vehicle'].isin(bad_vehicle)) & (df['Delivery_Status'] == 'Atrasado')]
        combined_condition = (df['Weather'].isin(bad_weather)) & (df['Traffic'].isin(bad_traffic))
        combined_atrasado = df[combined_condition & (df['Delivery_Status'] == 'Atrasado')]
        
        total_entregas = len(df)
        total_stormy = len(df[df['Weather'].isin(bad_weather)])
        total_high_traffic = len(df[df['Traffic'].isin(bad_traffic)])
        total_bike = len(df[df['Vehicle'].isin(bad_vehicle)])
        
        # Suporte
        st.subheader("Suporte: Frequência Conjunta")
        st.write("*Fórmula:* Suporte = (Ocorrências de X e Y juntas) / Total de entregas")
        suporte_stormy = len(stormy_atrasado) / total_entregas
        suporte_high_traffic = len(high_traffic_atrasado) / total_entregas
        suporte_bike = len(bike_atrasado) / total_entregas
        suporte_combined = len(combined_atrasado) / total_entregas
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Suporte Clima Ruim → Atraso", f"{suporte_stormy:.4f}")
            st.metric("Suporte Tráfego Alto → Atraso", f"{suporte_high_traffic:.4f}")
        with col2:
            st.metric("Suporte Bicicleta → Atraso", f"{suporte_bike:.4f}")
            st.metric("Suporte Clima + Tráfego → Atraso", f"{suporte_combined:.4f}")
        
        # Confiança
        st.subheader("Confiança: Probabilidade Condicional")
        st.write("*Fórmula:* Confiança = (Ocorrências de X e Y juntas) / Ocorrências de X")
        confiança_stormy = len(stormy_atrasado) / total_stormy if total_stormy > 0 else 0
        confiança_high_traffic = len(high_traffic_atrasado) / total_high_traffic if total_high_traffic > 0 else 0
        confiança_bike = len(bike_atrasado) / total_bike if total_bike > 0 else 0
        confiança_combined = len(combined_atrasado) / len(df[combined_condition]) if len(df[combined_condition]) > 0 else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Confiança Clima Ruim → Atraso", f"{confiança_stormy:.4f}")
            st.metric("Confiança Tráfego Alto → Atraso", f"{confiança_high_traffic:.4f}")
        with col2:
            st.metric("Confiança Bicicleta → Atraso", f"{confiança_bike:.4f}")
            st.metric("Confiança Clima + Tráfego → Atraso", f"{confiança_combined:.4f}")
        
        # Lift
        st.subheader("Lift: Força da Associação")
        st.write("*Fórmula:* Lift = Confiança / Probabilidade de Y (atraso)")
        total_atrasados = len(df[df['Delivery_Status'] == 'Atrasado'])
        probabilidade_atrasado = total_atrasados / total_entregas
        lift_stormy = confiança_stormy / probabilidade_atrasado if probabilidade_atrasado > 0 else 0
        lift_high_traffic = confiança_high_traffic / probabilidade_atrasado if probabilidade_atrasado > 0 else 0
        lift_bike = confiança_bike / probabilidade_atrasado if probabilidade_atrasado > 0 else 0
        lift_combined = confiança_combined / probabilidade_atrasado if probabilidade_atrasado > 0 else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Lift Clima Ruim → Atraso", f"{lift_stormy:.4f}")
            st.metric("Lift Tráfego Alto → Atraso", f"{lift_high_traffic:.4f}")
        with col2:
            st.metric("Lift Bicicleta → Atraso", f"{lift_bike:.4f}")
            st.metric("Lift Clima + Tráfego → Atraso", f"{lift_combined:.4f}")
    
    # Resumo com tabela
    st.subheader("📈 Resumo das Regras de Associação")
    conclusoes_df = pd.DataFrame({
        'Regra': ['Clima Ruim → Atraso', 'Tráfego Alto → Atraso', 'Bicicleta → Atraso', 'Clima + Tráfego → Atraso'],
        'Suporte': [suporte_stormy, suporte_high_traffic, suporte_bike, suporte_combined],
        'Confiança': [confiança_stormy, confiança_high_traffic, confiança_bike, confiança_combined],
        'Lift': [lift_stormy, lift_high_traffic, lift_bike, lift_combined]
    })
    st.dataframe(conclusoes_df.style.format({'Suporte': '{:.4f}', 'Confiança': '{:.4f}', 'Lift': '{:.4f}'}))
    
    # Gráficos lado a lado
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🚚 Número de Atrasos por Condição")
        atrasos_df = pd.DataFrame({
            'Condição': ['Clima Ruim', 'Tráfego Alto', 'Bicicleta', 'Clima + Tráfego'],
            'Atrasos': [len(stormy_atrasado), len(high_traffic_atrasado), len(bike_atrasado), len(combined_atrasado)]
        })
        st.bar_chart(atrasos_df.set_index('Condição'))
    
    with col2:
        st.subheader("📊 Chance de Atraso (Confiança)")
        chance_df = pd.DataFrame({
            'Condição': ['Clima Ruim', 'Tráfego Alto', 'Bicicleta', 'Clima + Tráfego'],
            'Confiança': [confiança_stormy, confiança_high_traffic, confiança_bike, confiança_combined]
        })
        st.bar_chart(chance_df.set_index('Condição'))
        st.caption("*Nota:* Bicicleta tem alta confiança (13.33%) apesar de poucos casos (15 entregas, 2 atrasadas).")
    
else:
    st.warning("Carregue o dataset na página inicial para aplicar regras de associação.")