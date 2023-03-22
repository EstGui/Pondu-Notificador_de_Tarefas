import discord
from discord import app_commands

import time
from time import sleep
import datetime

id_do_servidor = 1067537196938178611 #Coloque aqui o ID do seu servidor

def cump():
    hr = int(time.strftime("%H", time.localtime()))
    if 5 <= hr < 12:
        cump = 'Bom dia'
    elif 12 <= hr < 18:
        cump = 'Boa tarde'
    elif 18 <= hr or hr < 5:
        cump = 'Boa noite'

    return cump

class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False


    async def on_ready(self):
        await self.wait_until_ready()

        if not self.synced:
            await tree.sync(guild = discord.Object(id=id_do_servidor))
            self.synced = True

        print(f"Entramos como {self.user}.")

aclient = client()
tree = app_commands.CommandTree(aclient)

@tree.command(guild = discord.Object(id=id_do_servidor), name = 'teste', description='Testando') 
async def slash0(interaction: discord.Interaction):
    await interaction.response.send_message("Estou funcionando!", ephemeral = True) 


@tree.command(guild = discord.Object(id=id_do_servidor), name = 'comandos', description='Lista de Comandos')  #cria comando
async def slash1(interaction: discord.Interaction):

    @client.event
    async def teste(interaction):
#        def check(m):
#                return  == interaction.user.id
                
        print(f"ID = {interaction.user.id}\n")
        print(f"User: {interaction.user}\n")

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
     
    await interaction.response.send_message(f"{teste(interaction)}", ephemeral = True)
                

'''while True:
        await context.message.author.send("\nDigite o **número** do comando para ver sua **função**, ou \"**Sair**\" para sair.")

        num = await client.wait_for('message', check=check)
        if num.content == 'Sair' or num.content == 'SAIR' or num.content == 'sair':
            await context.message.author.send("Comando Finalizado")
            break
        elif 0 < int(num.content) <= len(com_fun):
            await context.message.author.send(f'**{list(com_fun.keys())[int(num.content)-1]}**  -->  {list(com_fun.values())[int(num.content)-1]}')
        else:
            await context.message.author.send("Opção Inválida")
        sleep(2)'''


aclient.run('MTA2NzU0MTUzNDQxMDU1OTU2MA.GQw7HV.i0F-dH2dMoN9MRKlgNfMAeaWa_dQDsW3vJoBbI')