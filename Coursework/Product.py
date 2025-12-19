class Product:
    def __init__(self, name: str, calories: float,
                 proteins: float, fats: float, carbs: float):
        self.name = name
        self.proteins = proteins
        self.fats = fats
        self.carbs = carbs
        self.calories = calories if calories else self._calculate_calories()
    
    def _calculate_calories(self):
        return round(self.protein * 4 + self.fats * 9 + self.carbs * 4, 1)