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

st.set_page_config(page_title='Dashboard Restaurantes', page_icon='🍴')

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

st.set_page_config(layout='wide')

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

st.sidebar.markdown('### Desenvolvido por [Matheus Melo](https://www.linkedin.com/in/matheus-melo-borges/)')

#Filtro de data
min_date, max_date = date_slider
df_filtrado = (df['Order_Date'] >= min_date) & (df['Order_Date'] <= max_date)
df = df.loc[df_filtrado, :]

#Filtro de trânsito
df_filtrado = df['Road_traffic_density'].isin(traffic_options)
df = df.loc[df_filtrado, :]

# ===================================================
# Layout no Streamlit
# ===================================================

st.set_page_config(layout='wide')

st.header('Marketplace - Relatório de Restaurantes')

with st.container():
    st.markdown('''---''')
    st.subheader('Métricas gerais')
    col1, col2, col3, col4, col5, col6 = st.columns(6, gap='small')
        
    with col1:
        entregadores_unicos = df['Delivery_person_ID'].nunique()
        col1.metric(
            'Quantidade de entregadores:',
            entregadores_unicos,
            border=True
        )
    
    with col2:
        df['Distance'] = df.apply(
            lambda x: haversine(
                (x['Restaurant_latitude'], x['Restaurant_longitude']),
                (x['Delivery_location_latitude'], x['Delivery_location_longitude'])
            ),
            axis=1
        )
        distancia_media = df['Distance'].mean().round(1)
        col2.metric(
            'Distância média delivery (km):',
            distancia_media,
            border=True
        )
    #colocar essas 4 colunas na mesma funcao
    with col3:
        df_tempo_medio_festivais = (
            df.loc[:,['Festival', 'Time_taken(min)']]
                .groupby(['Festival'])
                .agg({'Time_taken(min)':['mean','std']})
                .reset_index()
        )
        df_tempo_medio_festivais.columns = ['Festival', 'Time_taken(min)_mean', 'Time_taken(min)_std']
        df_tempo_medio_festivais = (
            df_tempo_medio_festivais
                .loc[df_tempo_medio_festivais['Festival'] == 'Yes', :]
        )
        col3.metric(
            'Entrega - dias festivos (min):',
            df_tempo_medio_festivais['Time_taken(min)_mean'].round(1),
            border=True
        )
    
    with col4:
        df_tempo_medio_festivais = (
            df.loc[:,['Festival', 'Time_taken(min)']]
                .groupby(['Festival'])
                .agg({'Time_taken(min)':['mean','std']})
                .reset_index()
        )
        df_tempo_medio_festivais.columns = ['Festival', 'Time_taken(min)_mean', 'Time_taken(min)_std']
        df_tempo_medio_festivais = (
            df_tempo_medio_festivais
                .loc[df_tempo_medio_festivais['Festival'] == 'Yes', :]
        )
        col4.metric(
            'Desvio - dias festivos (± min):',
            df_tempo_medio_festivais['Time_taken(min)_std'].round(1),
            border=True
        )
    
    with col5:
        df_tempo_medio_festivais = (
            df.loc[:,['Festival', 'Time_taken(min)']]
                .groupby(['Festival'])
                .agg({'Time_taken(min)':['mean','std']})
                .reset_index()
        )
        df_tempo_medio_festivais.columns = ['Festival', 'Time_taken(min)_mean', 'Time_taken(min)_std']
        df_tempo_medio_festivais = (
            df_tempo_medio_festivais
                .loc[df_tempo_medio_festivais['Festival'] == 'No', :]
        )
        col5.metric(
            'Entrega - dias não festivos (min):',
            df_tempo_medio_festivais['Time_taken(min)_mean'].round(1),
            border=True
        )
    
    with col6:
        df_tempo_medio_festivais = (
            df.loc[:,['Festival', 'Time_taken(min)']]
                .groupby(['Festival'])
                .agg({'Time_taken(min)':['mean','std']})
                .reset_index()
        )
        df_tempo_medio_festivais.columns = ['Festival', 'Time_taken(min)_mean', 'Time_taken(min)_std']
        df_tempo_medio_festivais = (
            df_tempo_medio_festivais
                .loc[df_tempo_medio_festivais['Festival'] == 'No', :]
        )
        col6.metric(
            'Desvio - dias não festivos (± min):',
            df_tempo_medio_festivais['Time_taken(min)_std'].round(1),
            border=True
        )

