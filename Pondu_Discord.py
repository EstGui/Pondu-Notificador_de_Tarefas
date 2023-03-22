import discord
from discord.ext import commands, tasks
from discord.flags import Intents
import asyncio

import time
from time import sleep
import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import mysql.connector


def cump():
    hr = int(time.strftime("%H", time.localtime()))
    if 5 <= hr < 12:
        cump = 'Bom dia'
    elif 12 <= hr < 18:
        cump = 'Boa tarde'
    elif 18 <= hr or hr < 5:
        cump = 'Boa noite'

    return cump

def atnd(context):
    comnd = f'update dbpondu set perfil_discord = "{context.message.author}" where id_discord = "{context.message.author.id}"'
    cursor.execute(comnd)
    conexao.commit()


conexao = mysql.connector.connect( # ---> banco de dados
    host='localhost',
    user='root',
    password='Pondu054',
    database='pondusql'
)
cursor = conexao.cursor() # ---> bando de dados

client = commands.Bot(command_prefix='!', intents=Intents.all()) # ---> discord

@tasks.loop(seconds=2, count=3)
async def reminder(context):
    hr = int(time.strftime("%H", time.localtime()))
    #channel = client.get_channel(1067537196938178614)
    await context.message.author.send(f"{cump()}")

@client.command(name="cadastro")
async def cadastro(context):
    atnd(context)
    try:
        await context.message.delete()
        channel = context.message.channel.name
        canal_restrito = ['comandos']
    except:
        await context.message.author.send(f'Comando devem ser dados no canal **#comandos**.\nVocê utilizou: **Mensagens Diretas**.')
    else:
        if channel in canal_restrito:
            await context.message.author.send(f'Você fez uma solicitação para cadastro...\n{"- "*29}')

            def check(m):
                return m.author.id == context.author.id

            while True:
                await context.author.send("Digite o **número** da sua opção...\n **1**. Fazer Cadastro\n **2**. Atualizar Dados\n **3**. Excluir Conta\n **4**. Cancelar")
                opt = await client.wait_for('message', check=check)

                if opt.content == '1':
                #fazer cadastro
                    while True:
                        await context.message.author.send('Informe seu **RA**...')

                        sleep(0.5)

                        ra = await client.wait_for('message', check=check)

                        await context.message.author.send('Informe sua **Senha**...')

                        sleep(0.5)

                        senha = await client.wait_for('message', check=check)

                        await context.message.author.send(f'RA: {ra.content}\nSenha: {senha.content}\n\nDigite \"**Confirmar**\" para confirmar os dados ou \"**Corrigir**\" para corrigi-los.')

                        sleep(0.5)

                        confirmação = await client.wait_for('message', check=check)
                        if str(confirmação.content).strip() == 'confirmar' or str(confirmação.content).strip() == "Confirmar":
                            await context.message.author.send('**Aguarde...**')

                            options = webdriver.ChromeOptions()
                            options.add_argument("--headless")
                            navegador = webdriver.Chrome(chrome_options=options)

                            navegador.get('https://unasp.instructure.com/login/canvas')

                            try:
                                navegador.find_element('xpath', '//*[@id="pseudonym_session_unique_id"]').send_keys(ra.content, Keys.TAB)
                                navegador.find_element('xpath', '//*[@id="pseudonym_session_password"]').send_keys(senha.content, Keys.ENTER)
                                sleep(0.5)
                                navegador.find_element('xpath', '/html/body/div[3]/header[2]/div[1]/ul/li[1]/button/div[1]/div/img').click()
                                sleep(0.5)
                                name = navegador.find_element('xpath', '/html/body/div[4]/span/span/div/div/div/div/div/span/div/h2').get_attribute('innerHTML')

                            except:
                                navegador.quit()
                                await context.message.author.send('Ocorreu um erro.\nVerifique seus dados ou tente novamente mais tarde.')

                            else:
                                await context.message.author.send(f'**Cadastro Finalizado**!\nSeja bem vindo(a) ao Pondu, **{name}**!')

                                nome = name.split()[0]
                                sobrenome = name.split()[len(name.split())-1]
                                PerfilDiscord = context.message.author
                                IdDiscord = context.message.author.id
                                data_cadastro = datetime.date.today()

                                comando = f'insert into dbpondu (nome_usuario, sobrenome_usuario, perfil_discord, id_discord, ra_canvas, senha_canvas, data_cadastro) values ("{nome}", "{sobrenome}", "{PerfilDiscord}", "{IdDiscord}", "{ra.content}", "{senha.content}", "{data_cadastro}")'
                                
                                cursor.execute(comando)
                                conexao.commit()

                                navegador.quit()
                            break
                    break

                elif opt.content == '2':
                #atualizar dados
                    while True:
                        await context.author.send("Digite o número da opção que deseja mudar...\n **1**. RA\n **2**. Senha\n **3**. Cancelar")
                        opc = await client.wait_for('message', check=check)

                        if opc.content == '1':
                            while True:
                                await context.message.author.send('Informe seu **novo RA**...')
                                sleep(0.5)
                                nra = await client.wait_for('message', check=check)

                                await context.message.author.send(f'RA: {nra.content}\n\nDigite \"**Confirmar**\" para confirmar ou \"**Corrigir**\" para corrigir.')
                                sleep(0.5)
                                confirmação = await client.wait_for('message', check=check)

                                if str(confirmação.content).strip() == 'confirmar' or str(confirmação.content).strip() == "Confirmar":
                                    try:
                                        comando3 = f'update dbpondu set ra_canvas = "{nra.content}" where id_discord = "{context.message.author.id}"'

                                        cursor.execute(comando3)
                                        conexao.commit()
                                    except:
                                        await context.message.author.send('Erro. Tente novamente mais tarde.')
                                    else:
                                        await context.message.author.send('RA alterado com sucesso!')
                                    break
                            break

                        elif opc.content == '2':
                            while True:
                                await context.message.author.send('Informe sua **nova senha**...')
                                sleep(0.5)
                                nsenha = await client.wait_for('message', check=check)
                                await context.message.author.send(f'RA: {nsenha.content}\n\nDigite \"**Confirmar**\" para confirmar ou \"**Corrigir**\" para corrigir.')
                                sleep(0.5)
                                confirmação = await client.wait_for('message', check=check)

                                if str(confirmação.content).strip() == 'confirmar' or str(confirmação.content).strip() == "Confirmar":
                                    try:
                                        comando4 = f'update dbpondu set senha_canvas = "{nsenha.content}" where id_discord = "{context.message.author.id}"'

                                        cursor.execute(comando4)
                                        conexao.commit()
                                    except:
                                        await context.message.author.send('Erro. Tente novamente mais tarde.')
                                    else:
                                        await context.message.author.send('Senha alterada com sucesso!')
                                    break
                            break

                        elif opc.content == '3':
                            await context.message.author.send('Comando Cancelado')
                            break

                        else:
                            await context.message.author.send('Opção Inválida')
                    break

                elif opt.content == '3':
                #excluir conta
                    while True:        
                        await context.message.author.send('Digite \"**Confirmar**\" para confirmar os dados ou \"**Cancelar**\" para cancelar a exclusão da conta.')

                        sleep(0.5)

                        confirmação = await client.wait_for('message', check=check)
                        if str(confirmação.content).strip() == 'confirmar' or str(confirmação.content).strip() == "Confirmar":
                            try:
                                comando4 = f'delete from dbpondu where id_discord = "{context.message.author.id}"'
                                cursor.execute(comando4)
                                conexao.commit()
                            except:
                                await context.message.author.send('Erro. Tente novamente mais tarde.')
                            else:
                                await context.message.author.send('**Conta Excluida**.')
                                break
                        elif str(confirmação.content).strip() == 'cancelar' or str(confirmação.content).strip() == "Cancelar":
                            await context.message.author.send('**Exclusão Cancelada**.')
                            break
                        else:
                            await context.message.author.send('**Opção Inválida**.')
                            sleep(0.5)
                    break

                elif opt.content == '4':
                #cancelar
                    await context.message.author.send('**Comando Finalizado**')
                    break

                else:
                    await context.message.author.send('Opção inválida')
                    sleep(1)
        else:
            await context.message.author.send(f'Comando devem ser dados no canal **#comandos**.\nVocê utilizou o canal: **#{channel}**.')

