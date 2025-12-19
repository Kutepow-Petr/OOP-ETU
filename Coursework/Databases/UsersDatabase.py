import sqlite3
import json
from User import User

class UsersDatabase:
    DB_NAME = "users.sql"

    def __init__(self):
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER UNIQUE NOT NULL,
                    user_data TEXT NOT NULL
                )
            ''')
            conn.commit()

    def _connection(self):
        return sqlite3.connect(self.DB_NAME)
    


    def add_user(self, user: User) -> bool:
        try:
            with self._connection() as conn:
                cursor = conn.cursor()

                user_json = json.dumps(user.__dict__)

                cursor.execute('''
                    INSERT OR REPLACE INTO users
                    (user_id, user_data)
                    VALUES (?, ?)
                ''', (user.user_id, user_json))
                conn.commit()
                return True
        except:
            return False
    
    def get_user(self, user_id: int) -> User:
        try:
            with self._connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT user_data FROM users WHERE user_id = ?
                ''', (user_id,))

                user_json = cursor.fetchone()[0]
                if user_json:
                    try:
                        return User(**json.loads(user_json))
                    except json.JSONDecodeError:
                        return None
        except:
            return None