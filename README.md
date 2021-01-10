# TelBot
It is a Telegram bot created in order to be accepted to the the Programming Track of the workshop by Projectsthatwork.  The bot is able to recognize the user, write down his or her tasks, show these tasks, delete any chosen task. 

NOTE: This bot was the first bot I have created so it has a lot of strange lines and strange decisions. 



The order of launching a Telegram bot:
1. create a new project
2. download the requirements.txt file with a list of the required versions of the libraries (it is one) and install them into the virtual environment via pip: pip install -r requirements.txt.
3.in TOKEN = 'your_token' instead of 'your_token' insert the bot token, where the program will be launched
4.run bot

Using a bot in Telegram:
1. the / start command registers a new user or greets an old user and offers to use the button with the / all_commands command, which lists
all available bot functions
2. bot can: 
- record new user tasks
- delete tasks
- show all tasks

