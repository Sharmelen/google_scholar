import os
import time


print('Please Select One of These: \n 1.Search Paper By Author \n 2.Search Paper By Keyword')


number = input('Please pick your number \n')

if(number == 1):
	selection = 'author'
	keyword = input('Please Enter The Name Of The Author \n')
else:
	selection = 'phrase'
	keyword = input('Please Enter Your Keyword \n')

os.system("gnome-terminal -e 'bash -c \"python3 scholar.py -c 2 --{} {} > result; exec bash\"'".format(selection, keyword))

time.sleep(3)

results = open('result','r')
list_r = results.read()