@client.command(name='comandos')
async def comandos(context):
    atnd(context)
    try:
        await context.message.delete()
        channel = context.message.channel.name
        canal_restrito = ['comandos']
    except:
        await context.message.author.send(f'Comando devem ser dados no canal **#comandos**.\nVocê utilizou: **Mensagens Diretas**.')
    else:
        if channel in canal_restrito:
            def check(m):
                return m.author.id == context.author.id
                
            com_fun = {'!cadastro': 'Criar, Editar ou Excluir o Cadastro', '!comandos': 'Comandos Disponíveis e suas Funções', '!ajuda': 'Solicita ajuda para um Administrador do Pondu', '!taf': 'Mostra Tarefas Pendentes', '!tottaf': ' Mostra Total de Tarefas'}

            title = '**Lista de Comandos...**'
            lines = f"\n{'- '*15}"

            text = ''
            text += title + lines
            count = 1
            for k, v in com_fun.items():
                num = f'{(35-len(v)-len(k))*2.2:.0f}'
                text += f'\n {count}. {k}'
                count += 1
            text += lines
            await context.message.author.send(text)

            while True:
                await context.message.author.send(f"\nDigite o **número** do comando para ver sua **função**, ou \"**Sair**\" para sair.")

                num = await client.wait_for('message', check=check)
                if num.content == 'Sair' or num.content == 'SAIR' or num.content == 'sair':
                    await context.message.author.send("Comando Finalizado")
                    break
                elif 0 < int(num.content) <= len(com_fun):
                    await context.message.author.send(f'**{list(com_fun.keys())[int(num.content)-1]}**  -->  {list(com_fun.values())[int(num.content)-1]}')
                else:
                    await context.message.author.send("Opção Inválida")
                sleep(2)
        else:
            await context.message.author.send(f'Comando devem ser dados no canal **#comandos**.\nVocê utilizou o canal: **#{channel}**.')

