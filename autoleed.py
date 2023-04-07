import googlemaps
import pandas as pd

# Define a sua chave de API do Google Maps
API_KEY = ''

# Define as coordenadas da região desejada (latitude e longitude)
LATITUDE = -16.65014946144163
LONGITUDE = -49.23546617004431

# Define o raio da região em metros
RAIO = 8000

# Define o tipo de local desejado
PALAVRA_CHAVE = 'despachante'

# Cria um objeto da API do Google Maps
gmaps = googlemaps.Client(key=API_KEY)

# Realiza a consulta à API do Google Places
places = gmaps.places_nearby(location=(LATITUDE, LONGITUDE), radius=RAIO, keyword=PALAVRA_CHAVE)

# Cria um DataFrame vazio para armazenar as informações dos locais
df = pd.DataFrame(columns=['codigo', 'razao_social', 'telefone_1', 'telefone_2'])

# Extrai as informações desejadas de cada local
for place in places['results']:
    name = place['name']
    place_id = place['place_id']
    
    # Faz uma solicitação adicional à API do Google Places para obter detalhes do local
    place_details = gmaps.place(place_id=place_id, fields=['formatted_phone_number'])
    
    # Verifica se o local tem número de telefone registrado
    if 'formatted_phone_number' in place_details['result']:
        phone_number = place_details['result']['formatted_phone_number']
    else:
        phone_number = 'Número de telefone não disponível'
    
    # Adiciona as informações do local ao DataFrame
    df = df._append({
        'codigo': phone_number,
        'razao_social': name,
        'telefone_1': phone_number,
        'telefone_2': ''
    }, ignore_index=True)

# Salva o DataFrame como um arquivo de planilha
df.to_excel('despachantesGoiania.xlsx', index=False)