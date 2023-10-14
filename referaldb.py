import sqlite3

class DataBase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))
        
    def add_user(self, user_id, referrer_id=None):
        with self.connection:
            if referrer_id != None:
                return self.cursor.execute("INSERT INTO users (user_id, referrer_id) VALUES (?, ?)", (user_id, referrer_id,))
            else:
                return self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
    
    def count_referals(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(id) as count FROM users WHERE referrer_id = ?", (user_id,)).fetchone()[0]
        
    def change_balance(self, user_id, referrer_id, refferer_money):
        with self.connection:
            return self.cursor.execute("UPDATE users SET refferer_money = ? WHERE user_id = ? AND referrer_id = ?", (refferer_money, user_id, referrer_id)).fetchall()
        
    def start_message(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT refferer_money FROM users WHERE user_id = ? ", (user_id,)).fetchall()
        
    def change_win(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT win_or_lose FROM users WHERE user_id = ?", (user_id,)).fetchall()
        
    def show_balance(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT refferer_money FROM users WHERE user_id = ?", (user_id,)).fetchall()
    
    def change_win_upd(self, win_or_lose, user_id, refferer_id):
        with self.connection:
            return self.cursor.execute('UPDATE users SET win_or_lose = ? WHERE user_id = ? AND referrer_id = ?', (win_or_lose, user_id, refferer_id)).fetchall()
        
    def change_balance_plus(self, ref_money, user_id):
        with self.connection:
            return self.cursor.execute('UPDATE users SET refferer_money = refferer_money + ? WHERE user_id = ?', (ref_money, user_id,)).fetchone()
    def change_balance_minus(self, ref_money, user_id):
        with self.connection:
            return self.cursor.execute('UPDATE users SET refferer_money = refferer_money - ? WHERE user_id = ?', (ref_money, user_id,)).fetchone()
    def withdrawals(self, ref_money, user_id):
        with self.connection:
            return self.cursor.execute('UPDATE users SET refferer_money = refferer_money - ? WHERE user_id = ?', (ref_money, user_id,)).fetchone()
    