@client.command(name='ajuda')
async def help(context):
    atnd(context)
    try:
        await context.message.delete()
        channel = context.message.channel.name
        canal_restrito = ['comandos']
    except:
        await context.message.author.send(f'Comando devem ser dados no canal **#comandos**.\nVocê utilizou: **Mensagens Diretas**.')
    else:
        if channel in canal_restrito:
            mchannel = client.get_channel(1073252445133750274)
            await mchannel.send(f'@{context.message.author} solicitou ajuda.')

            await context.message.author.send('Enviamos seu pedido de ajuda aos administradores do Pondu.\nAssim que possível entraremos em contato!')
        else:
            await context.message.author.send(f'Comando devem ser dados no canal **#comandos**.\nVocê utilizou o canal: **#{channel}**.')

@client.command(name='taf')
async def taf(context):
    atnd(context)
    try:
        await context.message.delete()
        channel = context.message.channel.name
        canal_restrito = ['comandos']
    except:
        await context.message.author.send(f'Comando devem ser dados no canal **#comandos**.\nVocê utilizou: **Mensagens Diretas**.')
    else:
        if channel in canal_restrito:
            await context.message.author.send('Buscando tarefas. Aguarde... ')
            m = []
            mtp = dict()
            tp = list()

            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            navegador = webdriver.Chrome(chrome_options=options)

            comando_ra = f'select ra_canvas from dbpondu where id_discord = "{context.message.author.id}";'
            cursor.execute(comando_ra)
            resultado1 = cursor.fetchall()
            ra = resultado1[0][0]

            comando_senha = f'select senha_canvas from dbpondu where id_discord = "{context.message.author.id}";'
            cursor.execute(comando_senha)
            resultado2 = cursor.fetchall()
            senha = resultado2[0][0]

            comando_nome = f'select nome_usuario from dbpondu where id_discord = "{context.message.author.id}";'
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
        
                await context.message.author.send(f'{cump()}, **{nome}**.\n\nAs tarefas são: ')
                await context.message.author.send(txt)

            else:
                await context.message.author.send('Não há atividades pendentes!')

            navegador.quit()
        else:
            await context.message.author.send(f'Comando devem ser dados no canal **#comandos**.\nVocê utilizou o canal: **#{channel}**.')