with st.container():
    st.markdown('''---''')
    col1, col2 = st.columns(2, gap='large')

    with col1:
        #gráfico de barras - distância média por cidade
        df['Distance'] = df.apply(
            lambda x: haversine(
                (x['Restaurant_latitude'], x['Restaurant_longitude']),
                (x['Delivery_location_latitude'], x['Delivery_location_longitude'])
            ),
            axis=1
        )
        distancia_media_cidade = (
            df.loc[:,['City','Distance']]
            .groupby('City')
            .mean()
            .round(1)
            .reset_index()  
        )
        fig = px.bar(
            distancia_media_cidade,
            x='City',
            y='Distance',
            title='Distância Média das Entregas por Tipo de Cidade',
            labels={
                'City':'Tipo de Cidade',
                'Distance':'Distância Média (km)'
            },
            text='Distance',
            width=800,
            height=500
        )
        fig.update_traces(
            marker_color='#4e62a5',
            texttemplate='%{text:.1f}',
            textposition='outside'
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('''---''')
        #gráfico sunburst - tempo médio de entrega por cidade e tipo de trânsito
        df_tempo_medio_entrega_por_cidade_trafego = (
            df.loc[:,['City', 'Road_traffic_density', 'Time_taken(min)']]
                .groupby(['City', 'Road_traffic_density'])
                .agg({'Time_taken(min)':['mean','std']})
                .reset_index()
        )
        df_tempo_medio_entrega_por_cidade_trafego.columns = ['City', 'Road_traffic_density', 'Time_taken(min)_mean', 'Time_taken(min)_std']
        fig = px.sunburst(
            df_tempo_medio_entrega_por_cidade_trafego,
            path=['City', 'Road_traffic_density'],
            values='Time_taken(min)_mean',
            color='Time_taken(min)_std',
            color_continuous_scale='temps',
            title='Tempo Médio de Entrega por Tipo de Cidade e Tipo de Trânsito',
            width=800,
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

    
    with col2:
        #gráfico de barras - tempo médio de entrega por cidade
        df_tempo_medio_entrega_por_cidade = (
            df.loc[:, ['City', 'Time_taken(min)']]
                .groupby(['City'])
                .agg({'Time_taken(min)': ['mean', 'std']})
                .reset_index()
        )
        df_tempo_medio_entrega_por_cidade = (
            df_tempo_medio_entrega_por_cidade
                .reset_index(drop=True)
        )
        df_tempo_medio_entrega_por_cidade.columns = ['City', 'Time_taken(min)_mean', 'Time_taken(min)_std']
        fig = px.bar(
            df_tempo_medio_entrega_por_cidade,
            x='City',
            y='Time_taken(min)_mean',
            error_y='Time_taken(min)_std',
            title='Tempo Médio de Entrega por Tipo de Cidade',
            labels={
                'City':'Tipo de Cidade',
                'Time_taken(min)_mean':'Tempo Médio de Entrega (min)',
                'Time_taken(min)_std':'Desvio Padrão do Tempo de Entrega (min)'
            },
            text='Time_taken(min)_mean',
            width=800,
            height=500
        )
        fig.update_traces(
            marker_color="#ac5c5c",
            texttemplate='%{text:.1f}',
            textposition='auto'
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('''---''')
        #tabela
        df_tempo_medio_entrega_por_cidade_pedido = (
            df.loc[:,['City', 'Type_of_order', 'Time_taken(min)']]
                .groupby(['City', 'Type_of_order'])
                .agg({'Time_taken(min)':['mean','std']})
                .reset_index()
        )
        df_tempo_medio_entrega_por_cidade_pedido = (
            df_tempo_medio_entrega_por_cidade_pedido
                .reset_index(drop=True)
        )
        df_tempo_medio_entrega_por_cidade_pedido.columns = ['Cidade', 'Tipo de Pedido', 'Tempo médio entrega (min)', 'Desvio padrão entrega (min)']
        df_tempo_medio_entrega_por_cidade_pedido = df_tempo_medio_entrega_por_cidade_pedido.round(1)
        st.dataframe(df_tempo_medio_entrega_por_cidade_pedido, height=458)