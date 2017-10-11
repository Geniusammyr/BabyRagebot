import asyncio
import random
import discord
import os
import time
import logging
import math
from discord.ext.commands import Bot
from discord.ext import commands

currentFile=os.path.split(os.path.abspath(__file__))[0]
Dir=os.path.join(currentFile,'bot texts')
random.seed(int(str(time.localtime()[3])+str(time.localtime()[4])+str(time.localtime()[5]))) #generates seed for random by smashing together hours/minutes/seconds of the current time

def rolls_display(rolls_list):
	rolls_display=''
	for i in rolls_list:
		rolls_display+=str(i)+', '
	rolls_display=rolls_display[:-2]
	return rolls_display
	
def setConfig():
	settings=[]
	settings_desc=[]
	with open(os.path.join(Dir,'config.txt'),'r') as config: #read config file
		for line in config:
			try:
				settings.append((line.split(':')[1])[:-1]) #shaves off \n from output, fix spaghetti later
				settings_desc.append((line.split(':')[0]))
			except(IndexError):
				continue
	bot_prefix=settings[0]
	daily_allowance=int(settings[1])
	starting_balance=int(settings[2])
	break_even=float(settings[3])
	money_name=str(settings[4])
	token=str(settings[5])
	if settings[5]=="''":
		print('\n\nPut your token into the config before running your bot, or else it will give scary errors.\n\n')
		time.sleep(3)
	else:
		token=str(settings[5])
	print('Loaded the following settings from config: ')
	for i in range(0,len(settings)-1):
		print(settings_desc[i]+':\n'+settings[i])
	return bot_prefix, daily_allowance, starting_balance, break_even, money_name,token
logging.basicConfig(level=logging.INFO)
Client = discord.Client()
bot_prefix, daily_allowance, starting_balance, break_even, money_name, token = setConfig()
client = commands.Bot(command_prefix=bot_prefix)

def bankWrite(bankdict): #opens bank.txt for writing
	with open(os.path.join(Dir,'bank.txt'),'w') as bankTxt:
		bankTxt.write(str(bankdict))
		
def bankRead(): #opens bank up for reading
	banklist = []
	bankdict=dict() 
	with open(os.path.join(Dir,'bank.txt'),'r') as bankTxt: #read in banktxt to banklist
		for line in bankTxt:
			try:
				banklist.append(eval(line))
			except (NameError,KeyError):
				pass
	for i in range(0,len(banklist)): #convert banklist into bankdict
		bankdict.update(banklist[i])
	return bankdict		
	
def expRead(): #opens exp up for reading
	explist = []
	expdict=dict() 
	with open(os.path.join(Dir,'exp.txt'),'r') as expTxt: #read in banktxt to banklist
		for line in expTxt:
			try:
				explist.append(eval(line))
			except (NameError,KeyError):
				pass
	for i in range(0,len(explist)): #convert explist into expdict
		expdict.update(explist[i])
	return expdict	
	
def expWrite(expdict): #opens exp.txt for writing
	with open(os.path.join(Dir,'exp.txt'),'w') as expTxt:
		expTxt.write(str(expdict))
@client.event
async def on_ready():  #displays info on ready
	print(discord.version_info)
	print('Bot ID: '+str(client.user.id))
	print("Bot Online!")
	

@client.command(pass_context=True)
async def ping():
	'''
	Used to test if bot is responding
	'''
	await client.say("Pong!")
	
@client.command(pass_context=True)
async def pong():
	'''
	Used to test if bot is responding
	'''
	await client.say('Ping!')
	
@client.command(pass_context=True)
async def pasta(): #displays random pasta from file, pastas are on their own individual line in the txt file
	'''
	Displays high quality copypasta served fresh from the pasta.txt file
	'''
	my_file=open(os.path.join(Dir,'pasta.txt'),'r')
	lenFinder=[]
	for i in my_file.readlines():
		lenFinder.append(i)
	n=random.randint(0,(len(lenFinder)-1))
	text=lenFinder[n]
	await client.say(text)
	
@client.command(pass_context=True)
async def flip():   #flips a 'coin'
	'''
	Filp a coin
	'''
	coin=random.randint(0,1)
	if coin==0:
		await client.say('FluffyTail')
	if coin==1:
		await client.say('4Head')
		
