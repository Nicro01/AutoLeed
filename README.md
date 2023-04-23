
# AutoLeed

Este é um projeto que utiliza as bibliotecas telebot e googlemaps para permitir que os usuários pesquisem locais próximos a uma determinada localização. O bot solicita ao usuário a cidade desejada, o raio de pesquisa e o segmento que está sendo procurado. Ele então usa a API do Google Maps para encontrar locais próximos a essa localização e cria um arquivo CSV com as informações encontradas. O arquivo é então enviado de volta ao usuário através do chatbot.


## 🔗 Link para o bot
[![telegram](https://img.shields.io/badge/telegram-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://t.me/AutoLeed_Bot)

## Tecnologias Utilizadas
- Python 3.9
- API Places do Google Maps
- Telebot
- Pandas
- Time
- Os
## Documentação do BOT

#### Comandos

```
  /leeds
```

#### Retorno do bot com as pergutas :

```
  Qual cidade você está procurando?
  Qual raio em metros você deseja procurar?
  Qual segmento você está procurando?
  Qual o nome que você gostaria de dar ao arquivo?
```

#### Responda separadamente com esses parâmetros :

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `Cidade` | `string` | **Obrigatório**. Cidade que queira localizar |


| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `Raio`      | `int` | **Obrigatório**. O Raio da pesquisa que você quer |

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `Segmento`      | `string` | **Obrigatório**. O Segmento da pesquisa que você quer |

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `NomeDoArquivo`      | `string` | **Obrigatório**. O nome do arquivo que você quer |