@client.command(name='tottaf')
async def tottaf(context):
    atnd(context)
    try:
        await context.message.delete()
        channel = context.message.channel.name
        canal_restrito = ['comandos']
    except:
        await context.message.author.send(f'Comando devem ser dados no canal **#comandos**.\nVocê utilizou: **Mensagens Diretas**.')
    else:
        if channel in canal_restrito:
            await context.message.author.send('Buscando todas as tarefas. Aguarde... ')

            materias = list()
            materias_validas = list()
            tarefas = list()
            mat_taf = dict()

            # |------------------------------->> ABRIR NAVEGADOR <<-------------------------------|     *** SEGUNDO PLANO COM ROTINA ***
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            navegador = webdriver.Chrome(chrome_options=options)

            # |-------------------------------->> DADOS DE LOGIN <<-------------------------------|       *** POO E BANCO DE DADOS ***
            comando_ra = f'select ra_canvas from dbpondu where id_discord = "{context.message.author.id}";'
            cursor.execute(comando_ra)
            resultado1 = cursor.fetchall()
            ra = resultado1[0][0]

            comando_senha = f'select senha_canvas from dbpondu where id_discord = "{context.message.author.id}";'
            cursor.execute(comando_senha)
            resultado2 = cursor.fetchall()
            senha = resultado2[0][0]

            comando_nome = f'select nome_usuario from dbpondu where id_discord = "{context.message.author.id}";'
            cursor.execute(comando_nome)
            resultado3 = cursor.fetchall()
            nome = resultado3[0][0]

            # |-------------------------------->> ACESSAR CANVAS <<-------------------------------|
            navegador.get('https://unasp.instructure.com/login/canvas')
            navegador.find_element('xpath', '//*[@id="pseudonym_session_unique_id"]').send_keys(ra, Keys.TAB)
            navegador.find_element('xpath', '//*[@id="pseudonym_session_password"]').send_keys(senha, Keys.ENTER)
            sleep(0.2)

            # |---------------------------->> QUANTIDADE DE MATÉRIAS <<---------------------------|
            navegador.find_element('xpath', '/html/body/div[3]/header[2]/div[1]/ul/li[2]/a').click() # --> painel de controle
            sleep(0.3)
            navegador.find_element('xpath', '//*[@id="DashboardOptionsMenu_Container"]/span').click()
            sleep(0.2)
            navegador.find_element('xpath', '/html/body/span/span/span/span[2]/ul/li[1]/span/ul/li[1]/span/span/span[2]').click()
            sleep(0.1)

            x = 1
            while True:
                try:
                    nome_materia = navegador.find_element('xpath', f'//*[@id="DashboardCard_Container"]/div/div/div[{x}]/div/a/div/div[1]').get_attribute('title')
                except:
                    x -= 1
                    break
                else:
                    materias.append(nome_materia)
                    x += 1
            # |------------------------------>> ACESSAR MATÉRIAS <<-------------------------------|
            for cont in range(1, x+1):
                navegador.find_element('xpath', f'//*[@id="DashboardCard_Container"]/div/div/div[{cont}]/div/a/div/div[1]').click() # --> matérias
                sleep(0.4)
                cont_bot = 1
                while True:
                    try:
                        fun_bot = navegador.find_element('xpath', f'//*[@id="section-tabs"]/li[{cont_bot}]/a').get_attribute('class')
                    except:
                        cont_bot -= 1
                        break
                    else:
                        if fun_bot == 'assignments':
                            materias_validas.append(materias[cont-1])

                            # |---------------------------->> QUANTIDADE DE TAREFAS <<----------------------------|
                            try:
                                navegador.find_element('xpath', f'//*[@id="section-tabs"]/li[{cont_bot}]/a').click()
                            except:
                                navegador.find_element('xpath', '//*[@id="courseMenuToggle"]/i').click()
                                navegador.find_element('xpath', f'//*[@id="section-tabs"]/li[{cont_bot}]/a').click()

                            sleep(0.2)
                            navegador.find_element('xpath', '/html/body/div[3]/div[2]/div[2]/div[3]/div[1]/div/div[1]/div[2]/div/fieldset/span/span/span/span/span/span/span[1]/div/label/span[2]').click()
                            sleep(0.4)

                            c = 1
                            while True:
                                try:
                                    navegador.find_element('xpath', f'/html/body/div[3]/div[2]/div[2]/div[3]/div[1]/div/div[2]/ul/li/div/div[2]/ul/li[{c}]/div[1]/div/div[2]/a')
                                except:
                                    c -= 1
                                    break
                                else:
                                    c += 1

                            for taf in range(1, c+1):
                                nome_taf = navegador.find_element('xpath', f'/html/body/div[3]/div[2]/div[2]/div[3]/div[1]/div/div[2]/ul/li/div/div[2]/ul/li[{taf}]/div[1]/div/div[2]/a').get_attribute('innerHTML')
                                
                                tarefas.append(nome_taf.strip())

                            mat_taf[f'{materias[cont-1]}'] = tarefas[:]
                            tarefas.clear()
                            break

                        else:
                            cont_bot += 1

                navegador.find_element('xpath', '/html/body/div[3]/header[2]/div[1]/ul/li[2]/a').click() #voltar para painel de controle
                sleep(0.4)

            for k in list(mat_taf):
                if mat_taf[k] == []:
                    del mat_taf[k]
            txt = ""
            for k, v in mat_taf.items():
                txt += f'**{k}:**\n'
                for i, taf in enumerate(v):
                    if i == len(v)-1:
                        txt += f'\t\t- {taf}\n\n'
                    else:
                        txt += f'\t\t- {taf}\n'

            await context.message.author.send(f'{cump()}, **{nome}**.\nSegue uma lista com todas as tarefas...\n\n{txt}')
            navegador.quit()
        else:
             await context.message.author.send(f'Comando devem ser dados no canal **#comandos**.\nVocê utilizou o canal: **#{channel}**.')

@client.event
async def on_ready():
    print(f'Conectado como \"{client.guilds[0]}\"!')

@client.event
async def on_member_join(member):
    await client.get_channel(1070412395043880990).send(f'Bem Vindo(a) ao **{member.guild.name}**, {member.mention}')

client.run('MTA2NzU0MTUzNDQxMDU1OTU2MA.GQw7HV.i0F-dH2dMoN9MRKlgNfMAeaWa_dQDsW3vJoBbI')