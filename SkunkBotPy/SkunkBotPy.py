#Updated: Now parses messages from stored SQL data
import os
import secrets
import discord
import random
import time
import pandas
import openai
import re
#import pymssql #leave out unless using mysql
import pyodbc
#import requests for url text processing
import requests
import datetime as dt
import dateparser
import dateparser.search


from itertools import filterfalse
from re import X
from ctypes.wintypes import MSG
from discord.ext import commands
from dotenv import load_dotenv
from dateutil.parser import parse
from dateutil.tz import tzutc
from dateparser.search import search_dates


try:
    GHToken = ""
    #CONN = pymssql.connect(DBSERVER, DBUSER, DBPASS, DBNAME)
    #CONN = pyodbc.connect(os.getenv('SQL_CONNECTION_STRING'))
    #cursor = CONN.cursor()
except:
    print('could not establish')




load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
client = discord.Client(intents=intents)




BazLogFileURL = 'https://raw.githubusercontent.com/manuva/EQLogs/master/bzrlog_Project%20Lazarus_Bigpoppapizzaco.txt'
#bazFileContents = requests.get(BazLogFileURL)
bazSession = requests.Session()
bazFileContents = bazSession.get(BazLogFileURL)





##############
## COMMANDS ##
##############



############
## EVENTS ##
############
@client.event
async def on_ready():
    BotLoadedInfoMsg()
    
    
@client.event
async def on_message(message):
    try:
        await UserMessageReceive(message)
        
    except:
        async with message.channel.typing():
            time.sleep(secrets.choice(range(1,5))) 
            #await message.channel.send("i dono man i couldnt connect")
            print("I couldnt recognize this input i dono")
        
        

