import streamlit as st
import pandas as pd
import folium  # Mapa
from folium.plugins import MarkerCluster  # Marcadores
from streamlit_folium import st_folium

# Título e barra lateral
st.title('RIO EATS')
with st.sidebar:
    st.header('Rio Eats')
    st.write('O site que vai ajudar a achar o restaurante mais pertinho de você')
    st.caption('Criado por Luaninha, Julinha e Mary')
    st.image('rio eats.jpg')

st.write('O Rio Eats chegou para deixar mais fácil a sua escolha de restaurante na cidade maravilhosa!')

# Carregar dados diretamente do CSV limpo
data = pd.read_csv('restaurantes_final_limpo.csv')

# Criar um filtro para o tipo de culinária
opcoes_culinaria = data['CULINARIA'].unique()
culinaria_selecionada = st.multiselect('Selecione Tipos de Culinária', opcoes_culinaria, default=opcoes_culinaria[:3])

# Filtrar dados com base nos tipos de culinária selecionados
dados_filtrados = data[data['CULINARIA'].isin(culinaria_selecionada)]

# Criar mapa
m = folium.Map(location=[dados_filtrados['latitude'].mean(), dados_filtrados['longitude'].mean()], zoom_start=12)
marker_cluster = MarkerCluster().add_to(m)

# Adicionar marcadores ao mapa
for idx, row in dados_filtrados.iterrows():
    folium.Marker(location=[row['latitude'], row['longitude']],
                  popup=f"{row['NOME']} - {row['CULINARIA']}",
                  icon=folium.Icon(color="blue", icon="info-sign")).add_to(marker_cluster)

# Exibir mapa
st_folium(m, width=700, height=500)

# Exibe info dos restaurantes
for idx, row in dados_filtrados.iterrows():
    with st.expander(row['NOME']):
        st.markdown(f"**Endereço**: {row['ENDERECO']}")
