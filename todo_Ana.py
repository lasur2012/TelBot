import telebot
import os


TOKEN = 'your_token'
bot = telebot.TeleBot(TOKEN)

if not os.path.exists(f'tasks/') != False:
    os.mkdir(f'tasks/')

'''
готовим кнопки '/start' и '/all_commands'
'''

start_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
start_keyboard.row('/start', '/all_commands')
# и инлайновые кнопки, которые заменят ввод комманд /all, /new_item и /delete
keyboard = types.InlineKeyboardMarkup()
key_new_item = types.InlineKeyboardButton(text='Новая задача', callback_data='new_item')
key_all = types.InlineKeyboardButton(text='Все задачи', callback_data='all')
key_delete = types.InlineKeyboardButton(text='Удалить задачу', callback_data='delete')
keyboard.add(key_new_item, key_all, key_delete)


@bot.message_handler(commands=['start'])  # обработчик команды старт
def start_handler(message):
    # проверяем, был ли пользователь ранее зарегистрирован
    if not os.path.exists(f'tasks/{message.from_user.id}/{message.from_user.id}.txt'):
        os.mkdir(f'tasks/{message.from_user.id}/')
        # если он здесь впервые, то создаем для него файл, куда будут записываться его задачи
        f = open(f'tasks/{message.from_user.id}/{message.from_user.id}.txt', 'w')
        f.write('')
        f.close()
        bot.send_message(message.from_user.id,
                         text = f'Привет, {message.from_user.first_name}! С чего начнем? /all_commands',
                         reply_markup = start_keyboard)
    else:
        # если пользователь здесь не впервые, то просто приветствуем его и предлагаем начать работу
        bot.send_message(message.from_user.id, f"С возвращением, {message.from_user.first_name}!",
                         reply_markup=keyboard)


@bot.message_handler(commands = ['all_commands'])  # показывает доступный функционал бота
def all_commands_handler(message):
    bot.send_message(message.from_user.id, text = f'Привет, {message.from_user.first_name}. Вот список всех моих команд',
                     reply_markup=keyboard)


@bot.callback_query_handler(func = lambda call: True)  # обработчик команд с кнопок
def callback_worker(call):
    if call.data == "new_item":
        bot.send_message(call.from_user.id,
                         f'ОК, давай запишем новую задачу. Для этого используй ключевое слово "задача", например, задача создать Телеграм-бота')
    elif call.data == "all":
        todo_list = []  # сюда запишем список дел, который затем вернем пользователю
        f = open(f'tasks/{call.from_user.id}/{call.from_user.id}.txt', 'r')
        for task in f:
            todo_list.append(task)
        '''теперь выведем список наших задач по одной в сообщении'''
        if todo_list != []:
            bot.send_message(call.from_user.id,
                             f"Вот список всех твоих дел:")
            for i in range(len(todo_list)):
                bot.send_message(call.from_user.id, f'{i + 1}. {todo_list[i]}')
        else:
            bot.send_message(call.from_user.id, 'Похоже, ты выполнил все задачи. Так держать!')

    elif call.data == "delete":
        bot.send_message(call.from_user.id,
                         f"Введи номер задачи, которую хочешь удалить")


@bot.message_handler(content_types=['text'])
def text_messages(message):
    todo_list = []  # сюда запишем список дел, который затем вернем пользователю
    with open(f'tasks/{message.from_user.id}/{message.from_user.id}.txt', 'r') as f:
        for task in f:
            todo_list.append(task.strip())
    try:  # пытаемся удалить задачу, для этого проверяем, номер ли нам ввели
        index = int(message.text.split()[-1])  # смотрим на номер задачи к удалению
        try:
            bot.send_message(message.from_user.id,
                             f'Задача №{index}."{todo_list[index - 1]}" удалена')
            del todo_list[index - 1]  # удаляем задачу, помня про индексацию в Питоне
        except IndexError:  # если задача не существует
            bot.send_message(message.from_user.id,
                             f"Задача №{index} не существует. Проверь номер задачи при помощи команды /all и попробуй еще раз")
    except ValueError:  # ранее нам ввели не номер, а текст. Считаем, что это текст задачи
        if (message.text.split()[0]).lower() == 'задача':  # проверяем по ключевому слову, прислал ли пользователь новую задачу, или просто незначимое сообщение
            task = str(' '.join(message.text.split()[1::]))
            todo_list.append(task)
            if todo_list[0] == '\n':
                del todo_list[0]
            bot.send_message(message.from_user.id, f"Задача '{task}' записана")
            if todo_list[-1] == '\n':
                del todo_list[-1]
    if todo_list != []:
        bot.send_message(message.from_user.id,
                         f"Вот список всех твоих дел:")
        for i in range(len(todo_list)):
            bot.send_message(message.from_user.id, f'{i + 1}. {todo_list[i]}')
    else:
        bot.send_message(message.from_user.id, 'Похоже, ты выполнил все задачи. Так держать!')
    f = open(f'tasks/{message.from_user.id}/{message.from_user.id}.txt', 'w')
    todo_list = map(lambda x: x + '\n', todo_list)
    f.writelines(todo_list)
    f.close()

    if message.text.lower() == 'привет':
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIH9V9uXTEon7lAwNLLy9ClJazmCv2IAAI9AgACusCVBSZBRSyGTjcJGwQ')


if __name__ == '__main__':
    bot.infinity_polling()
