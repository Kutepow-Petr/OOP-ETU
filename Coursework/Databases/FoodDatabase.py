import sqlite3
import json
from typing import List
from Product import Product

class FoodDatabase:
    DB_NAME = "foods.sql"

    def __init__(self):
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS foods (
                    product_name TEXT UNIQUE,
                    product TEXT,
                    created_at TIMESTAMP
                )
            ''')
            conn.commit()

    def _connection(self):
        return sqlite3.connect(self.DB_NAME)
    

    
    def add_product(self, product: Product) -> bool:
        try:
            with self._connection() as conn:
                cursor = conn.cursor()
                
                product_json = json.dumps(product.__dict__)
                
                cursor.execute('''
                    INSERT OR REPLACE INTO foods
                    (product_name, product, created_at)
                    VALUES (?, ?, DATETIME('now'))
                ''', (product.name, product_json))
                conn.commit()

                self.cleanup_old_records()
                return True
        except:
            return False
    
    def search(self, query: str) -> List[Product]:
        try:
            with self._connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT product FROM foods 
                    WHERE product_name LIKE ?
                    ORDER BY created_at DESC
                    LIMIT ?
                ''', (f"%{query}%", 20))
                
                results = []
                for (product_json,) in cursor.fetchall():
                    try:
                        product = Product(**json.loads(product_json))
                        results.append(product)
                    except:
                        continue
                
                return results
        except:
            return []
        


    def cleanup_old_records(self, days_to_keep: int = 90) -> int:
        try:
            with self._connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    DELETE FROM foods 
                    WHERE date(created_at) < date('now', ?)
                ''', (f'-{days_to_keep} days',))
                conn.commit()     
        except:
            pass