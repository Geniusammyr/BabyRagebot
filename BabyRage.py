import asyncio #REMEBER THAT MOST THINGS MUST BE SPECIFIED AS ASYNCRONOUS TO WORK PROPERLY
import discord
import logging
import random
import time
import os
import time
import math
from discord import opus
from discord.ext.commands import Bot
from discord.ext import commands

currentFileName = os.path.split(os.path.abspath(__file__))[0]
botTextsDir = os.path.join(currentFileName,'bot texts')
#generates seed for random by smashing together hours/minutes/seconds of the current time
random.seed(int(str(time.localtime()[3]) + str(time.localtime()[4]) + str(time.localtime()[5])))
      
def makeBottyString(originalString):
        return ("```" + originalString + "```")
     
 #construct a string, uses a list passed in from the dnd function
def rollsDisplay(rollsList):
    rollsDisplay = ''
    for i in rollsList:
        rollsDisplay  += str(i) + ', '
    rollsDisplay = rollsDisplay[:-2]
    return rollsDisplay

    
#loads in all elements from config txt file,
def setConfig():
    settings=[]
    settingsDesc=[]
    with open(os.path.join(botTextsDir,'config.txt'),'r') as config: #open config.txt as config, in read mode
        for line in config:
            try:
                settings.append((line.split(':')[1])[:-1]) #shaves off \n from output, fix spaghetti later
                settingsDesc.append((line.split(':')[0]))
            except(IndexError):
                continue
                
    botPrefix = settings[0]
    dailyAllowance = int(settings[1])
    startingBalance = int(settings[2])
    breakEven = float(settings[3])
    moneyName = str(settings[4])
    botToken = str(settings[5])
    
    if settings[5] == "''":
        print('\n\nPut your bot token into the config before running your bot, or else it will give scary errors.\n\n')
        time.sleep(3)
    else:
        botToken = str(settings[5])
    print('Loaded the following settings from config: ')
    for i in range(0,len(settings)-1):
        print(settingsDesc[i] + ':\n' + settings[i])
    print("")
    return botPrefix, dailyAllowance, startingBalance, breakEven, moneyName, botToken

botPrefix, dailyAllowance, startingBalance, breakEven, moneyName, botToken = setConfig()
Client = discord.Client() #often called bot in api and examples
client = commands.Bot(command_prefix = botPrefix) #used when referencing discord.Client commands in api
logging.basicConfig(level = logging.INFO)


#passes a dict and a filename, to save the dict to the file
def dictWrite(setdict,filename):
    with open(os.path.join(botTextsDir,filename + '.txt'),'w') as setTxt:
        setTxt.write(str(setdict))


#opens up a txt file in read mode, name prodivded in args        
def dictRead(filename):
    setList = []
    setdict = dict() 
    
    with open(os.path.join(botTextsDir,filename + '.txt'),'r') as setTxt: #read in banktxt to banklist
        for line in setTxt:
            try:
                setList.append(eval(line))
            except (NameError,KeyError):
                pass
                
    for i in range(0,len(setList)): #convert banklist into bankDict
        setdict.update(setList[i])
    return setdict 

    
#displays message when bot becomes usable
@client.event
async def on_ready():  
    print(string(discord.version_info))
    print('Bot ID: ' + str(client.user.id))
    print("Bot Online!```")
    


@client.command(pass_context = True)
async def ping():
    '''
    Used to test if bot is responding
    '''
    await client.say(makeBottyString("Pong!"))
    
    
    
@client.command(pass_context = True)
async def pong():
    '''
    Used to test if bot is responding
    '''
    await client.say(makeBottyString("Ping!"))
    
    
#displays random string from file, strings are on their own individual lines in the pasta.txt file
@client.command(pass_context = True)
async def pasta(): 
    '''
    Displays high quality copypasta served fresh from the pasta.txt file
    '''
    pastaFile = open(os.path.join(botTextsDir,'pasta.txt'),'r')
    lenFinder=[]
    for i in pastaFile.readlines():
        lenFinder.append(i)
    n = random.randint(0,(len(lenFinder)-1))
    text = lenFinder[n]
    await client.say(text)
    
    
