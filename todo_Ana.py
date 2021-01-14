import telebot, os


TOKEN = 'your_token'
bot = telebot.TeleBot(TOKEN)

if not os.path.exists(f'tasks/') != False:
    os.mkdir(f'tasks/')

'''
prepare buttons '/start' и '/all_commands'
'''

start_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
start_keyboard.row('/start', '/all_commands')
# and inline keys instead of commands /all, /new_item и /delete
keyboard = types.InlineKeyboardMarkup()
key_new_item = types.InlineKeyboardButton(text = 'New task', callback_data='new_item')
key_all = types.InlineKeyboardButton(text = 'All tasks', callback_data='all')
key_delete = types.InlineKeyboardButton(text = 'Delete the task', callback_data='delete')
keyboard.add(key_new_item, key_all, key_delete)


@bot.message_handler(commands=['start']) 
def start_handler(message):
    # check if the user was registered before
    if not os.path.exists(f'tasks/{message.from_user.id}/{message.from_user.id}.txt'):
        os.mkdir(f'tasks/{message.from_user.id}/')
        # if the user is first time here, then create a new folder for his tasks
        f = open(f'tasks/{message.from_user.id}/{message.from_user.id}.txt', 'w')
        f.write('')
        f.close()
        bot.send_message(message.from_user.id,
                         text = f"Hi, {message.from_user.first_name}! Let's begin? /all_commands",
                         reply_markup = start_keyboard)
    else:
        #  if the user is not new -  greet him
        bot.send_message(message.from_user.id, f"Welcome back, {message.from_user.first_name}!",
                         reply_markup=keyboard)


@bot.message_handler(commands = ['all_commands'])  
def all_commands_handler(message):
    bot.send_message(message.from_user.id, text = f'Hi, {message.from_user.first_name}. Here is what I can do',
                     reply_markup = keyboard)


@bot.callback_query_handler(func = lambda call: True)  # обработчик команд с кнопок
def callback_worker(call):
    if call.data == "new_item":
        bot.send_message(call.from_user.id,
                         f"ОК, let's write down the new task. Use keyword 'task', for example, 'task create Telegram-bot'")
    elif call.data == "all":
        todo_list = []  #  list with user's tasks 
        f = open(f'tasks/{call.from_user.id}/{call.from_user.id}.txt', 'r')
        for task in f:
            todo_list.append(task)
        '''print user's tasks one by one'''
        if todo_list != []:
            bot.send_message(call.from_user.id,
                             f"There are your tasks: ")
            for i in range(len(todo_list)):
                bot.send_message(call.from_user.id, f'{i + 1}. {todo_list[i]}')
        else:
            bot.send_message(call.from_user.id, 'It seems you did all you have planned. Well done!')

    elif call.data == "delete":
        bot.send_message(call.from_user.id,
                         f"Enter the number of the task you wanna delete")


@bot.message_handler(content_types=['text'])
def text_messages(message):
    todo_list = []  
    with open(f'tasks/{message.from_user.id}/{message.from_user.id}.txt', 'r') as f:
        for task in f:
            todo_list.append(task.strip())
    try:  #  trying to delete the task
        index = int(message.text.split()[-1])  # looking at the number of the task
        try:
            bot.send_message(message.from_user.id,
                             f'The task №{index}."{todo_list[index - 1]}" was deleted')
            del todo_list[index - 1]  # deleting the task
        except IndexError:  #  if the task doesn't exist
            bot.send_message(message.from_user.id,
                             f"The task №{index} doesn't exist. Check its number using /all command and try again")
    except ValueError:  # if text instead of the number was entered
        if (message.text.split()[0]).lower() == 'task':  #  checking the keyword
            task = str(' '.join(message.text.split()[1::]))
            todo_list.append(task)
            if todo_list[0] == '\n':
                del todo_list[0]
            bot.send_message(message.from_user.id, f"The task '{task}' was created")
            if todo_list[-1] == '\n':
                del todo_list[-1]
    if todo_list != []:
        bot.send_message(message.from_user.id,
                         f"There are your tasks:")
        for i in range(len(todo_list)):
            bot.send_message(message.from_user.id, f'{i + 1}. {todo_list[i]}')
    else:
        bot.send_message(message.from_user.id, 'It seems you did all you have planned. Well done!')
    f = open(f'tasks/{message.from_user.id}/{message.from_user.id}.txt', 'w')
    todo_list = map(lambda x: x + '\n', todo_list)
    f.writelines(todo_list)
    f.close()

    if message.text.lower() == 'hi' or message.text.lower() == 'hello':
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIH9V9uXTEon7lAwNLLy9ClJazmCv2IAAI9AgACusCVBSZBRSyGTjcJGwQ')


if __name__ == '__main__':
    bot.infinity_polling()
