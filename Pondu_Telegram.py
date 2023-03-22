import telebot

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import mysql.connector

import time
from time import sleep
import datetime

def cump():
    hr = int(time.strftime("%H", time.localtime()))
    if 5 <= hr < 12:
        cump = 'Bom dia'
    elif 12 <= hr < 18:
        cump = 'Boa tarde'
    elif 18 <= hr or hr < 5:
        cump = 'Boa noite'

    return cump

tele_key = "6050304542:AAEs2Ac7vEiMyciTEZI4DlNivzVuA6jQYh8"

bot = telebot.TeleBot(tele_key)

conexao = mysql.connector.connect( # ---> banco de dados
    host='localhost',
    user='root',
    password='Pondu054',
    database='pondusql'
)
cursor = conexao.cursor() # ---> bando de dados

@bot.message_handler(commands=["opcao1"])
def reply(mensagem):
    bot.reply_to(mensagem, 'Buscando tarefas. Aguarde...')
    m = []
    mtp = dict()
    tp = list()

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    navegador = webdriver.Chrome(chrome_options=options)

    comando_ra = f'select ra_canvas from dbpondu where nome_usuario = "{mensagem.chat.first_name}" and sobrenome_usuario = "{mensagem.chat.last_name}";'
    cursor.execute(comando_ra)
    resultado1 = cursor.fetchall()
    ra = resultado1[0][0]

    comando_senha = f'select senha_canvas from dbpondu where nome_usuario = "{mensagem.chat.first_name}" and sobrenome_usuario = "{mensagem.chat.last_name}";'
    cursor.execute(comando_senha)
    resultado2 = cursor.fetchall()
    senha = resultado2[0][0]

    comando_nome = f'select nome_usuario from dbpondu where nome_usuario = "{mensagem.chat.first_name}" and sobrenome_usuario = "{mensagem.chat.last_name}";'
    cursor.execute(comando_nome)
    resultado3 = cursor.fetchall()
    nome = resultado3[0][0]

    navegador.get('https://unasp.instructure.com/login/canvas')
    navegador.find_element('xpath', '//*[@id="pseudonym_session_unique_id"]').send_keys(ra, Keys.TAB)
    navegador.find_element('xpath', '//*[@id="pseudonym_session_password"]').send_keys(senha, Keys.ENTER)

    sleep(0.4)
    navegador.find_element('xpath', '/html/body/div[3]/header[2]/div[1]/ul/li[2]/a').click() # --> painel de controle
    sleep(0.35)
    navegador.find_element('xpath', '//*[@id="DashboardOptionsMenu_Container"]/span').click()
    sleep(0.35)
    navegador.find_element('xpath', '/html/body/span/span/span/span[2]/ul/li[1]/span/ul/li[1]/span/span/span[2]').click()
    sleep(0.35)

    try:
        a = navegador.find_element('xpath', '/html/body/div[3]/div[2]/div/div[2]/div[2]/aside/div[2]/div/span').get_attribute('innerHTML')
    except:
        qtd_taf = 0
        while True:
            try:
                mat = navegador.find_element('xpath', f'/html/body/div[3]/div[2]/div/div[2]/div[2]/aside/div[2]/div/ul/li[{qtd_taf+1}]/div/div[1]/span').get_attribute('innerHTML')
            except:
                qtd_taf -= 1
                break
            else:
                if mat not in m:
                    m.append(mat)

                qtd_taf += 1

        for i, v in enumerate(m):
            for count in range(0, qtd_taf+1):
                mat = navegador.find_element('xpath', f'/html/body/div[3]/div[2]/div/div[2]/div[2]/aside/div[2]/div/ul/li[{count+1}]/div/div[1]/span').get_attribute('innerHTML')

                if mat == v:
                    tp.append(navegador.find_element('xpath', f'/html/body/div[3]/div[2]/div/div[2]/div[2]/aside/div[2]/div/ul/li[{count+1}]/div/div[1]/div/a/span').get_attribute('innerHTML').strip())

                mtp[f'{v}'] = tp[:]
                sleep(0.2)
            tp.clear()

        txt = ''
        for k, v in mtp.items():
            if k == '':
                txt += f'***<Matéria Não Especificada>:***\n'
            else:
                txt += f'**{k}:**\n'
            for i, t in enumerate(v):
                if i+1 == len(v):
                    txt += f'\t - {t}.\n\n'
                else:
                    txt += f'\t - {t};\n'

        bot.send_message(mensagem.chat.id, f'{cump()}, **{nome}**.\n\nAs tarefas são: \n{txt}')
    else:
        bot.send_message(mensagem.chat.id, 'Não há atividades pendentes!')
    navegador.quit()

#@bot.message_handler(commands=["opcao2"])
#def reply(mensagem):
#    bot.reply_to(mensagem, "")