#basic coin flip command
@client.command(pass_context = True)
async def flip():   #flips a 'coin'
    '''
    Flip a coin
    '''
    coinrandom.randint(0,1)
    if coin == 0:
        await client.say(makeBottyString('Tails'))
    if coin == 1:
        await client.say(makeBottyString('Heads'))
    

#roll from 0 to number in args
@client.command(pass_context = True)
async def roll(self, number: int): #simple display of randint rolling
    '''
    Roll a number between 0 and your inputted number Ex: (command)roll 20
    '''
    rolled = random.randint(0, number)
    await client.say(makeBottyString("You rolled a " + str(rolled)))
   
#roll a random number between arg1 and arg2
@client.command(pass_context = True)
async def rollz(self, number1:int,number2:int):
    '''
    Roll between two numbers Ex: (command)rollz 1 10
    '''
    rolled = random.randint(number1,number2)
    await client.say(makeBottyString('Rolling between ' + str(number1) + ' and ' + str(number2) + '.\n' + str(rolled)))
        

#gamble an amount on a simulated slot machine
@client.command(pass_context = True)
async def gamble(ctx,bet:float = 0.0): 
    '''
    Gamble an amount of money (command)gamble 20, -1 for ALL-IN
    '''
    authorString = str(ctx.message.author)
    display=[]
    emotes = open(os.path.join(botTextsDir,'emotes.txt'),'r') #loads the contents of the emotes.txt file into the gamble function
    emotesList = emotes.read().splitlines()
    bankDict = dictRead("bank") #returns a usable python dictonary 
    if authorString not in bankDict.keys(): #create a new user in dict if not in dict
        bankDict.update({authorString:[startingBalance,366]}) 
        await client.say(makeBottyString('An account has been made for you, try betting again, you start out with ' + str(startingBalance)
        + ' ' +  moneyName + '.'))
        dictWrite(bankDict,"bank")
        return None
    else: 
        balance = bankDict[authorString][0]
    if bet < 0:
        if bet == -1:
            bet = balance
            if bet  ==  0: #flavor text for all-in spammers
                await client.say(ctx.message.author.mention + ' R.I.P. ' + moneyName + ', I think you\'ve already all-in\'ed enough.')
                return
            else:
                await client.say(makeBottyString('It\'s ALL IN boys!'))
        else:
            await client.say(makeBottyString('NO! (only positive numbers or -1 are valid bets)'))
            return None
    elif bet == 0.0:
        await client.say(makeBottyString('You can bet nothing, but you can\'t win any money that way!'))
    elif bet > balance:
        await client.say(makeBottyString('You can\'t bet more money than you have!'))
        return None
    bet = int(bet) #sanitize(poorly) user input, then deduct bet from account
    bankDict[authorString][0] -= bet
    for i in range(0,9): #load up lottery images
        display.append(emotesList[random.randint(0,len(emotesList)-1)])
    score = 0
    if display[0] == display[1] == display[2]:
        score += 10            
    if display[3] == display[4] == display[5]:
        score += 10            
    if display[6] == display[7] == display[8]:
        score += 10
    if display[0] == display[4] == display[8]:
        score += 10
    if display[6] == display[4] == display[2]:
        score += 10
    for i in range(0,9):
        if display[i] == emotesList[time.localtime()[6]]:
            score += 1
    points = math.ceil((score / breakEven) * bet) #average score is 2.22, the default value should cause a slight growth in money over time

    await client.say('>' + display[0] + display[1] + display[2] + '<\n>' + display[3] + display[4] + display[5] + '<\n>'
    + display[6] + display[7] + display[8] + '<')

    await client.say(ctx.message.author.mention + ', your score is ' + str(score) + '. Today\'s bonus item is '
    + emotesList[time.localtime()[6]] + '. That means that you win ' + str(points) + ' ' + moneyName + '. You now have '
    + str(bankDict[authorString][0] + points) + ' ' + moneyName + '.')
    
    bankDict[authorString][0] += points
    dictWrite(bankDict,"bank")

    