###############
## FUNCTIONS ##
###############   
##Do something on message received from user
async def UserMessageReceive(message):
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
    #only chat if instance is a DM CHANNEL initiated by the user
    if isinstance(message.channel, discord.DMChannel):
        #true if any words are from user and are in msgUserInput 
        #if message starts with a-z
        #if any (element in message.content for element in msgUserInput):
        if msgUserInput.match(message.content):
            print('new message detected')
            #store a random number 1-5
            randomNumber = secrets.choice(range(1,5))
            print('random number is ', randomNumber)
            msgCount = 0
            #number of messages based on random number
            while (msgCount < randomNumber):
                response = random.choice(skunkQuoteText)
                #indicate the bot is typing based on 1-10 seconds. somewhat more realistic
                async with message.channel.typing():
                    time.sleep(secrets.choice(range(1,5)))
                    await message.channel.send(response)
                    msgCount += 1
                    print('\n--message count is currently--', msgCount)
        elif message.content.startswith('!song'):
            async with message.channel.typing():
                songResponse = 'https://soundcloud.com/bodeche/secondtonone'
                time.sleep(secrets.choice(range(1,5)))
                await message.channel.send(songResponse)
        elif message.content.startswith('!stocks'):
            async with message.channel.typing():
                helpResponse = '$XLE $PICK $EINC $COPX $URNM'
                time.sleep(secrets.choice(range(1,5)))
                await message.channel.send(helpResponse)
        elif message.content == '!name':
            async with message.channel.typing():
                nameResponse = 'my name is skunkbot, what is yours?'
                time.sleep(3)
                await message.channel.send(nameResponse)
        #reporting sales data
        elif message.content.startswith('!allsales'):
            async with message.channel.typing():
                time.sleep(secrets.choice(range(1,5)))
                ReportAllPurchases()
        elif message.content == "!sold":
            async with message.channel.typing():
                time.sleep(secrets.choice(range(1,5)))
                soldResponse = ReportSoldLootList()
                await message.channel.send(soldResponse)
        elif message.content == "!dates":
            
            async with message.channel.typing():
                time.sleep(secrets.choice(range(1,5)))
                dateResponse = ParseWeeklySales()
                #await message.channel.send(dateResponse)
                #await message.channel.send('!dates recognized')
                print(dateResponse)
        elif message.content.startswith("!"):
            async with message.channel.typing():
                
                return
                
        elif message.content.startswith("$"):
            async with message.channel.typing():
                
                prev_line = ''
                msg = message.content.strip()
                userInput = msg.strip('$')
                
                print(userInput)
                
                
                
                for line in bazFileContents.text.splitlines():
                    
                    line = line.rstrip()
                
                    
                    if 'purchased' in line:
                        #timestamp1 = dt.datetime.strptime(line, "[%a %b %d %H:%M:%S %Y]")
                        #timestamp2 = dt.datetime.strptime(line, "[%c]")
                        #timestamp3 = search_dates(line)
                        #print(timestamp3)
                        
                        if 'browsing' in prev_line:
                            purchaseLines = prev_line + "\n" + line
                            #print(purchaseLines)
                            #timestampBrowse = search_dates(purchaseLines)
                            #print(timestampBrowse)
                            #print(timestampBrowse)
                            if userInput.capitalize() in purchaseLines:
                                print(purchaseLines)
                                await message.channel.send("``` " + purchaseLines + " ```")
                                print(userInput)
                                
                                
                                
                                
                                
                    prev_line = line
                
                
                return
        elif message.content.startswith("?"):        
            async with message.channel.typing():
                questionResponse = AnnounceNewSales(message.content.strip())
                await message.channel.send(questionResponse)        
                    
        #message received doesnt match anything!
        elif not msgUserInput.match(message.content):
            async with message.channel.typing():
                time.sleep(secrets.choice(range(1,5))) 
                await message.channel.send("i dono man")
    #otherwise, message is in a CHANNEL with a specific id
    elif isinstance(message.channel, discord.TextChannel):
        #channel validations
        if message.channel.id == 761447182183694348:
            #channel commands
            if message.content == "!allsales":
                async with message.channel.typing():
                    time.sleep(secrets.choice(range(1,5)))
                    salesResponse = ReportAllPurchases()
                    await message.channel.send(salesResponse)
            elif message.content == "!sold":
                
                
                prev_line = ''
                
                for line in bazFileContents.text.splitlines():
                    line = line.rstrip()
            
                    if ('purchased' in line and 'Aged' in line) | \
                    ('purchased' in line and 'Reinforced' in line): # or if line == 'text'
                        if 'browsing' in prev_line:
                            #print(prev_line)
                            #print(line)
                            print(prev_line + "\n" + line)
                            async with message.channel.typing():
                                await message.channel.send("```\n" + prev_line + "\n" + line + "\n```")
                            
                            
                    prev_line = line
            elif message.content.startswith('$'):
                async with message.channel.typing():

                    prev_line = ''
                    msg = message.content.strip()
                    userInput = msg.strip('$')

                    print(userInput)



                    for line in bazFileContents.text.splitlines():
                        
                        line = line.rstrip()

                        
                        if 'purchased' in line:
                            #timestamp1 = dt.datetime.strptime(line, "[%a %b %d %H:%M:%S %Y]")
                            #timestamp2 = dt.datetime.strptime(line, "[%c]")
                            #timestamp3 = search_dates(line)
                            #print(timestamp3)
                            
                            if 'browsing' in prev_line:
                                purchaseLines = prev_line + "\n" + line
                                #print(purchaseLines)
                                #timestampBrowse = search_dates(purchaseLines)
                                #print(timestampBrowse)
                                #print(timestampBrowse)
                                if userInput.capitalize() in purchaseLines:
                                    print(purchaseLines)
                                    await message.channel.send("``` " + purchaseLines + " ```")
                                    print(userInput)
                                    
                                    
                                    
                        prev_line = line


                    return
            elif message.content == "!weeklysales":
                async with message.channel.typing():
                    time.sleep(secrets.choice(range(1,5)))
                    latestResponse = ParseWeeklySales()
                    await message.channel.send(latestResponse)                  


#Displays 
def ReportSoldLootList():
    
    prev_line = ''
    
    
    for line in bazFileContents.text.splitlines():
        line = line.rstrip()

        if ('purchased' in line and 'Aged' in line) | \
        ('purchased' in line and 'Reinforced' in line): # or if line == 'text'
            if 'browsing' in prev_line:
                #print(prev_line)
                #print(line)
                print(prev_line + "\n" + line)
                print("```\n" + prev_line + "\n" + line + "\n```")
                
        prev_line = line
                        
def AnnounceNewSales(inputMessage):
    prev_line = ''
    userInput = inputMessage.strip('?')
    
    
    
    
    for line in bazFileContents.text.splitlines():
        line = line.rstrip()
        
        if 'purchased' in line:
            #timestamp1 = dt.datetime.strptime(line, "[%a %b %d %H:%M:%S %Y]")
            #timestamp2 = dt.datetime.strptime(line, "[%c]")
            #timestamp3 = search_dates(line)
            #print(timestamp3)
            
            if 'browsing' in prev_line:
                purchaseLines = prev_line + "\n" + line
                #print(purchaseLines)
                #timestampBrowse = search_dates(purchaseLines)
                #print(timestampBrowse)
                #print(timestampBrowse)
                if userInput in purchaseLines:
                    print(purchaseLines)
                    print(userInput)
                
        prev_line = line
    
    
    return

                        
