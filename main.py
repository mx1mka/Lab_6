import sqlite3
import telebot

conn = sqlite3.connect('mydb.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, name TEXT, value INTEGER)')

bot = telebot.TeleBot('6521721833:AAEyE9ukJSVqsVTv4aQhUGUp26cUCw2Cfac')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, я телеграм бот магазина. Вы можете использовать следующие команды:\n\n'
                                      '/add name value - добавить товар с названием name и количеством value\n'
                                      '/show - показать все товары в табличном виде\n'
                                      '/buy name value - купить товар\n'
                                      '/delete id - удалить товар\n'
                                      '/help - показать эту справку')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Вы можете использовать следующие команды:\n\n'
                                      '/add name value - добавить запись с именем name и значением value в базу данных\n'
                                      '/show - показать все записи из базы данных в табличном виде\n'
                                      '/buy name value - купить товар\n'
                                      '/delete id - удалить товар\n'
                                      '/help - показать эту справку')

@bot.message_handler(commands=['add'])
def add(message):
    args = message.text.split()
    if len(args) == 3:
        try:
            name = args[1]
            value = int(args[2])
            cursor.execute('INSERT INTO data (name, value) VALUES (?, ?)', (name, value))
            conn.commit()
            bot.send_message(message.chat.id, 'Запись успешно добавлена в базу данных')
        except Exception as e:
            bot.send_message(message.chat.id, 'Произошла ошибка при добавлении записи в базу данных: ' + str(e))
    else:
        bot.send_message(message.chat.id, 'Неверный формат команды. Используйте /add name value')

@bot.message_handler(commands=['show'])
def show(message):
    try:
        cursor.execute('SELECT * FROM data')
        rows = cursor.fetchall()
        table = '| ID | Название | Количество |\n'
        table += '|----|------|-------|\n'
        for row in rows:
            table += '| ' + str(row[0]) + ' | ' + str(row[1]) + ' | ' + str(row[2]) + ' |\n'
        bot.send_message(message.chat.id, table)
    except Exception as e:
        bot.send_message(message.chat.id, 'Произошла ошибка при показе записей из базы данных: ' + str(e))

@bot.message_handler(commands=['buy'])
def buy(message):
        args = message.text.split()
        if len(args) == 3:
            try:
                b_name = args[1]
                b_value = int(args[2])
                cursor.execute('SELECT * FROM data')
                rows = cursor.fetchall()
                kl = 0
                for row in rows:
                    if str(row[1] == b_name):
                        kl=1
                        if int(row[2]) - b_value > -1:
                            b_value = int(row[2]) - b_value
                            cursor.execute('UPDATE data SET value = ? WHERE id = ?', (b_name, b_value))
                            bot.send_message(message.chat.id, "Успешная покупка")
                            conn.commit()
                        else:
                            bot.send_message(message.chat.id, "Недостаточно товара на складе")
                if kl==0:
                    bot.send_message(message.chat.id, "Товар с указанным названием не найден на складе")
            except Exception as e:
                bot.send_message(message.chat.id, 'Произошла ошибка при покупке товара: ' + str(e))
        else:
            bot.send_message(message.chat.id, 'Неверный формат команды. Используйте /buy name value')

@bot.message_handler(commands=['delete'])
def delete(message):
    args = message.text.split()
    if len(args) == 2:
        try:
            id = int(args[1])
            cursor.execute('DELETE FROM data WHERE id = ?', (id,))
            conn.commit()
            bot.send_message(message.chat.id, 'Запись успешно удалена из базы данных')
        except Exception as e:
            bot.send_message(message.chat.id, 'Произошла ошибка при удалении записи из базе данных: ' + str(e))
    else:
        bot.send_message(message.chat.id, 'Неверный формат команды. Используйте /delete id')

bot.polling(none_stop = True)