#companion to gamble function, displays bank balances and gives daily free money
@client.command(pass_context = True)
async def balance(ctx,freebie:int = 0):
    '''
    Check your gambling account balance (command)balance
    '''
    authorString = str(ctx.message.author)
    bankDict = dictRead("bank")
    try:
        balance = bankDict[authorString][0]
    except(KeyError):
        await client.say(makeBottyString(ctx.message.author.mention + ', try using the gamble command to make an account first.'))
        return None
    if bankDict[authorString][1] != time.localtime()[7]:
        freebie = dailyAllowance #This is the number added daily, change as you see fit for balance in the config
        bankDict[authorString][0] += freebie
        bankDict[authorString][1] = time.localtime()[7]
        bankDict[authorString][0] = math.ceil(bankDict[authorString][0])
        dictWrite(bankDict,"bank")
        await client.say(makeBottyString('You haven\'t claimed your daily ' + moneyName + ' yet! ' + str(dailyAllowance) + ' ' + moneyName
        + ' have been added to your account'))
    await client.say(ctx.message.author.mention + ', your bank balance is ' + str(balance + freebie) + ' ' + moneyName + '.')
        
        
#links wikipedia search for given terms
@client.command(pass_context = True) 
async def wiki(ctx,*args):
    '''
    Search wikipedia for the keywords provided (command)wiki keywords
    '''
    search_term = ''
    for i in range(len(args)):
        search_term += (args[i] + '_')
    await client.say('https://en.wikipedia.org/w/index.php?search=' + search_term)
    
    
#prints out a random capital letter
@client.command(pass_context = True) 
async def letter(ctx):
    '''
    Generate random letter a-z
    '''
    letterNum = random.randint(65,90)
    await client.say(makeBottyString(chr(letterNum)))
    
    
#based on dnd based rolling, arg1 is number of die, arg2 is value of die (d-6, d-20), and optional arg3 is the modifier
#added to the sum, not to each term
@client.command(pass_context = True)
async def dnd(ctx, *args): #"borrows" idea from roll20
    '''
    Advanced dice roller (command)dnd a/d/number die_number modifier
    '''
    rollsList = []
    rolls_total = 0
    argsCopy = []
    for i in args:
        argsCopy.append(i)
    for i in range(0,len(argsCopy)):
            try:
                argsCopy[i] = int(argsCopy[i])
            except(TypeError,ValueError):
                pass
    global bonus
    bonus = 0
    try:
        bonus = argsCopy[2]
    except(IndexError):
        argsCopy.append(0)
    if type(argsCopy[0]) == str:
        if argsCopy[0] == 'd' or argsCopy[0] == 'D':
            for i in range(0,2):
                rollsList.append(random.randint(1,argsCopy[1]))
            if rollsList[0] > rollsList[1]:
                rolls_total = rollsList[1]
            else:
                rolls_total = rollsList[0]
            await client.say(ctx.message.author.mention + ', Your rolls are: ' + rollsDisplay(rollsList)
            + ', and your final roll is: ' + str(rolls_total + bonus))
                
        if argsCopy[0] == 'a' or argsCopy[0] == 'A':
            for i in range(0,2):
                rollsList.append(random.randint(1,argsCopy[1]))
            if rollsList[0] < rollsList[1]:
                rolls_total = rollsList[1]
            else:
                rolls_total = rollsList[0]
            await client.say(ctx.message.author.mention + ', Your rolls are: ' + rollsDisplay(rollsList)
            + ', and your final roll is: ' + str(rolls_total + bonus))
    else:
        for i in range(0,argsCopy[0]):
            rollsList.append(random.randint(1,argsCopy[1]))
        for i in rollsList:
            rolls_total += i
        await client.say(ctx.message.author.mention + ', Your rolls are: ' + rollsDisplay(rollsList)
        + ', and your final roll is: ' + str(rolls_total + bonus))
            
@client.event
async def on_ready():  #displays ready
    print("Bot Online!")
    global emojiList
    emojiList = client.get_all_emojis()
    emojiList = list(emojiList)
    
client.run(botToken) #client botToken
