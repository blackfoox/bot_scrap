from bs4 import BeautifulSoup
import requests
import time
import psycopg2
from import_data import messages, db_config, urls, bot


### Обработка команды /start
class BotMassege:
    def __init__(self, bot, messages):
        self.bot = bot
        self.messages = messages

    ### Функция, которая отправляет приветственное сообщение и список команд пользователю
    def bot_functionality(self, message):
        # Отправка приветственного сообщения с информацией о возможностях бота
        self.bot.send_message(message.chat.id, f"Привет {message.from_user.first_name}, я могу вытащить игры из сайта stopgame из категории 'мусор', 'проходняк', 'похвально' , 'изумительно'")

        # Цикл отправляет пользователю дополнительные сообщения из списка `messages`
        for mess in self.messages:
            time.sleep(2)
            self.bot.send_message(message.chat.id, mess)


### Обработка команды /start. Этот обработчик вызывается, когда пользователь отправляет команду /start.
@bot.message_handler(commands=['start'])
def start_message(message):
    bot_message = BotMassege(bot, messages)
    bot_message.bot_functionality(message)


### Класс для скрапинга игр из указанных пользователем категорий и обработки информации об одной игре
class ProvidingGames:
    def __init__(self, bot, urls, message_in_user):
        self.bot = bot
        self.urls = urls
        self.message = message_in_user.text.lower()
    
    ### Функция для скрапинга игр с сайта stopgame по категории, указанной пользователем
    def scrap_games(self, message):
        try:
            page = 0
            games = [] # Список для хранения названий игр, чтобы избежать повторов

            # Получаем URL для категории игр, введенной пользователем
            url = self.urls[self.message]

            ### Скрапинг всех игр из указанной категории на всех страницах
            while True:
                page += 1
                new_page_url = url + str(page) # Добавляем номер страницы к URL
                soup = BeautifulSoup(requests.get(new_page_url).text, 'html.parser')
                data = soup.select('._card_1u499_4') # Получаем данные об играх

                time.sleep(5) # Пауза между запросами для избегания блокировки

                ### Проверяем, есть ли игра уже в списке `games`. Если нет, то добавляем и отправляем данные пользователю
                if data[0]['title'] not in games:
                    for item in data:
                        self.bot.send_message(message.chat.id, item['title'])
                        self.bot.send_message(message.chat.id, f"https://stopgame.ru{item['href']}")
                        self.bot.send_message(message.chat.id, '--------------------------------------------')
                        games.append(item['title'])
                else:    
                    break # Прерываем цикл, если в текущей категории больше нет новых игр


        ### Если возникла ошибка (например, введенная категория отсутствует), то выполняется запрос к базе данных для поиска конкретной игры
        except:
           ### Создаем объект класса OneGame и запускаем метод для получения информации об игре
           game_info = OneGame(db_config, bot, message)
           game_info.game_in_db(message)
            

### Обработчик любых текстовых сообщений от пользователя
@bot.message_handler()
def games(message):
    # Создаем объект класса ProvidingGames и вызываем функцию скрапинга игр
    providing_games = ProvidingGames(bot, urls, message)
    providing_games.scrap_games(message)



### Класс для поиска информации об одной игре из базы данных
class OneGame:
    def __init__(self, db_config, bot, message):
        # Устанавливаем соединение с базой данных
        self.conn = psycopg2.connect(**db_config)
        self.cur = self.conn.cursor()
        self.bot = bot
        self.message = message


    ### Функция для поиска игры в базе данных и отправки информации пользователю
    def game_in_db(self, message):
        # Используем курсор для выполнения SQL-запроса для поиска игры по названию
        with self.conn.cursor() as self.cur:
            self.cur.execute("SELECT * FROM person WHERE game_name = %s", (message.text,))
            game = self.cur.fetchall()

        ### Если игра найдена в базе данных, парсим и отправляем дополнительную информацию
        if game:
            # Делаем запрос на страницу игры для получения информации о дате выхода
            soup = BeautifulSoup(requests.get(game[0][1]).text, 'html.parser')            
            release_data = soup.find('dd').text

            # Отправляем пользователю информацию об игре
            self.bot.send_message(message.chat.id, game[0][0]) # Название игры
            self.bot.send_message(message.chat.id, game[0][1]) # Ссылка на игру
            self.bot.send_message(message.chat.id, f"Дата выхода: {release_data}")
            self.bot.send_message(message.chat.id, '--------------------------------------------')
            # Закрываем соединение с базой данных
            self.conn.close()
        ### Если игра не найдена, отправляем сообщение пользователю
        else:
            self.bot.send_message(message.chat.id, "Либо такой игры нет на сайте, либо вы допустили ошибку.")
            self.conn.close() # Закрываем соединение с базой данных


# Запускаем бота для постоянной обработки сообщений (бот будет работать без остановки)
bot.polling(none_stop=True)