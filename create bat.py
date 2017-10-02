import os
Dir=os.path.split(os.path.abspath(__file__))[0]
with open(os.path.join(Dir,'Run BabyRagebot.bat'),'w') as batFile:
	batFile.write('start cmd.exe /k python "'+str(os.path.join(Dir,'BabyRage.py"')))