@client.command(pass_context=True)
async def roll(self, number: int): #simple display of randint rolling
	'''
	Roll a number between 0 and your inputted number Ex: (command)roll 20
	'''
	rolled=random.randint(0,number)
	await client.say("You rolled a "+str(rolled))
	
@client.command(pass_context=True)
async def rollz(self, number1:int,number2:int): #simple display of randint rolling, with both parameters being optional
	'''
	Roll between two numbers Ex: (command)rollz 1 10
	'''
	await client.say('Rolling between '+str(number1)+' and '+str(number2)+'.')
	rolled=random.randint(number1,number2)
	await client.say(str(rolled))
			
@client.command(pass_context=True)
async def gamble(ctx,bet:float=0.0): 
	'''
	Gamble an amount of money (command)gamble 20, -1 for ALL-IN
	'''
	authorString=str(ctx.message.author)
	display=[]
	emotes=open(os.path.join(Dir,'emotes.txt'),'r') #loads the contents of the emotes.txt file into the gamble function
	listt=emotes.read().splitlines()
	bankdict=bankRead() #returns a usable python dictonary 
	if authorString not in bankdict.keys(): #create a new user in dict if not in dict
		bankdict.update({authorString:[starting_balance,366]}) #first number in the list is the default amount given to a new account, change as you see fit in the config
		await client.say('An account has been made for you, try betting again, you start out with '+str(starting_balance)+' '+ money_name+'.')
		bankWrite(bankdict)
		return None
	else: 
		balance=bankdict[authorString][0]
	if bet<0:
		if bet==-1:
			bet=balance
			if bet==0: #flavor text for all-in spammers
				await client.say(ctx.message.author.mention+' R.I.P. '+money_name+', I think you\'ve already all-in\'ed enough.')
			else:
				await client.say('It\'s ALL IN boys.')
		else:
			await client.say('NO! (only positive numbers or -1 are valid bets)')
			return None
	elif bet==0.0:
		await client.say('You can bet nothing, but you can\'t win any money that way!')
	elif bet>balance:
		await client.say('You can\'t bet more money than you have!')
		return None
	bet=int(bet) #sanitize(poorly) user input, then deduct bet from account
	bankdict[authorString][0]-=bet
	for i in range(0,9): #load up lottery images
		display.append(listt[random.randint(0,len(listt)-1)])
	score=0
	if display[0]==display[1]==display[2]:
		score+=10			
	if display[3]==display[4]==display[5]:
		score+=10			
	if display[6]==display[7]==display[8]:
		score+=10
	if display[0]==display[4]==display[8]:
		score+=10
	if display[6]==display[4]==display[2]:
		score+=10
	for i in range(0,9):
		if display[i]==listt[time.localtime()[6]]:
			score+=1
	points=math.ceil((score/break_even)*bet) #average score is 2.22, the default value should cause a slight growth in money over time
	await client.say('>'+display[0]+display[1]+display[2]+'<\n>'+display[3]+display[4]+display[5]+'<\n>'+display[6]+display[7]+display[8]+'<')
	await client.say(ctx.message.author.mention+', your score is '+str(score)+'. Today\'s bonus item is '+listt[time.localtime()[6]]+'. That means that you win '+str(points)+' '+money_name+'. You now have '+str(bankdict[authorString][0]+points)+' '+money_name+'.')
	bankdict[authorString][0]+=points
	bankWrite(bankdict)

@client.command(pass_context=True)
async def balance(ctx,freebie:int=0):
	'''
	Check your gambling account balance (command)balance
	'''
	authorString=str(ctx.message.author)
	bankdict=bankRead()
	try:
		balance=bankdict[authorString][0]
	except(KeyError):
		await client.say(ctx.message.author.mention+', try using the gamble command to make an account first.')
		return None
	if bankdict[authorString][1]!=time.localtime()[7]:
		freebie=daily_allowance #This is the number added daily, change as you see fit for balance in the config
		bankdict[authorString][0]+=freebie
		bankdict[authorString][1]=time.localtime()[7]
		bankdict[authorString][0]=math.ceil(bankdict[authorString][0])
		bankWrite(bankdict)
		await client.say('You haven\'t claimed your daily '+money_name+' yet! '+str(daily_allowance)+' '+money_name+' have been added to your account')
	await client.say(ctx.message.author.mention+', your bank balance is '+str(balance+freebie)+' '+money_name+'.')
		
