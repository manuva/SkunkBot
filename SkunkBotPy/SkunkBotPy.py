#Updated: Now parses messages from stored SQL data
import os
import secrets
from re import X
import discord
from dotenv import load_dotenv
import random
from discord.ext import commands
import time
import pandas
import re
#import pymssql #leave out unless using mysql
import pyodbc

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
#CONN = pymssql.connect(DBSERVER, DBUSER, DBPASS, DBNAME)
CONN = pyodbc.connect(os.getenv('SQL_CONNECTION_STRING'))

cursor = CONN.cursor()





bot = commands.Bot(command_prefix="!")

client = discord.Client()

@client.event
async def on_ready():
    reportBotInfo()
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    #select sql data
    skunkQuotes = cursor.execute('SELECT quote_text FROM Quotes').fetchall()
    #make it a list. updated from static list/array
    skunkQuoteText = [row[0] for row in skunkQuotes]
    
    #can probably do this with isalpha or regex. user input 
    triggerWords = re.compile('[a-zA-Z]')
    
    #without bot prefix
    #only chat if instance is a DM channel initiated by the user
    if isinstance(message.channel, discord.DMChannel):
        #true if any words are from user and are in triggerwords 
        #if any (element in message.content for element in triggerWords):
        if triggerWords.search(message.content):
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
                    '''
            #store and make the response random
            response = random.choice(skunkQuotes)
            #indicate the bot is typing
            async with message.channel.typing():
                time.sleep(5) #implement a small delay before sending message
                await message.channel.send(response) #if all are true above, tell the user a random message
            async with message.channel.typing():
                response=random.choice(skunkQuotes)
                time.sleep(3)
                await message.channel.send(response)
            async with message.channel.typing():
                response=random.choice(skunkQuotes)
                time.sleep(3)
                await message.channel.send(response)
'''
'''
@bot.command(name='hey', help='responds with a random quote')
async def skunk_message(ctx):
    skunkQuotes = [
        'i dono man',
        'why group when you can solo'
    ]
    
    response = random.choice(skunkQuotes)
    await ctx.send(response)
 '''

    
def reportBotInfo():
    '''for guild in client.guilds:
        if guild.name == GUILD:
            break'''
    guild = discord.utils.get(client.guilds, name=GUILD)
        
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    
    

    

client.run(TOKEN)
#bot.run(TOKEN)
