#Updated: Now parses messages from stored SQL data
from itertools import filterfalse
import os

import secrets
import discord
import random
import time
import pandas
import re
#import pymssql #leave out unless using mysql
import pyodbc
from re import X
from ctypes.wintypes import MSG
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
#CONN = pymssql.connect(DBSERVER, DBUSER, DBPASS, DBNAME)
CONN = pyodbc.connect(os.getenv('SQL_CONNECTION_STRING'))

cursor = CONN.cursor()
bot = commands.Bot(command_prefix="!")
client = discord.Client()






############
## EVENTS ##
############
@client.event
async def on_ready():
    reportBotInfo()
        

    
    
@client.event
async def on_message(message):
    await SendRandomQuote(message)    

###############
## FUNCTIONS ##
###############   
async def SendRandomQuote(message):
    if message.author == client.user:
        return
    
    #select sql data
    skunkQuotes = cursor.execute('SELECT quote_text FROM Quotes').fetchall()
    #make it a list. updated from static list/array
    skunkQuoteText = [row[0] for row in skunkQuotes]
    
    #can probably do this with isalpha or regex. user input 
    msgUserInput = re.compile('[a-zA-Z]')
    msgUserNumInput = re.compile('[0-9]')


    #without bot prefix
    #only chat if instance is a DM channel initiated by the user
    if isinstance(message.channel, discord.DMChannel):
        #true if any words are from user and are in msgUserInput 
        #if message starts with a-z
        #if any (element in message.content for element in msgUserInput):
        if msgUserInput.match(message.content):
            #store a random number 1-5
            randomNumber = secrets.choice(range(1, 5))
            #print('random number is ', randomNumber)
            msgCount = 0
            #number of messages based on random number
            while (msgCount < randomNumber):
                response = random.choice(skunkQuoteText)
                #indicate the bot is typing based on 1-10 seconds. somewhat more realistic
                async with message.channel.typing():
                    time.sleep(secrets.choice(range(1,10)))
                    await message.channel.send(response)
                    msgCount += 1
                    #print('\n--message count is currently', msgCount)
        elif message.content.startswith('!song'):
            async with message.channel.typing():
                songResponse = 'https://soundcloud.com/bodeche/secondtonone'
                time.sleep(secrets.choice(range(1,10)))
                await message.channel.send(songResponse)
        elif message.content.startswith('!stocks'):
            async with message.channel.typing():
                helpResponse = '$XLE $PICK $EINC $COPX $URNM'
                time.sleep(secrets.choice(range(1,10)))
                await message.channel.send(helpResponse)
        elif message.content == '!name':
            async with message.channel.typing():
                nameResponse = 'my name is skunkbot, what is yours?'
                time.sleep(3)
                await message.channel.send(nameResponse)
        elif not msgUserInput.match(message.content):
            async with message.channel.typing():
                time.sleep(secrets.choice(range(1,10))) 
                await message.channel.send("i dono man")


                    
                


                
                
                
def reportBotInfo():
    '''for guild in client.guilds:
        if guild.name == GUILD:
            break'''
    guild = discord.utils.get(client.guilds, name=GUILD)
    
    
        
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
        f"\n  ____  _                _    ____        _"
        f"\n / ___|| | ___   _ _ __ | | _| __ )  ___ | |_ "
        f"\n \___ \| |/ / | | | '_ \| |/ /  _ \ / _ \| __|          by [manuva]"
        f"\n  ___) |   <| |_| | | | |   <| |_) | (_) | |_ "
        f"\n |____/|_|\_\\\__,_|_| |_|_|\_\____/ \___/ \__|"
    )
    



'''@bot.command(name='hey', help='here is a list of helpful commands')
async def skunk_message(ctx):
    skunkQuotes = [
        'i dono man',
        'why group when you can solo'
    ]
    response = random.choice(skunkQuotes)
    await ctx.send(response) 
     
bot.run(TOKEN)'''
client.run(TOKEN)