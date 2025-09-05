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

st.set_page_config(page_title='Dashboard Empresa', page_icon='📈')

# ===================================================
# Funções
# ===================================================

def clean_code(df):
    """
    Esta função tem a responsabilidade de limpar o dataframe.
    Tipos de limpeza:
    1. Remoção dos dados NaN
    2. Mudança do tipo da coluna de dados
    3. Remoção dos espaços das variáveis de texto
    4. Formatação da coluna de datas
    5. Limpeza da coluna de tempo (remoção do texto da variável numérica)
    
    Input: Dataframe
    Output: Dataframe
    """

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

    return df


def chart_pedidos_dia (df):
    cols = ['ID', 'Order_Date']
    df_pedidos_dia = df.loc[:,cols].groupby(['Order_Date']).count().reset_index()

    fig = px.bar(df_pedidos_dia,
        x='Order_Date',
        y='ID',
        title='Número de Pedidos x Dia',
        color='ID',
        color_continuous_scale='RdYlGn',
        labels={'ID':'Contagem de Pedidos',
                'Order_Date':'Data'},
        text='ID',
        width=1600,
        height=500
    )
    return fig


def chart_pedidos_por_trafego (df):
    cols=['ID', 'Road_traffic_density']
    df_pedidos_por_trafego = (
        df.loc[:,cols]
            .groupby('Road_traffic_density')
            .count()
            .reset_index()
        )
    df_pedidos_por_trafego['perc_traffic'] = (df_pedidos_por_trafego['ID'] / df_pedidos_por_trafego['ID'].sum()) * 100

    fig=px.pie(df_pedidos_por_trafego,
        'Road_traffic_density',
        'ID',
        title='Distribuição de Pedidos por Tipo de Trânsito',
        labels={'ID':'Contagem de Pedidos',
                'Road_traffic_density':'Tipo de Trânsito'},
        hole=0.4,
        color_discrete_sequence=px.colors.diverging.Portland,
        width=800,
        height=500
    )
    return fig


def chart_volume_pedidos(df):
    cols=['ID', 'City', 'Road_traffic_density']
    df_volume_pedidos = (
        df.loc[:,cols]
            .groupby(['City', 'Road_traffic_density'])
            .count()
            .reset_index()
    )
    fig=px.scatter(df_volume_pedidos,
            x='City',
            y='Road_traffic_density',
            size='ID', color='City',
            title='Comparação do Volume de Pedidos por Cidade e Tipo de Trânsito',
            width=800,
            height=500
    )
    return fig


def chart_numero_pedidos_semana(df):
    df['Week_of_year'] = df['Order_Date'].dt.strftime('%U')
    cols = ['ID', 'Week_of_year']
    df_pedidos_semana = (
        df.loc[:,cols]
            .groupby(['Week_of_year'])
            .count()
            .reset_index()
    )
    fig = px.line(df_pedidos_semana,
        x='Week_of_year',
        y='ID',
        title='Número de Pedidos x Semana do Ano',
        labels={
            'ID':'Contagem de Pedidos',
            'Week_of_year':'Semana do Ano'
        },
        text='ID',
        width=1000,
        height=500
    )
    fig.update_traces(
        line=dict(color="#4e62a5"),
        textposition='top right'
    )
    return fig


def chart_numero_pedidos_por_entregador_semana(df):
    df_pedidos_semana = (
        df.loc[:, ["ID", "Week_of_year"]]
            .groupby(["Week_of_year"])
            .count()
            .reset_index()
    )
    df_entregadores_unicos_semana = (
        df.loc[:, ["Delivery_person_ID", "Week_of_year"]]
            .groupby(["Week_of_year"])
            .nunique()
            .reset_index()
    )
    df_aux = pd.merge(df_pedidos_semana, df_entregadores_unicos_semana, how='inner')
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    fig = px.line(
        df_aux,
        x='Week_of_year',
        y='order_by_deliver',
        title='Número de Pedidos por entregador x Semana do Ano',
        labels={
            'order_by_deliver':'Pedidos por Entregador',
            'Week_of_year':'Semana do Ano'
        },
        text='order_by_deliver',
        width=1000,
        height=500
    )
    fig.update_traces(
        line=dict(color='#ba4c4c'),
        texttemplate='%{text:.1f}',
        textposition='top right'
    )
    return fig


def map_delivery_lat_long(df):
    df_map_delivery = (
        df.loc[
            :,
            [
                "City",
                "Road_traffic_density",
                "Delivery_location_latitude",
                "Delivery_location_longitude",
            ],
        ]
        .groupby(["City", "Road_traffic_density"])
        .median()
        .reset_index()
    )
    map = folium.Map(
        location=[
            df_map_delivery['Delivery_location_latitude'].mean(),
            df_map_delivery['Delivery_location_longitude'].mean()],
            zoom_start=7
    )
    for index, location_info in df_map_delivery.iterrows():
        folium.Marker(
            [location_info['Delivery_location_latitude'],
            location_info['Delivery_location_longitude']],
            popup=location_info[['City', 'Road_traffic_density']]
    ).add_to(map)
    return map


# ===================================================
# Extração arquivo
# ===================================================

#lendo o arquivo importado
df = pd.read_csv('dataset/train.csv')
df_original = df.copy()

#limpando os dados
df = clean_code(df)

# ===================================================
# Layout Sidebar
# ===================================================

st.set_page_config(layout='wide')

st.header('Marketplace - Relatório Empresarial')

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

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        # pergunta de negócio 1 - Quantidade de pedidos por dia
        # processo: realizar a contagem de pedidos e distribuir pela varável order_date, apresentar como coluna de barras
        fig = chart_pedidos_dia(df)
        st.plotly_chart(fig, use_container_width=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            # pergunta de negócio 3 - Distribuição dos pedidos por tipo de tráfico
            # processo: realizar a contagem de pedidos e distribuir pela varável Road_traffic_density, apresentar como gráfico de pizza
            fig = chart_pedidos_por_trafego(df) 
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            # pergunta de negócio 4 - Comparação do volume de pedidos por cidade e tipo de tráfego'
            # processo: realizar a contagem de pedidos e distribuir pela varável Road_traffic_density e city, apresentar como gráfico de bolhas
            fig = chart_volume_pedidos(df)
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    with st.container():
        fig = chart_numero_pedidos_semana(df)
        st.plotly_chart(fig, use_container_width=True)
    
    with st.container():
        fig = chart_numero_pedidos_por_entregador_semana(df)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    map = map_delivery_lat_long(df)
    folium_static(map, width=1024, height=600)