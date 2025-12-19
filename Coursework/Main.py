from telebot import TeleBot
from Databases.UsersDatabase import UsersDatabase
from Databases.MealsDatabase import MealsDatabase
from Databases.FoodDatabase import FoodDatabase
from Utils.UserManager import UserManager
from Utils.FoodManager import FoodManager

bot = TeleBot(BOT_TOKEN)

USERS_DATABASE = UsersDatabase()
MEALS_DATABASE = MealsDatabase()
FOOD_DATABASE = FoodDatabase()

USER_MANAGER = UserManager(bot, USERS_DATABASE)
FOOD_MANAGER = FoodManager(bot, MEALS_DATABASE, FOOD_DATABASE)

@bot.message_handler(content_types=['text'])
def text_handler(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if message.text == "/start":
        USER_MANAGER.start_registration(chat_id, user_id)
    else:
        user = USER_MANAGER.user_exist(chat_id, user_id)
        if user:
            match message.text:
                case "Добавить вручную":
                    FOOD_MANAGER.add_food_manually(chat_id, user)

                case "Удалить запись":
                    FOOD_MANAGER.ask_to_delete_meal(chat_id, user_id)

                case "Редактировать профиль":
                    USER_MANAGER.start_editing_profile(chat_id, user)

                case "Статистика за месяц":
                    FOOD_MANAGER.nutrients_per_month(chat_id, user)

                case _:
                    FOOD_MANAGER.search_food(message, user)

bot.polling(none_stop=True)