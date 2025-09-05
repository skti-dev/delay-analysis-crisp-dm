# Previsão de Atrasos e Padrões de Entregas em Logística com CRISP-DM

Este projeto utiliza técnicas de mineração de dados e aprendizado de máquina para analisar e prever atrasos em entregas de logística, aplicando o framework CRISP-DM (Cross-Industry Standard Process for Data Mining).

## Demo
<img width="1916" height="783" alt="image" src="https://github.com/user-attachments/assets/142a70c6-fb3c-48bc-9d11-0c9d6635ed3c" />
<img width="1887" height="880" alt="image" src="https://github.com/user-attachments/assets/0258da45-9408-4381-8181-0b1a32ead9af" />
<img width="1884" height="897" alt="image" src="https://github.com/user-attachments/assets/f5f9633f-268a-4c6c-a329-5e9a6f2db958" />
<img width="1895" height="713" alt="image" src="https://github.com/user-attachments/assets/c97dcb77-ce3e-41f1-9182-fc8a3e30f491" />

## Funcionalidades

- **Análise Exploratória**: Visão geral do dataset Amazon Delivery.
- **Regras de Associação**: Cálculo de suporte, confiança e lift para identificar padrões.
- **Algoritmos de Classificação**: Comparação de KNN, Decision Tree e Logistic Regression.
- **Árvores de Decisão com CRISP-DM**: Aplicação completa do framework para modelagem preditiva.

## Pré-requisitos

- Python 3.8 ou superior
- Conta no Kaggle (para baixar o dataset)
- Bibliotecas: streamlit, pandas, kagglehub, scikit-learn, matplotlib

## Instalação

1. **Clone o repositório**.
2. **Instale as dependências**:

   ```bash
   pip install streamlit pandas kagglehub scikit-learn matplotlib
   ```

3. **Configure a API do Kaggle** :

- Acesse [Kaggle](vscode-file://vscode-app/c:/Users/User/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) e faça login.
- Vá para "Account" > "API" > "Create New API Token".
- Baixe o arquivo `kaggle.json`.
- Coloque o arquivo em `~/.kaggle/kaggle.json` (Linux/Mac) ou `C:\Users\[SeuUsuario]\.kaggle\kaggle.json` (Windows).
- Defina permissões: `chmod 600 ~/.kaggle/kaggle.json` (Linux/Mac).

## Como Usar

1. **Baixe o dataset** : Execute o script `download_dataset.py` para baixar e carregar o dataset:

```
python download_dataset.py
```

Isso baixará o dataset "Amazon Delivery" do Kaggle e exibirá uma prévia.

2. **Execute o aplicativo Streamlit** :

```
streamlit run app.py
```

Abra o navegador no endereço indicado (geralmente [http://localhost:8501](vscode-file://vscode-app/c:/Users/User/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html)) para explorar as análises.

## Estrutura do Projeto

```
.
├── app.py                          # Página principal com análise exploratória
├── download_dataset.py             # Script para baixar o dataset
├── pages/
│   ├── 1_Regras_de_Associação.py   # Análise de regras de associação
│   ├── 2_Algoritmos_de_Classificação.py  # Comparação de algoritmos de classificação
│   └── 3_Árvores_de_Decisão_CRISP-DM.py  # Árvores de decisão com CRISP-DM
└── README.md                       # Este arquivo
```

## Notas

- O limiar de atraso é definido como média dos tempos de entrega + 1 desvio padrão.
- Certifique-se de que o dataset seja carregado corretamente antes de navegar pelas páginas.
- Para dúvidas, consulte a documentação do Streamlit e Kaggle.

## Licença

Este projeto é para fins educacionais. Use sob sua responsabilidade.