@bot.message_handler(commands=["opcao3"])
def reply(mensagem):
    text = """
    Escolha uma opção para continuar. (Clique no item)

     /cadastro1 --> Realizar Cadastro;
     /cadastro2 --> Atualizar Cadastro;
     /cadastro3 --> Deletar Cadastro;
     /cadastro4 --> Cancelar;
    """
    bot.send_message(mensagem.chat.id, text)
    bot.reply_to(mensagem, text)


@bot.message_handler(commands=["cadastro1"])
def cad1(mensagem):
    def regRA(mensagem):
        ra = mensagem.text
        print(ra)

    
        #while True:
    bot.send_message(mensagem.chat.id, 'Informe seu **RA**...')

    sleep(0.5)

    bot.register_next_step_handler(mensagem, regRA)
    print(ra)
#
#            bot.send_message(mensagen.chat.id, 'Informe sua **Senha**...')
#
#            sleep(0.5)
#
#            senha = await client.wait_for('message', check=check)
#
#            await context.message.author.send(f'RA: {ra.content}\nSenha: {senha.content}\n\nDigite \"**Confirmar**\" para confirmar os dados ou \"**Corrigir**\" para corrigi-los.')
#
#            sleep(0.5)
#
#            confirmação = await client.wait_for('message', check=check)
#            if str(confirmação.content).strip() == 'confirmar' or str(confirmação.content).strip() == "Confirmar":
#                await context.message.author.send('**Aguarde...**')
#
#                options = webdriver.ChromeOptions()
#                options.add_argument("--headless")
#                navegador = webdriver.Chrome(chrome_options=options)
#
#                navegador.get('https://unasp.instructure.com/login/canvas')
#
#                try:
#                    navegador.find_element('xpath', '//*[@id="pseudonym_session_unique_id"]').send_keys(ra.content, Keys.TAB)
#                    navegador.find_element('xpath', '//*[@id="pseudonym_session_password"]').send_keys(senha.content, Keys.ENTER)
#                    sleep(0.5)
#                    navegador.find_element('xpath', '/html/body/div[3]/header[2]/div[1]/ul/li[1]/button/div[1]/div/img').click()
#                    sleep(0.5)
#                    name = navegador.find_element('xpath', '/html/body/div[4]/span/span/div/div/div/div/div/span/div/h2').get_attribute('innerHTML')
#
#                except:
#                    navegador.quit()
#                    await context.message.author.send('Ocorreu um erro.\nVerifique seus dados ou tente novamente mais tarde.')
#
#                else:
#                    await context.message.author.send(f'**Cadastro Finalizado**!\nSeja bem vindo(a) ao Pondu, **{name}**!')
#
#                    nome = name.split()[0]
#                    sobrenome = name.split()[len(name.split())-1]
#                    PerfilDiscord = context.message.author
#                    IdDiscord = context.message.author.id
#                    data_cadastro = datetime.date.today()
#
#                    comando = f'insert into dbpondu (nome_usuario, sobrenome_usuario, perfil_discord, id_discord, ra_canvas, senha_canvas, data_cadastro) values ("{nome}", "{sobrenome}", "{PerfilDiscord}", "{IdDiscord}", "{ra.content}", "{senha.content}", "{data_cadastro}")'
#                    
#                    cursor.execute(comando)
#                    conexao.commit()
#
#                    navegador.quit()
#                break
#
#    def cadastro2(mensagem):
#    def cadastro3(mensagem):
#    def cadastro4(mensagem):


#@bot.message_handler(commands=["opcao4"])
#def reply(mensagem):
#    bot.reply_to(mensagem, "")

@bot.message_handler(commands=["opcao5"])
def errorbug(mensagem):
    chatid = "-1001831457784"

    def envio(mensagem):
        bot.forward_message(chatid, mensagem.chat.id, mensagem.message_id)

    bot.send_message(mensagem.chat.id, "Sua descrição será enviada para desenvolvedores do Pondu\n\nDescreva o erro ou bug...")
    bot.register_next_step_handler(mensagem, envio)

#@bot.message_handler(commands=["opcao6"])
#def reply(mensagem):


def verificar(mensagem):
    return True

@bot.message_handler(func=verificar)
def reply(mensagem):
    text = """
    Escolha uma opção para continuar. (Clique no item)

     /opcao1 --> Receber tarefas pendentes;
     /opcao2 --> Receber tarefas feitas e pendentes;
     /opcao3 --> Realizar, atualizar ou deletar cadastro;
     /opcao4 --> Solicitar ajuda;
     /opcao5 --> Reportar erro ou bug;
     /opcao6 --> Limpar chat;
    """
    bot.send_message(mensagem.chat.id, text)

bot.polling()