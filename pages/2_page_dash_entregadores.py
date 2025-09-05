#importando as bibliotecas
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import folium
from haversine import haversine
import streamlit as st
import datetime
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(page_title='Dashboard Entregadores', page_icon='🛵')


#lendo o arquivo importado
df = pd.read_csv('dataset/train.csv')
df_original = df.copy()


#limpeza de dados
#1. removendo linhas vazias
columns_to_filter = ['Delivery_person_Age', 'Road_traffic_density', 'City', 'Festival', 'multiple_deliveries', 'Delivery_person_Ratings']
for col in columns_to_filter:
    df = df[df[col] != 'NaN ']

#2. convertendo a coluna Delivery_person_Age de texto para número
df['Delivery_person_Age'] = df['Delivery_person_Age'].astype(int)

#3. convertendo a coluna Delivery_person_Ratings de texto para float
df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].astype(float)

#4. convertendo a coluna Order_Date de texto para data
df['Order_Date'] = pd.to_datetime(df['Order_Date'], dayfirst=True, format='%d-%m-%Y')

#5. convertendo a coluna multiple_deliveries de texto para número
df['multiple_deliveries'] = df['multiple_deliveries'].astype(int)

#6. Remover espaços em branco de todas as linhas das colunas especificadas
columns_to_strip = ['ID', 'Delivery_person_ID', 'Road_traffic_density', 'Type_of_order', 'Type_of_vehicle', 'Festival', 'City']
for col in columns_to_strip:
    df.loc[:, col] = df.loc[:, col].str.strip()

#7. resetar os numeros de index
df = df.reset_index(drop=True)

#8. limpando a coluna de time_taken
df['Time_taken(min)'] = df['Time_taken(min)'].apply( lambda x: x.split('(min) ')[1])
df['Time_taken(min)'] = df['Time_taken(min)'].astype(int)


# ===================================================
# Layout Sidebar
# ===================================================

image_path = 'images/logo_curry_company.png' 
image = Image.open(image_path)
st.sidebar.image(image, width=210)

st.sidebar.markdown('''---''')

st.sidebar.markdown('## Selecione um filtro de datas de entrega')

min_date = pd.to_datetime(df['Order_Date'].min()).to_pydatetime()
max_date = pd.to_datetime(df['Order_Date'].max()).to_pydatetime()

date_slider = st.sidebar.slider(
    "Intervalo de datas",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="DD/MM/YYYY",
    label_visibility='visible'
)

st.sidebar.markdown('''---''')

st.sidebar.markdown('## Selecione um filtro de tipos de tráfego')

traffic_options = st.sidebar.multiselect(
    'Condições de tráfego',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam']
)

st.sidebar.markdown('''---''')

st.sidebar.markdown('## Selecione um filtro de clima')
weather_options = st.sidebar.multiselect(
    'Condições de clima',
    ['conditions Sunny', 'conditions Fog', 'conditions Cloudy', 'conditions Windy', 'conditions Stormy', 'conditions Sandstorms'],
    default=['conditions Sunny', 'conditions Fog', 'conditions Cloudy', 'conditions Windy', 'conditions Stormy', 'conditions Sandstorms']
)

st.sidebar.markdown('''---''')

st.sidebar.markdown('### Desenvolvido por [Matheus Melo](https://www.linkedin.com/in/matheus-melo-borges/)')

#Filtro de data
min_date, max_date = date_slider
df_filtrado = (df['Order_Date'] >= min_date) & (df['Order_Date'] <= max_date)
df = df.loc[df_filtrado, :]

#Filtro de trânsito
df_filtrado = df['Road_traffic_density'].isin(traffic_options)
df = df.loc[df_filtrado, :]

#Filtro de trânsito
df_filtrado = df['Weatherconditions'].isin(weather_options)
df = df.loc[df_filtrado, :]

# ===================================================
# Layout no Streamlit
# ===================================================

st.set_page_config(layout='wide')

st.header('Marketplace - Relatório de Entregadores')

with st.container():
    st.markdown('''---''')
    st.subheader('Métricas gerais')
    col1, col2, col3, col4 = st.columns(4, gap='medium')
        
    with col1:
        idade_entregadores_max = df.loc[:,'Delivery_person_Age'].max()
        col1.metric('Maior idade de entregador:', idade_entregadores_max, border=True)
    
    with col2:
        idade_entregadores_min = df.loc[:,'Delivery_person_Age'].min()
        col2.metric('Menor idade de entregador:', idade_entregadores_min, border=True)
    
    with col3:
        condicao_veiculo_max = df.loc[:,'Vehicle_condition'].max()
        col3.metric('Melhor condição de veículo:', condicao_veiculo_max, border=True)
    
    with col4:
        condicao_veiculo_min = df.loc[:,'Vehicle_condition'].min()
        col4.metric('Pior condição de veículo:', condicao_veiculo_min, border=True)


