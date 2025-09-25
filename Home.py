import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='Home',
    page_icon='🍛'
)

image_path = 'images/logo_curry_company.png' 
image = Image.open(image_path)
st.sidebar.image(image, width=210)

st.markdown(
    """
    ## Bem-vindos ao Dashboard da empresa Curry Company! 🍛📈
    
    ###🎮 Como Usar
    - Página Inicial: Acesse a página de boas-vindas com overview do projeto
    - Navegação: Use a sidebar para alternar entre os dashboards
    - Filtros: Aplique filtros de data, tráfego e clima conforme necessário
    - Interatividade: Explore gráficos interativos e mapas
    - Análises: Obtenha insights através das métricas e visualizações
    
    ##📊 Principais Métricas Acompanhadas
    
    ###🏢 Métricas da Empresa
    - Volume total de pedidos
    - Tendências temporais (diário/semanal)
    - Distribuição geográfica
    - Análise de tráfego urbano
    
    ###👤 Métricas dos Entregadores
    - Performance individual
    - Avaliações de qualidade
    - Eficiência de entrega
    - Análise de condições operacionais
    
    ###🍕 Métricas dos Restaurantes
    - Tempos de entrega
    - Distâncias percorridas
    - Impacto de eventos especiais
    - Análise comparativa por região
    """,
    unsafe_allow_html=True  

)
