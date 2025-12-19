from datetime import date

class User:
    GENDER = {
        "male": {
            "discription": "👨‍🦱 Мужской",
            "bmr": 5
        },
        "female": {
            "discription": "👩 Женский",
            "bmr": -161
        }
    }
    ACTIVITIES = {
        "low": {
            "discription": "🛋️ Сидячий образ жизни (минимальная активность)",
            "calories": 1.2
        },
        "light": {
            "discription": "🚶‍♀️ Легкая активность (1-3 тренировки в неделю)",
            "calories": 1.375
        },
        "medium": {
            "discription": "🏃‍♂️ Умеренная активность (3-5 тренировок в неделю)",
            "calories": 1.55
        },
        "high": {
            "discription": "🏋️ Высокая активность (6-7 тренировок в неделю)",
            "calories": 1.725
        },
        "veryHigh": {
            "discription": "⚡ Очень высокая активность (тяжелая физическая работа + тренировки)",
            "calories": 1.9
        }
    }
    GOALS = {
        "lose": {
            "discription": "Похудеть",
            "calories": 0.85,
            "proteins": 1.8
        },
        "maintaining": {
            "discription": "Поддерживать форму",
            "calories": 1,
            "proteins": 1.4
        },
        "gain": {
            "discription": "Набрать мышечную массу",
            "calories": 1.1,
            "proteins": 2
        }
    }

    def __init__(self, user_id: int, gender: str,
                 birth: int, height: float, weight: float,
                 activity: str, goal:str, bmr:float=None,
                 calories:float=None, proteins:float=None,
                 fats:float=None, carbs:float=None):
        self.user_id = user_id
        self.gender = gender
        self.birth = birth
        self.height = height
        self.weight = weight
        self.activity = activity
        self.goal = goal
        self.bmr = bmr if bmr \
            else User._calculate_bmr(self.gender, self.birth, self.weight, self.height)
        self.update_daily_nutriments(calories, proteins, fats, carbs)

    def __str__(self):
        return (
            f"• Пол: {'Мужской' if self.gender == 'male' else 'Женский'}\n"
            f"• Год рождения: {self.birth} г\n"
            f"• Рост: {self.height} см\n"
            f"• Вес: {self.weight} кг\n"
            f"• Активность: {User.ACTIVITIES[self.activity]["discription"]}\n"
            f"• Цель: {User.GOALS[self.goal]["discription"]}"
            f"\n\n🗓 <b>Суточные нормы:</b>\n"
            f"• Калорий в день: {self.calories} ккал\n"
            f"• Белка в день: {self.proteins} г\n"
            f"• Жиров в день: {self.fats} г\n"
            f"• Углеводов в день: {self.carbs} г"
        )



    def update_daily_nutriments(self, calories:float=None, proteins:float=None,
                 fats:float=None, carbs:float=None):
        self.calories = calories if calories \
            else User._calculate_calories(self.bmr, self.activity, self.goal)
        self.proteins = proteins if proteins \
            else User._calculate_proteins(self.weight, self.goal)
        self.fats = fats if fats \
            else User._calculate_fats(self.calories)
        self.carbs = carbs if carbs \
            else User._calculate_carbs(self.calories, self.proteins, self.fats)

    @staticmethod
    def _age(birth: int):
        return date.today().year - birth
    
    @staticmethod
    def _calculate_bmr(gender: str, birth: int, weight: float, height: float):
        age = User._age(birth)
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + User.GENDER[gender]["bmr"]
        return round(bmr, 1)
    
    @staticmethod
    def _calculate_calories(bmr: str, activity: str, goal: str):
        daily_calories = bmr * User.ACTIVITIES[activity]["calories"] * User.GOALS[goal]["calories"]
        return round(daily_calories, 1)
    
    @staticmethod
    def _calculate_proteins(weight: float, goal):
        daily_proteins = weight * User.GOALS[goal]["proteins"]
        return round(daily_proteins, 1)
    
    @staticmethod
    def _calculate_fats(daily_calories: float):
        daily_fats = daily_calories * 0.25 / 9
        return round(daily_fats, 1)
    
    @staticmethod
    def _calculate_carbs(daily_calories: float, daily_proteins: float, daily_fats: float):
        daily_carbs = (daily_calories - (daily_proteins * 4) - (daily_fats * 9)) / 4
        return round(daily_carbs, 1)