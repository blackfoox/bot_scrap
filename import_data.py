import telebot

bot = telebot.TeleBot('6926148773:AAHOHmkB1TfGR0Vu3QknwbDWLU9koFIzClw')

messages = ["Чтобы вытащить игры из категории низкой оценки, напишете 'мусор'",
           "Чтобы вытащить игры из категории средней оценки, напишете 'проходняк'",
           "Чтобы вытащить игры из категории больше среднего, напишете 'похвально'",
           "Чтобы вытащить игры из категории изумительной оценки, напишете 'изумительно'",
           "Если вы хотите узнать, есть ли та или иная игра на сайте пропишите её. Нужно точное название игры."
]

db_config = {
    'host': "localhost",
    'dbname': "postgres",
    'user': "postgres",
    'password': "yashka000",
    'port': "5432"
}

urls = {'мусор': 'https://stopgame.ru/games/musor/new?p=',
        'проходняк': 'https://stopgame.ru/games/prohodnyak/new?p=',
        'похвально': 'https://stopgame.ru/games/pohvalno/new?p=',
        'изумительно': 'https://stopgame.ru/games/izumitelno/new?p='
}
