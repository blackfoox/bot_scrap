from bs4 import BeautifulSoup
import requests
import telebot
import time
import random
import psycopg2

bot = telebot.TeleBot('6926148773:AAHOHmkB1TfGR0Vu3QknwbDWLU9koFIzClw')
messages = ["Чтобы вытащить игры из категории низкой оценки, напишете 'мусор'",
           "Чтобы вытащить игры из категории средней оценки, напишете 'проходняк'",
           "Чтобы вытащить игры из категории больше среднего, напишете 'похвально'",
           "Чтобы вытащить игры из категории изумительной оценки, напишете 'изумительно'",
           "Если вы хотите узнать, есть ли та или иная игра на сайте пропишите её. Нужна точная информация игры."
]

@bot.message_handler(commands=['start'])
def power(message):
    bot.send_message(message.chat.id, f"Привет {message.from_user.first_name}, я могу вытащить игры из сайта stopgame из категорий 'мусор', 'проходняк', 'похвально' , 'изумительно'")
    for mess in messages:
        time.sleep(2)
        bot.send_message(message.chat.id, mess)

urls = {'мусор': 'https://stopgame.ru/games/musor/new?p=',
        'проходняк': 'https://stopgame.ru/games/prohodnyak/new?p=',
        'похвально': 'https://stopgame.ru/games/pohvalno/new?p=',
        'изумительно': 'https://stopgame.ru/games/izumitelno/new?p='
}

@bot.message_handler()
def info(message):
    data_from_user = message.text.lower()
    if data_from_user in urls:
        page = 0
        games = []

        url = urls[data_from_user]

        while True:
            page += 1
            new_page_url = url + str(page)
            soup = BeautifulSoup(requests.get(new_page_url).text, 'html.parser')
            data = soup.select('._card_1u499_4')
            time.sleep(10)
            
            if data[0]['title'] not in games:
                for item in data:
                    bot.send_message(message.chat.id, item['title'])
                    bot.send_message(message.chat.id, f"https://stopgame.ru{item['href']}")
                    bot.send_message(message.chat.id, '--------------------------------------------')
                    games.append(item['title'])
            else:
                break
    else:
        conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres",
                        password="yashka000", port="5432")

        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM person WHERE game_name = %s", (data_from_user,))
            game = cursor.fetchall()

        if game:
            soup = BeautifulSoup(requests.get(game[0][2]).text, 'html.parser')
            release_data = soup.find('dd').text
            bot.send_message(message.chat.id, game[0][1])
            bot.send_message(message.chat.id, game[0][2])
            bot.send_message(message.chat.id, f"Дата выхода: {release_data}")
            bot.send_message(message.chat.id, '--------------------------------------------')
            conn.close()

        else:
            bot.send_message(message.chat.id, 'Либо такой игры нет на сайте, либо вы допустили ошибку.')
            
bot.polling(none_stop=True)
