import sqlite3
import json
from Product import Product
from typing import List, Optional, Tuple

class MealsDatabase:
    DB_NAME = "meals.sql"
    
    def __init__(self):
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS meals (
                    user_id INTEGER,
                    product TEXT,
                    amount REAL,
                    created_at TIMESTAMP
                )
            ''')
            conn.commit()
    
    def _connection(self):
        return sqlite3.connect(self.DB_NAME)
    
    
    
    def add_meal(self, user_id: int, product: Product, amount: float) -> bool:
        try:
            with self._connection() as conn:
                cursor = conn.cursor()
                
                product_json = json.dumps(product.__dict__)
                
                cursor.execute('''
                    INSERT INTO meals 
                    (user_id, product, amount, created_at)
                    VALUES (?, ?, ?, DATETIME('now', '+3 hours'))
                ''', (user_id, product_json, amount))
                conn.commit()

                self._cleanup_old_records()
                return True
        except Exception as e:
            print(e)
            return False
    
    def get_today_meals(self, user_id: int) -> List[Tuple[Product, float, str]]:
        try:
            with self._connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT product, amount, created_at
                    FROM meals 
                    WHERE user_id = ? 
                    AND date(created_at) = date('now', '+3 hours')
                    ORDER BY created_at DESC
                ''', (user_id,))
                
                meals = []
                for row in cursor.fetchall():
                    product_json, amount, created_at = row
                    try:
                        product = Product(**json.loads(product_json))
                        meals.append((product, amount, created_at))
                    except json.JSONDecodeError:
                        continue
                return meals
        except:
            return []
    
    def get_month_meals(self, user_id: int) -> List[Tuple[Product, float, str]]:
        try:
            with self._connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT product, amount, date(created_at)
                    FROM meals 
                    WHERE user_id = ? 
                    AND date(created_at) >= date('now', '-30 days')
                    ORDER BY created_at DESC
                ''', (user_id,))
                
                meals = []
                for row in cursor.fetchall():
                    product_json, amount, created_at = row
                    try:
                        product = Product(**json.loads(product_json))
                        meals.append((product, amount, created_at))
                    except json.JSONDecodeError:
                        continue
            return meals
        except:
            return []
    
    
    
    def delete_meal(self, user_id: int, created_at: str) -> bool:
        try:
            with self._connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    DELETE FROM meals 
                    WHERE user_id = ? 
                    AND created_at = ?
                ''', (user_id, created_at))
                
                deleted_count = cursor.rowcount
                conn.commit()
                if deleted_count > 0:
                    return True
                else:
                    return False
        except:
            return False
    
    def _cleanup_old_records(self, days_to_keep: int = 31):
        try:
            with self._connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    DELETE FROM meals
                    WHERE date(created_at) < date('now', ?)
                ''', (f'-{days_to_keep} days',))
                conn.commit()
        except:
            pass