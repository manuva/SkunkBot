#bot.py
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

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix="!")

client = discord.Client()

@client.event
async def on_ready():
    reportBotInfo()
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    skunkQuotes = [
        'I dono man',
        'I dono man',
        'I dono man',
        'why group when you can solo',
        'yea it sucks man',
        'would you be interested in participating in a publicity stunt?',
        'i feel like thats their gimmick',
        'only regular people suffer',
        'so if you immediately go after the truth',
        'you are a suffering denier',
        'but its like im not denying the regulars/poor suffer',
        'im trying to understand why because ultimately we''re in the same position',
        'it just seems like you gotta be a sociopath to have one world government as an objective',
        'how many sociopaths can you really get on the same team at one time',
        'theres a total wine and more store',
        'yea',
        'private mega liquor store',
        'they removed all russian products from their shelves',
        'in support of ukraine',
        '..........',
        'everyones beating around the bush and then just using religion to absolve themselves of guilt and shame',
        'its weird tho',
        'and everyone was all about them cause they were high quality and rare',
        'if these satanists would just stop',
        'cause cuban cigars were banned',
        'like we could legit be living in heaven on earth',
        'which to me is the weird shit about religion',
        'theres some halve truths in there but nobody will just say it',
        'tired of the military interventionalism',
        'thats why i feel like',
        'their actions in this moment show their hand' ,
        'you think these nigs are burning zero days',
        'or using old known shit',
        'bunch of cucks working at valve',
        'why is this shit in the stema sale',
        'no wonder tf2 is fucked up',   
        'yea but i think its some cheese that',
	    'youtube is adding "fact checking" to world economic forum references',
        'makes you think about that guy that was on rogan',
        'people who have no clue what the wef is see that little snippet and they can change 90% of their minds over time',
        'or some shit',
        'this is kind of interesting',
        'trump canceled pelosi\'s trip to davos on the us taxpayers dime',
        'back in 2019',
        'Rick Rule''s VIRTUAL URANIUM Investors Bootcamp',
        'its a saturday marathon',
        'damn'
        'so thats why starlink was deployed in ukraine',
        'not to give the citizens access to tiktok',
        'but to give the military access to remote into vehicles',
        'just peeped that video',
        'looks like theyre def gonna use peoples starlinks as some sort of mesh network around the jurisdiction',
        'so that shit dont even gotta jump from orbit to the vehicle it can jump from some dudes roof top if its closer',
        'star link bout to be the next cyberdyne systems'

    ]
    
    #can do this with isalpha or regex 
    triggerWords = re.compile('[a-zA-Z]')
        
    
    #generate a random number (1-5). that number will determine how many messages are sent per triggerword
    
    
    #without bot prefix
    #only chat if instance is a DM channel initiated by the user
    if isinstance(message.channel, discord.DMChannel):
        #true if any words are from user and are in triggerwords 
        #if any (element in message.content for element in triggerWords):
        if triggerWords.search(message.content):
            randomNumber = secrets.choice(range(1, 5))
            print('random number is ', randomNumber)
            msgCount = 0
            while (msgCount < randomNumber):
                response = random.choice(skunkQuotes)
                async with message.channel.typing():
                    time.sleep(secrets.choice(range(1,10)))
                    await message.channel.send(response)
                    msgCount += 1
                    print('\n--message count is currently', msgCount)
                    '''
            #store and make the response random
            response = random.choice(rickQuotes)
            #indicate the bot is typing
            async with message.channel.typing():
                time.sleep(5) #implement a small delay before sending message
                await message.channel.send(response) #if all are true above, tell the user a random message
            async with message.channel.typing():
                response=random.choice(rickQuotes)
                time.sleep(3)
                await message.channel.send(response)
            async with message.channel.typing():
                response=random.choice(rickQuotes)
                time.sleep(3)
                await message.channel.send(response)
'''
'''
@bot.command(name='hey', help='responds with a random quote')
async def rick_message(ctx):
    rickQuotes = [
        'i dono man',
        'why group when you can solo'
    ]
    
    response = random.choice(rickQuotes)
    await ctx.send(response)
 '''
    
def randomizeMessageCount(number):
    number = random.randint(1,5)
    return number


    
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
bot.run(TOKEN)
