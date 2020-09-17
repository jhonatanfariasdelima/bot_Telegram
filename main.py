# bot para telegram chamado JnBono
from googletrans import Translator
import telepot
import requests

bot = telepot.Bot("1162281441:AAEOia2PWV8ri4vZBUjmrjgaxGRiUQL38dI")
nome = '\033[1;31mJnBono\033[m'
traduzir = ''  # ativador da função de tradução
consulta_cep = ''  # ativi a função de culsulta cep
consulta_filmes = ''  # ativa a função de consulta filmes


# bot.sendMessage = enviar no telegram


def mensagens(msg):
    print(msg['from']['first_name'] + msg['from']['last_name']
          + ': ' + msg['text'])  # nome sobrenome e mensagem recebida
    main(msg)


# função de consulta de cep
def Consulta_cep(msg):
    try:
        cep = msg['text']
        id_msg = msg['chat']['id']
        request = requests.get(f"https://viacep.com.br/ws/{cep}/json/")

        print('cep: {} \nrua: {} \nbairro: {} \ncidade: {} \nestado: {}'.format(request.json()['cep'],
              request.json()['logradouro'], request.json()['bairro'], request.json()['localidade'], request.json()['uf']))

        bot.sendMessage(id_msg, 'cep: {}\nrua: {}\nbairro: {}\ncidade: {}\nestado: {}'.format(request.json()['cep'],
                request.json()['logradouro'], request.json()['bairro'], request.json()['localidade'], request.json()['uf']))
    except:
        id_msg = msg['chat']['id']
        print('aconteceu um erro')
        bot.sendMessage(id_msg, 'aconteceu um erro')

    global consulta_cep
    consulta_cep = 'não'
    menu(msg)


# função de consulta de filmes
def Consulta_filmes(msg):
    try:
        filme = msg['text']
        id_msg = msg['chat']['id']
        request = requests.get(f"http://www.omdbapi.com/?t={filme}&apikey=6620801a")

        print('Title: {}\nano: {} \ngenero: {} \ntempo de filme: {} \nPoster: {}'.format(request.json()['Title'],
              request.json()['Year'], request.json()['Genre'], request.json()['Runtime'], request.json()['Poster']))

        bot.sendMessage(id_msg, 'Title: {}\nano: {} \ngenero: {} \ntempo de filme: {} \nPoster: {}'.format(request.json()['Title'],
              request.json()['Year'], request.json()['Genre'], request.json()['Runtime'], request.json()['Poster']))
    except:
        id_msg = msg['chat']['id']
        print('aconteceu um erro')
        bot.sendMessage(id_msg, 'aconteceu um erro')

    global consulta_filmes
    consulta_filmes = 'não'
    menu(msg)


# função de tradução de palavras
def traducao(msg):
    try:
        texto = msg['text']
        id_msg = msg['chat']['id']
        translator = Translator()
        t = translator.translate(texto, dest='pt')
        print(f'entrada: {t.src} destino: {t.dest}')
        print(f'original: {t.origin} -> tradução: {t.text}')

        mensage = (f'entrada: {t.src} destino: {t.dest}\n'
                   f'original: {t.origin} -> tradução: {t.text}')
        bot.sendMessage(id_msg, mensage)

    except:
        id_msg = msg['chat']['id']
        print('aconteceu um erro')
        bot.sendMessage(id_msg, 'aconteceu um erro')

    menu(msg)
    global traduzir
    traduzir = 'não'


# adiciona comandos não reconhecidos a um txt
def comandos_nao_reconhecidos(msg):
    id_msg = msg['chat']['id']
    texto = str(msg['text'])
    nome_do_emitente = msg['from']['first_name'] + msg['from']['last_name']

    mensage = 'desculpa não entendi :(\n' \
              'vou adicionar isso ao banco de dados'
    bot.sendMessage(id_msg, mensage)
    print(nome + ': ' + mensage)
    with open('PergSemRespostas.txt', 'a') as PergSemRespostas:
        PergSemRespostas.write(nome_do_emitente + ': ' + texto + '\n')
    menu(msg)


# menu de opções
def menu(msg):
    id_msg = msg['chat']['id']
    mensage = 'atualmente minhas funções são as seguintes:\n\n' \
              '[1] tradução de palavras\n' \
              '[2] culsultar cep\n' \
              '[3] consulta filmes'
    bot.sendMessage(id_msg, mensage)
    print(nome + ': ' + mensage)


def main(msg):
    global traduzir
    global consulta_cep
    global consulta_filmes

    id_msg = msg['chat']['id']
    texto = str(msg['text'])
    saudacao = {'ola', 'olá', 'oi', 'bom dia', 'boa tarde', 'boa noite'}
    texto = texto.lower()

    if texto in saudacao:
        mensage = 'ola, como vai?\n'
        bot.sendMessage(id_msg, mensage)
        print(nome + ': ' + mensage)
        menu(msg)  # menu de opções

    elif traduzir == 'sim':
        traducao(msg)

    elif texto == '1':
        print(nome + ": digite a palavra que deseja traduzir: ")
        bot.sendMessage(id_msg, 'digite a palavra que deseja traduzir: ')
        traduzir = 'sim'

    elif texto == '2':
        print(nome + ': digite o cep que deseja consultar no formato 12345678: ')
        bot.sendMessage(id_msg, 'digite o cep que deseja consultar no formato 12345678: ')
        consulta_cep = 'sim'

    elif consulta_cep == 'sim':
        Consulta_cep(msg)

    elif texto == '3':
        print(nome + ': digite o nome do filme que você deseja consultar: ')
        bot.sendMessage(id_msg, 'digite o nome do filme que você deseja consultar: ')
        consulta_filmes = 'sim'

    elif consulta_filmes == 'sim':
        Consulta_filmes(msg)

    else:
        comandos_nao_reconhecidos(msg)


bot.message_loop(mensagens)  # procura mensagems se tiver chama a função

while True:
    pass
