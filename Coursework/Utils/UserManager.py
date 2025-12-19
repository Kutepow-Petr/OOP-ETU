import telebot
from telebot import types
from User import User
from Databases.UsersDatabase import UsersDatabase

class UserManager:
    def __init__(self, bot: telebot.TeleBot, users_db: UsersDatabase):
        self.bot = bot
        self.users_db = users_db
        self.registration_data = {}
        self.users_in_editing = {}
        self._setup_handlers()



    def user_exist(self, chat_id: int, user_id: int) -> User:
        user = self.users_db.get_user(user_id)
        if user:
            return user
        else:
            self.bot.send_message(
                chat_id,
                "❌ Похоже, ты не зарегистрирован(а)"
                "\nОтправь '/start' для регистрации"
            )
            return None
        


    def start_registration(self, chat_id: int, user_id: int):
        self.registration_data[chat_id] = {}
        self.registration_data[chat_id]["user_id"] = user_id

        self.bot.send_message(chat_id, "Привет! 👋 Расскажи о себе")
        self._ask_gender(chat_id, "registration")

    def _complete_registration(self, chat_id: int):
        try:
            user = User(**self.registration_data[chat_id])
            self.users_db.add_user(user)
            self.bot.send_message(
                chat_id,
                f"✅ <b>Регистрация завершена!</b>\n"
                f"{str(user)}",
                parse_mode="html")
            self.bot.send_message(
                chat_id,
                f"✨ <b>Теперь можно добавлять приемы пищи</b>\n\n"
                f"Просто отправь сообщение в формате:\n"
                f"  продукт, граммы\n"
                f"📊 Например:\n"
                f"  <em>овсянка, 100</em>",
                parse_mode="html", reply_markup=(
                    types.ReplyKeyboardMarkup(
                    ).row(
                        types.KeyboardButton("Добавить вручную"),
                        types.KeyboardButton("Удалить запись")
                    ).row(
                        types.KeyboardButton("Статистика за месяц"),
                        types.KeyboardButton("Редактировать профиль")
                    )
                )
            )
        except:
            self.bot.send_message(
                chat_id, 
                "⚠️ Не удалось завершить регистрацию.\nПопробуй через некоторое время"
            )
        del self.registration_data[chat_id]
    


    def start_editing_profile(self, chat_id: int, user: User):
        self.users_in_editing[chat_id] = user
        self.bot.send_message(
            chat_id,
            "Что изменить?",
            reply_markup=self._buttons_from_dict(
                {
                    "Цель": "change_goal",
                    "Активность": "change_activity",
                    "Вес": "change_weight",
                    "Рост": "change_height",
                    "Дату рождения": "change_birth",
                    "Пол": "change_gender"
                }
            )
        )

    def _complete_editing_profile(self, chat_id: int, attribute: str, value):
        try:
            user = self.users_in_editing[chat_id]
        except: pass

        setattr(user, attribute, value)
        user.update_daily_nutriments()

        if self.users_db.add_user(user):
            self.bot.send_message(
                chat_id, 
                f"✅ <b>Успешно изменено</b>\n"
                f"{str(user)}",
                parse_mode="html"
            )
        else:
            self.bot.send_message(
                chat_id, 
                "⚠️ Не удалось изменить профиль.\nПопробуй позже"
            )
        del self.users_in_editing[chat_id]
    


    def _ask_gender(self, chat_id: int, action: str):
        buttons_dict = {}
        for key, value in User.GENDER.items():
            buttons_dict[value["discription"]] = f"get_gender_{key}_{action}"
        self.bot.send_message(
            chat_id,
            "Твой пол:",
            reply_markup=self._buttons_from_dict(buttons_dict)
        )

    def _ask_birth(self, chat_id: int, action: str):
        message = self.bot.send_message(
            chat_id,
            "🎂 Год рождения? Отправь мне целое число"
        )
        self.bot.register_next_step_handler(message, self._get_birth, action)

    def _ask_height(self, chat_id: int, action: str):
        message = self.bot.send_message(
            chat_id,
            "❓ Какой у тебя рост (см)? Отправь мне целое число или число с точкой"
        )
        self.bot.register_next_step_handler(message, self._get_height, action)

    def _ask_weight(self, chat_id: int, action: str):
        message = self.bot.send_message(
            chat_id,
            "❓ Какой у тебя вес (кг)? Отправь мне целое число или число с точкой"
        )
        self.bot.register_next_step_handler(message, self._get_weight, action)

    def _ask_activity(self, chat_id: int, action: str):
        buttons_dict = {}
        for key, value in User.ACTIVITIES.items():
            buttons_dict[value["discription"]] = f"get_activity_{key}_{action}"
        self.bot.send_message(
            chat_id,
            "Какая у тебя активность?",
            reply_markup=self._buttons_from_dict(buttons_dict)
        )

    def _ask_goal(self, chat_id: int, action: str):
        buttons_dict = {}
        for key, value in User.GOALS.items():
            buttons_dict[value["discription"]] = f"get_goal_{key}_{action}"
        self.bot.send_message(
            chat_id,
            "Выбери свою цель:",
            reply_markup=self._buttons_from_dict(buttons_dict)
        )



    def _get_birth(self, message, action: str):
        chat_id = message.chat.id
        try:
            birth = int(message.text)

            if action == "registration":
                self.registration_data[chat_id]["birth"] = birth
                self._ask_height(chat_id, "registration")
            elif action == "editing":
                self._complete_editing_profile(chat_id, "birth", birth)
        except ValueError:
            message = self.bot.send_message(chat_id, "❌ Отправь целое число!")
            self.bot.register_next_step_handler(
                message,
                self._get_birth,
                action
            )

    def _get_height(self, message, action: str):
        chat_id = message.chat.id
        try:
            height = float(message.text)

            if action == "registration":
                self.registration_data[chat_id]["height"] = height
                self._ask_weight(chat_id, "registration")
            elif action == "editing":
                self._complete_editing_profile(chat_id, "height", height)
        except ValueError:
            message = self.bot.send_message(chat_id, "❌ Отправь целое число или число с точкой!")
            self.bot.register_next_step_handler(
                message,
                self._get_height,
                action
            )

    def _get_weight(self, message, action: str):
        chat_id = message.chat.id
        try:
            weight = float(message.text)

            if action == "registration":
                self.registration_data[chat_id]["weight"] = weight
                self._ask_activity(chat_id, "registration")
            elif action == "editing":
                self._complete_editing_profile(chat_id, "weight", weight)
        except ValueError:
            message = self.bot.send_message(chat_id, "❌ Отправь целое число или число с точкой!")
            self.bot.register_next_step_handler(message, self._get_weight, action)
        
    def _setup_handlers(self):
        self.bot.register_callback_query_handler(
            self._getter_handler,
            func=lambda callback: callback.data.startswith("get_")
        )
        self.bot.register_callback_query_handler(
            self._profile_editing_handler,
            func=lambda callback: callback.data.startswith("change_")
        )
        
    def _getter_handler(self, callback):
        chat_id = callback.message.chat.id

        _, field, data, action = callback.data.split("_")

        self.bot.delete_message(chat_id, callback.message.message_id)
        if action == "registration":
            self.registration_data[chat_id][field] = data

            if field == "gender":
                self._ask_birth(chat_id, "registration")
            elif field == "activity":
                self._ask_goal(chat_id, "registration")
            elif field == "goal":
                self._complete_registration(chat_id)
        elif action == "editing":
            self._complete_editing_profile(chat_id, field, data)

    def _profile_editing_handler(self, callback):
            _, field = callback.data.split("_")
            chat_id = callback.message.chat.id
            self.bot.delete_message(chat_id, callback.message.message_id)
            match field:
                case "goal":
                    self._ask_goal(chat_id, "editing")
                case "activity":
                    self._ask_activity(chat_id, "editing")
                case "weight":
                    self._ask_weight(chat_id, "editing")
                case "height":
                    self._ask_height(chat_id, "editing")
                case "birth":
                    self._ask_birth(chat_id, "editing")
                case "gender":
                    self._ask_gender(chat_id, "editing")



    @staticmethod
    def _buttons_from_dict(dict: dict):
        markup = types.InlineKeyboardMarkup()
        for button_text, callback in dict.items():
            markup.add(
                types.InlineKeyboardButton(
                    button_text,
                    callback_data=f"{callback}"
                )
            )
        return markup