with st.container():
    st.markdown('''---''')
    st.subheader('Avaliações')
    col1, col2 = st.columns(2, gap='large')

    with col1:
        st.markdown('Avaliação média por entregador')
        df_avaliacao_media_entregador = (
            df.loc[:, ["Delivery_person_ID", "Delivery_person_Ratings"]]
            .groupby(["Delivery_person_ID"])
            .mean()
            .sort_values(by="Delivery_person_Ratings", ascending=False)
            .reset_index()
        )
        df_avaliacao_media_entregador.columns = ['ID Entregador','Média Avaliação Entregador']
        st.dataframe(df_avaliacao_media_entregador, height=555) #ajuste de altura da tabela para ficar harmonioso com as tabelas da direita
    
    with col2:
        st.markdown('Avaliação média e desvio padrão por tipo de tráfego')
        df_geral_rating_trafego = (
            df.loc[:,['Road_traffic_density', 'Delivery_person_Ratings']]
                .groupby(['Road_traffic_density'])
                .agg({'Delivery_person_Ratings': ['mean','std']})
        )
        df_geral_rating_trafego.columns = ['Delivery_person_Ratings_mean','Delivery_person_Ratings_std']
        df_geral_rating_trafego = df_geral_rating_trafego.reset_index()
        df_geral_rating_trafego = (
            df_geral_rating_trafego
                .sort_values(by='Delivery_person_Ratings_mean', ascending=False)
                .reset_index(drop=True)
        )
        df_geral_rating_trafego.columns = ['Intensidade de Téfaego','Média Avaliação Entregador','Desvio Padrão Avaliação Entregador']
        st.dataframe(df_geral_rating_trafego)

        st.markdown('''---''')

        st.markdown('Avaliação média e desvio padrão por tipo de clima')
        df_geral_rating_clima = (
            df.loc[:,['Weatherconditions', 'Delivery_person_Ratings']]
                .groupby(['Weatherconditions'])
                .agg({'Delivery_person_Ratings': ['mean','std']})
        )
        df_geral_rating_clima.columns = ['Delivery_person_Ratings_mean','Delivery_person_Ratings_std']
        df_geral_rating_clima = df_geral_rating_clima.reset_index()

        df_geral_rating_clima = (
            df_geral_rating_clima
                .sort_values(by='Delivery_person_Ratings_mean', ascending=False)
        )
        df_geral_rating_clima.columns = ['Condições Climática','Média Avaliação Entregador','Desvio Padrão Avaliação Entregador']
        st.dataframe(df_geral_rating_clima)

#colocar essas 2 numa funcao só
with st.container():
    st.markdown('''---''')
    st.subheader('Velocidade de entrega')
    col1, col2 = st.columns(2, gap='large')

    with col1:
        st.markdown('Top 10 entregadores mais rápidos')
        df_top10_entregador_rapido = (
            df.loc[:,['Delivery_person_ID','City','Time_taken(min)']]
                .groupby(['City'])['Time_taken(min)']
                .nsmallest(10)
                .reset_index()
        )
        df_top10_entregador_rapido = df_top10_entregador_rapido.reset_index(drop=True)
        df_top10_entregador_rapido['Delivery_person_ID'] = df.loc[df_top10_entregador_rapido['level_1'],'Delivery_person_ID'].astype(str).tolist()
        df_top10_entregador_rapido = df_top10_entregador_rapido.drop('level_1', axis=1)
        df_top10_entregador_rapido.columns = ['Tipo de Cidade','Tempo de Entrega (min)','ID Entregador']
        st.dataframe(df_top10_entregador_rapido)
    
    with col2:
        st.markdown('Top 10 entregadores mais lentos')
        df_top10_entregador_lento = (
            df.loc[:,['Delivery_person_ID','City','Time_taken(min)']]
                .groupby(['City'])['Time_taken(min)']
                .nlargest(10)
                .reset_index()
        )

        df_top10_entregador_lento = df_top10_entregador_lento.reset_index(drop=True)
        df_top10_entregador_lento['Delivery_person_ID'] = df.loc[df_top10_entregador_lento['level_1'],'Delivery_person_ID'].astype(str).tolist()
        df_top10_entregador_lento = df_top10_entregador_lento.drop('level_1', axis=1)

        df_top10_entregador_lento.columns = ['Tipo de Cidade','Tempo de Entrega (min)','ID Entregador']
        st.dataframe(df_top10_entregador_lento)