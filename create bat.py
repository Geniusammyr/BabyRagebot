import os
Dir=os.path.split(os.path.abspath(__file__))[0]
with open(os.path.join(Dir,'Run LuLbot.bat'),'w') as batFile:
	batFile.write('start cmd.exe /k python '+str(os.path.join(Dir,'LuLbot.py')))
#start cmd.exe /k python C:\Users\geniusammyr\desktop\LuLbot\personalbot.py