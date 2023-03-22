import disnake
from disnake.ext import commands
from disnake.flags import Intents
from disnake import Interaction
import asyncio

import time
from time import sleep
import datetime

client = commands.Bot(command_prefix='/', intents=Intents.all())

@client.slash_command(name="cadastro", description='Criar, Editar ou Excluir o Cadastro')
async def cadastro(inter):
    
    
@client.slash_command(name="teste", description='testando slash UHUHUUUU!!')
async def teste(inter):

    def text():
        print(f"ID = {inter.user.id}\n")
        print(f"User: {inter.user}\n")

        com_fun = {'/cadastro': 'Criar, Editar ou Excluir o Cadastro', '/comandos': 'Comandos Disponíveis e suas Funções', '/ajuda': 'Solicita ajuda para um Administrador do Pondu', '/taf': 'Mostra Tarefas Pendentes', '/tottaf': ' Mostra Total de Tarefas'}

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

        return text

    await inter.response.send_message(text())


@client.event
async def on_ready():
    print(f'Conectado como \"{client.guilds[0]}\"!')

client.run('MTA2NzU0MTUzNDQxMDU1OTU2MA.GQw7HV.i0F-dH2dMoN9MRKlgNfMAeaWa_dQDsW3vJoBbI')
