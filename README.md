# 🍛 Curry Company - Dashboard de Análise de Dados

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.48.1-red.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.22.0-brightgreen.svg)](https://plotly.com/)

> **Dashboard interativo para análise de dados de uma empresa fictícia de delivery de comida**

Este repositório contém um dashboard completo desenvolvido em Python com Streamlit para análise de dados operacionais da Curry Company, uma empresa fictícia de delivery de comida. O projeto oferece insights detalhados sobre performance de entregas, satisfação de clientes e métricas operacionais através de visualizações interativas.

## 📊 Acesse o Dashboard publicado
[cilque aqui](https://mmb-currycompany.streamlit.app/)

## 🎯 Sobre o Projeto

A Curry Company é uma empresa de tecnologia que desenvolveu um aplicativo conectando restaurantes, entregadores e consumidores. Este dashboard foi criado para fornecer ao CEO uma visão completa dos principais KPIs (Key Performance Indicators) de crescimento da empresa, organizados em uma ferramenta única e interativa.

### 📊 Problema de Negócio

Apesar do crescimento no número de entregas, a empresa não possuía visibilidade completa dos indicadores-chave de crescimento. O modelo de negócio Marketplace requer acompanhamento de três grupos principais:

- **👥 Empresa**: Análise de pedidos e operações gerais
- **🛵 Entregadores**: Performance e avaliações dos entregadores  
- **🏪 Restaurantes**: Métricas de tempo e distância de entrega

## 🚀 Funcionalidades

### 📈 Dashboard Empresa
- Quantidade de pedidos por dia e por semana
- Distribuição de pedidos por tipo de tráfego
- Comparação de volume de pedidos por cidade e tipo de tráfego
- Análise de pedidos por entregador por semana
- Mapa interativo com localização central por cidade e tipo de tráfego

### 🛵 Dashboard Entregadores  
- Faixa etária dos entregadores (menor e maior idade)
- Análise de condição dos veículos (melhor e pior condição)
- Avaliação média por entregador
- Avaliação média e desvio padrão por tipo de tráfego e condições climáticas
- Top 10 entregadores mais rápidos e mais lentos por cidade

### 🏪 Dashboard Restaurantes
- Quantidade de entregadores únicos
- Distância média entre restaurantes e locais de entrega
- Tempo médio e desvio padrão de entrega por cidade
- Comparação de tempos de entrega em dias festivos vs não festivos
- Análise detalhada por tipo de pedido e cidade

## 🛠️ Tecnologias Utilizadas

| tecnologia | Versão | Finalidade |
|------------|---------|------------|
| **Python** | 3.8+ | Linguagem principal |
| **Streamlit** | 1.48.1 | Framework web para dashboards |
| **Pandas** | 2.3.2 | Manipulação de dados |
| **Plotly** | 5.22.0 | Visualizações interativas |
| **Folium** | 0.20.0 | Mapas interativos |
| **Haversine** | 2.9.0 | Cálculo de distâncias geográficas |
| **Matplotlib** | 3.9.4 | Visualizações estáticas |
| **Seaborn** | 0.13.2 | Visualizações estatísticas |

## 📁 Estrutura do Projeto

```
curry_company/
│
├── 📄 Home.py                          # Página principal do dashboard
├── 📋 requirements.txt                 # Dependências do projeto
├── 📖 README.md                        # Documentação
├── 🚫 .gitignore                       # Arquivos ignorados pelo Git
│
├── 📊 pages/                           # Páginas do dashboard
│   ├── 1_page_dash_empresa.py         # Dashboard da empresa
│   ├── 2_page_dash_entregadores.py    # Dashboard dos entregadores
│   └── 3_page_dash_restaurantes.py    # Dashboard dos restaurantes
│
├── 📈 dataset/                         # Dados do projeto
│   └── train.csv                       # Dataset principal
│
└── 🖼️ images/                          # Recursos visuais
    └── logo_curry_company.png          # Logo da empresa
```

## ⚡ Como Executar

### 1️⃣ Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### 2️⃣ Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/mm-borges/curry_company.git
cd curry_company
```

2. **Crie um ambiente virtual (recomendado):**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS  
source venv/bin/activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

### 3️⃣ Executando o Dashboard

```bash
streamlit run Home.py
```

O dashboard estará disponível em: `http://localhost:8501`

## 🎮 Como Usar

1. **Página Inicial**: Acesse a página de boas-vindas com overview do projeto
2. **Navegação**: Use a sidebar para alternar entre os dashboards
3. **Filtros**: Aplique filtros de data, tráfego e clima conforme necessário
4. **Interatividade**: Explore gráficos interativos e mapas
5. **Análises**: Obtenha insights através das métricas e visualizações

## 📊 Principais Métricas Acompanhadas

### 🏢 Métricas da Empresa
- Volume total de pedidos
- Tendências temporais (diário/semanal)
- Distribuição geográfica
- Análise de tráfego urbano

### 👤 Métricas dos Entregadores
- Performance individual
- Avaliações de qualidade
- Eficiência de entrega
- Análise de condições operacionais

### 🍕 Métricas dos Restaurantes  
- Tempos de entrega
- Distâncias percorridas
- Impacto de eventos especiais
- Análise comparativa por região

## 👨‍💻 Autor

**Matheus Melo Borges**
- 🌍 [LinkedIn](https://www.linkedin.com/in/matheus-melo-borges/)
- 📧 [Email](matheusmeloborges@gmail.com)
- 😺 [GitHub](https://github.com/mm-borges)

---

## 🎯 Objetivo de Aprendizado

Este projeto foi desenvolvido como parte de um portfólio de Análise de Dados, demonstrando habilidades em:

- ✅ **Análise Exploratória de Dados (EDA)**
- ✅ **Desenvolvimento de Dashboards Interativos**  
- ✅ **Visualização de Dados**
- ✅ **Desenvolvimento Web com Python**
- ✅ **Limpeza e Tratamento de Dados**
- ✅ **Pensamento Analítico e Business Intelligence**

---

### ⭐ Este projeto foi desenvolvido para fins educacionais e de demonstração, através de exercício proposto durante curso de Análise de Dados em [Comunidade DS](https://comunidadeds.com/)