@client.command(pass_context=True) 
async def wiki(ctx,*args): #links wikipedia page for given terms
	'''
	Search wikipedia for the keywords provided (command)wiki keywords
	'''
	search_term=''
	for i in range(len(args)):
		search_term+=(args[i]+'_')
	await client.say('https://en.wikipedia.org/w/index.php?search='+search_term)
	
@client.command(pass_context=True) 
async def letter(ctx):
	'''
	Generate random letter a-z
	'''
	letter_num=random.randint(1,26)
	letters={1:'a',2:'b',3:'c',4:'d',5:'e',6:'f',7:'g',8:'h',9:'i',10:'j',11:'k',12:'l',13:'m',14:'n',15:'o',16:'p',17:'q',18:'r',19:'s',20:'t',21:'u',22:'v',23:'w',24:'x',25:'y',26:'z'}
	await client.say(letters[letter_num].upper())
	
@client.command(pass_context=True)
async def dnd(ctx, *args): #"borrows" idea from roll20
	'''
	Advanced dice roller (command)dnd a/d/number die_number modifier
	'''
	rolls_list=[]
	rolls_total=0
	args_copy=[]
	for i in args:
		args_copy.append(i)
	for i in range(0,len(args_copy)):
			try:
				args_copy[i]=int(args_copy[i])
			except(TypeError,ValueError):
				pass
	global bonus
	bonus=0
	try:
		bonus=args_copy[2]
	except(IndexError):
		args_copy.append(0)
	if type(args_copy[0])==str:
		if args_copy[0]=='d' or args_copy[0]=='D':
			for i in range(0,2):
				rolls_list.append(random.randint(1,args_copy[1]))
			if rolls_list[0]>rolls_list[1]:
				rolls_total=rolls_list[1]
			else:
				rolls_total=rolls_list[0]
			await client.say(ctx.message.author.mention+', Your rolls are: '+rolls_display(rolls_list)+', and your final roll is: '+str(rolls_total+bonus))
				
		if args_copy[0]=='a' or args_copy[0]=='A':
			for i in range(0,2):
				rolls_list.append(random.randint(1,args_copy[1]))
			if rolls_list[0]<rolls_list[1]:
				rolls_total=rolls_list[1]
			else:
				rolls_total=rolls_list[0]
			await client.say(ctx.message.author.mention+', Your rolls are: '+rolls_display(rolls_list)+', and your final roll is: '+str(rolls_total+bonus))
	else:
		for i in range(0,args_copy[0]):
			rolls_list.append(random.randint(1,args_copy[1]))
		for i in rolls_list:
			rolls_total+=i
		await client.say(ctx.message.author.mention+', Your rolls are: '+rolls_display(rolls_list)+', and your final roll is: '+str(rolls_total+bonus))
		
@client.command(pass_context=True)
async def exp(ctx, *args):
	'''
	Gives daily exp and keeps track of arbitray levels
	'''
	authorString = str(ctx.message.author)
	expdict = expRead()
	if authorString not in expdict.keys(): #create a new user in dict if not in dict
		expdict.update({authorString:[1,0,366]})
		await client.say(ctx.message.author.mention+', a new account has been made for your power level, try again')
		expWrite(expdict)
		return None
	else: 
		if expdict[authorString][2] != time.localtime()[7]:
			expdict[authorString][2]=time.localtime()[7]
			added_exp = random.randint(1,100)
			await client.say(ctx.message.author.mention + ', you have gained ' + str(added_exp) + ' exp for today.')
			expdict[authorString][1] += added_exp
			expWrite(expdict)
		else:
			await client.say(ctx.message.author.mention + ', Your level is ' + str(expdict[authorString][0]) + ' and you have ' + str(expdict[authorString][1]) + ' exp.')
		while (10 * expdict[authorString][0] +1) < expdict[authorString][1]:
			expdict = expRead()
			expdict[authorString][1] -= (10 * expdict[authorString][0] + 1)
			expdict[authorString][0] += 1
			await client.say(ctx.message.author.mention + ', you have leveled up! Your new level is ' + str(expdict[authorString][0]) + ' and you have ' + str(expdict[authorString][1]) + ' exp.')
			expWrite(expdict)
	

client.run(token) #client token