def ParseWeeklySales():
    log_line = "[Sun Oct 09 06:14:26 2022] Wiladoc is browsing your wares."
    _datetimeWeekly = log_line[1:25]
    _datetime_strpWeekly = dt.datetime.strptime(_datetimeWeekly, '%a %b %d %H:%M:%S %Y')
    displayDate = _datetimeWeekly
    print(displayDate)
    #print(_datetimeWeekly)
    #print(_datetime_strpWeekly)
    return 
                                    
def ReportAllPurchases():
    AddAllPurchaseData()

def FindLinesWith2Words(file, word1, word2):
    """Print all lines in file that have both words in """
    for line in file:
        if re.search(r"\b" + word1 + r"\b", line) and \
            re.search(r"\b" + word2 + r"\b", line):
                print(line)
                
def BotLoadedInfoMsg():
    '''for guild in client.guilds:
        if guild.name == GUILD:
            break'''
    guild = discord.utils.get(client.guilds, name=GUILD)
    
    
        
    print(
        f'Bot ID: {client.user.id}, Name: {client.user.name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
        f"\n  ____  _                _    ____        _"
        f"\n / ___|| | ___   _ _ __ | | _| __ )  ___ | |_ "
        f"\n \___ \| |/ / | | | '_ \| |/ /  _ \ / _ \| __|          by [manuva]"
        f"\n  ___) |   <| |_| | | | |   <| |_) | (_) | |_ "
        f"\n |____/|_|\_\\\__,_|_| |_|_|\_\____/ \___/ \__|"
    )

def LogfileToSQL():
    
    prev_line = ''
    
    for line in bazFileContents.text.splitlines():
        line = line.rstrip()
        
        print(line)
    
    
    
    return

def FindTimestampFromLog():
    
    #this module, when provided with a text log file,
    #should output a browsing message only when new browsing has
    #been found after a certain date
    
    prev_line = ''
    timestamps = []
    
    #go through each line in baz file
    for line in bazFileContents.text.splitlines():
        line = line.rstrip() #strip whitespaces
        
        #timestamp format is as follows:
        # [Sun Oct 09 06:14:26 2022] Wiladoc is browsing your wares.
        # [Sun Oct 09 06:14:38 2022]  purchased 1 Aged Nightfall for (1000p).
        #file_dt = dt.datetime.strptime(line, '[ %a %b %m %H:%M:%S %Y ]')
        #_datetime = line[1:25]
        #file_dt = dt.datetime.strptime(_datetime, '%a %b %d %H:%M:%S %Y')
    
        #if purchased is found, get the timestamp of that line
        if 'purchased' in line and 'for' in line: # or if line == 'text'
            if 'browsing' in prev_line:
                print(prev_line)
                print(line)
                #print(file_dt)
                #print(_datetime + prev_line)
                

def AddAllPurchaseData():
    #this should strip the values out of the file and add them all up
    prev_line = ''
    
    for line in bazFileContents.text.splitlines():
        line = line.rstrip()
        if 'purchased' in line and 'for' in line:
            result = line[line.find('(')+1:line.find(')')]
            result = result.strip('p')
            print(result)
            print('\n\n ----Date last modified')
            ##find new commits
            #This program should search a github file for updates and display those updates  
            
        prev_line = line
    
    return

def LoadBazFile():
    try:
        #result = re.findall('purchased', response.text)
        #lineCount = 0
        #print(result)
        #for line in response.text.splitlines():
        #    if "purchased" in line:
        #        lineCount += 1
        #        purchased = print(line)

        #    else:
        #        print('nothing found')
        
        
        #BazLogFilePath = open('G:\D Drive\Games\Project Lazarus\Logs\bzrlog_Project Lazarus_Bigpoppapizzaco.txt')
        BazLogFileURL = 'https://raw.githubusercontent.com/manuva/EQLogs/master/bzrlog_Project%20Lazarus_Bigpoppapizzaco.txt'
        response = requests.get(BazLogFileURL)
        
        
        prev_line = ''
        
        for line in response.text.splitlines():
            line = line.rstrip()
            
            if 'purchased' in line and 'for' in line: # or if line == 'text'
                if 'browsing' in prev_line:
                    print(prev_line)
                    print(line)
             
            prev_line = line
         
           
    except:
        print('baz file parsing failed')
'''@bot.command(name='hey', help='here is a list of helpful commands')
async def skunk_message(ctx):
    skunkQuotes = [
        'i dono man',
        'why group when you can solo'
    ]
    response = random.choice(skunkQuotes)
    await ctx.send(response) 
     
bot.run(TOKEN)'''

#bot.run(TOKEN)
client.run(TOKEN)