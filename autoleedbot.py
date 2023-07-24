import telebot
import googlemaps
import pandas as pd
import time
import os

TOKEN = ''
bot = telebot.TeleBot(TOKEN)

API_KEY = ''
gmaps = googlemaps.Client(key=API_KEY)

listas_feitas = []

user_data = {}

def ask_city(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Qual cidade você está procurando?")
    bot.register_next_step_handler(msg, ask_radius)

def ask_radius(message):
    chat_id = message.chat.id
    city = message.text
    user_data[chat_id] = {"city": city}
    msg = bot.send_message(chat_id, "Qual raio em metros você deseja procurar?")
    bot.register_next_step_handler(msg, ask_segment)

def ask_segment(message):
    chat_id = message.chat.id
    radius = int(message.text)
    user_data[chat_id]["radius"] = radius
    msg = bot.send_message(chat_id, "Qual segmento você está procurando?")
    bot.register_next_step_handler(msg, ask_file_name)

def ask_file_name(message):
    chat_id = message.chat.id
    segment = message.text
    user_data[chat_id]["segment"] = segment
    msg = bot.send_message(chat_id, "Qual o nome que você gostaria de dar ao arquivo?")
    bot.register_next_step_handler(msg, search_places)

def search_places(message):
    
    chat_id = message.chat.id
    nome_arquivo = message.text + '.csv'
    cidade = user_data[chat_id]["city"]
    raio = user_data[chat_id]["radius"]
    palavra_chave = user_data[chat_id]["segment"]

    try:
        geocode_result = gmaps.geocode(cidade)
        latitude = geocode_result[0]['geometry']['location']['lat']
        longitude = geocode_result[0]['geometry']['location']['lng']
    except:
        bot.reply_to(message, "Erro ao obter a localização da cidade. Verifique se o nome da cidade está correto e tente novamente.")
        return

    df = pd.DataFrame(columns=['codigo', 'razao_social', 'telefone_1', 'telefone_2'])
    place_ids = []
    max_places = 120
    page_count = 1


    next_page_token = None
    while len(df) < max_places and page_count <= 3:
        places = gmaps.places_nearby(location=(latitude, longitude), radius=raio, keyword=palavra_chave, page_token=None if page_count == 1 else next_page_token)
        for place in places['results']:
            place_details = gmaps.place(place['place_id'])['result']
            if place_details['name'] in place_ids:
                continue
            codigo = place_details['place_id']
            razao_social = place_details['name']
            telefone_1 = place_details.get('formatted_phone_number', None)
            telefone_2 = place_details.get('international_phone_number', None)
            df.loc[len(df)] = [telefone_1, razao_social, telefone_1, telefone_2]
            place_ids.append(place_details['name'])
        page_count += 1
        if 'next_page_token' in places and page_count >= 3:
            next_page_token = places['next_page_token']
            page_count = 4
            continue
        

    if page_count > 3:
        print(page_count)
        while len(df) < max_places:
            places = gmaps.places_nearby(location=(latitude, longitude), radius=raio, keyword=palavra_chave, page_token=next_page_token)
            for place in places['results']:
                place_details = gmaps.place(place['place_id'])['result']
                if place_details['name'] in place_ids:
                    continue
                codigo = place_details['place_id']
                razao_social = place_details['name']
                telefone_1 = place_details.get('formatted_phone_number', None)
                telefone_2 = place_details.get('international_phone_number', None)
                df.loc[len(df)] = [telefone_1, razao_social, telefone_1, telefone_2]
                place_ids.append(place_details['name'])
                if len(df) >= max_places:
                    break
            if 'next_page_token' in places:
                next_page_token = places['next_page_token']
            else:
                break

    
    df.to_csv(nome_arquivo, index=False)

    
    with open(nome_arquivo, 'rb') as f:
        bot.send_document(chat_id=message.chat.id, document=f)

    # Remove o arquivo CSV
    os.remove(nome_arquivo)

@bot.message_handler(commands=['leeds'])
def start_leads(message):
    msg = bot.send_message(message.chat.id, "Vamos começar! Qual cidade você está procurando?")
    bot.register_next_step_handler(msg, ask_radius)    



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_message = (
        "Olá! Eu sou um chatbot criado com a biblioteca telebot.\n\n"
        "Você pode usar o comando /places para pesquisar locais próximos a uma determinada localização. "
        "Para usar esse comando, envie uma mensagem no formato:\n\n"
        "/places CIDADE RAIO PALAVRA_CHAVE NOME_ARQUIVO\n\n"
        "Por Exemplo:\n"
        "/places Londrina-Parana 20000 despachante despachanteChapeco\n"
        "Onde:\n"
        "- CIDADE é o local que vai ser procurado as informações, seja específico\n"
        "- RAIO é o raio da região a ser pesquisada (em metros)\n"
        "- PALAVRA_CHAVE é a palavra-chave para pesquisar (por exemplo, 'restaurantes' ou 'hotéis')\n"
        "- NOME_ARQUIVO é o nome do arquivo onde os resultados serão salvos (sem a extensão .csv)\n\n"
        "Após enviar o comando com os argumentos corretos, eu realizarei uma pesquisa de locais próximos usando a API do Google Places e enviarei os resultados para você em um arquivo do Excel."
    )
    bot.reply_to(message, welcome_message)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling(timeout=60, long_polling_timeout = 15)
