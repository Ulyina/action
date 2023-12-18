import sqlite3

class AuctionDatabase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT NOT NULL,
                password TEXT NOT NULL,
                user_type TEXT NOT NULL
            );
        ''')
        self.connection.commit()

    def create_auction_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                auctioneer_id INTEGER,
                item_name TEXT NOT NULL,
                start_bid REAL NOT NULL,
                FOREIGN KEY (auctioneer_id) REFERENCES users(id)
            );
        ''')
        self.connection.commit()

    def create_bid_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bids (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                item_id INTEGER,
                bid_value REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (item_id) REFERENCES items(id)
            );
        ''')
        self.connection.commit()

    def get_item_details(self, item_id):
        self.cursor.execute('SELECT item_name, start_bid FROM items WHERE id=?', (item_id,))
        item_name, start_bid = self.cursor.fetchone()

        # Получение текущей ставки для товара
        self.cursor.execute('SELECT MAX(bid_value) FROM bids WHERE item_id=?', (item_id,))
        current_bid = self.cursor.fetchone()[0] or start_bid

        return item_name, start_bid, current_bid

    def place_bid(self, item_id, bid_value):
        user_id = self.get_user_id(self.logged_in_user_login)
        self.cursor.execute('INSERT INTO bids (user_id, item_id, bid_value) VALUES (?, ?, ?)',
                            (user_id, item_id, bid_value))
        self.connection.commit()

    def add_user(self, login, password, user_type):
        self.cursor.execute('INSERT INTO users (login, password, user_type) VALUES (?, ?, ?)',
                            (login, password, user_type))
        self.connection.commit()

    def check_user_login(self, login, password):
        self.cursor.execute('SELECT * FROM users WHERE login=? AND password=?', (login, password))
        return self.cursor.fetchone() is not None

    def check_auctioneer_login(self, login, password):
        self.cursor.execute('SELECT * FROM users WHERE login=? AND password=? AND user_type="Аукционер"',
                            (login, password))
        return self.cursor.fetchone() is not None

    def add_item(self, auctioneer_id, item_name, start_bid):
        self.cursor.execute('INSERT INTO items (auctioneer_id, item_name, start_bid) VALUES (?, ?, ?)',
                            (auctioneer_id, item_name, start_bid))
        self.connection.commit()

    def get_user_id(self, login):
        self.cursor.execute('SELECT id FROM users WHERE login=?', (login,))
        user_id = self.cursor.fetchone()
        return user_id[0] if user_id else None

    def get_auctioneer_items(self, auctioneer_login):
        auctioneer_id = self.get_user_id(auctioneer_login)
        self.cursor.execute('SELECT item_name, start_bid FROM items WHERE auctioneer_id=?', (auctioneer_id,))
        items = self.cursor.fetchall()
        return [f'{item_name} - Начальная цена: {start_bid}' for item_name, start_bid in items]

    def get_item_id_by_name_and_bid(self, item_name, start_bid):
        self.cursor.execute('SELECT id FROM items WHERE item_name=? AND start_bid=?', (item_name, start_bid))
        item_id = self.cursor.fetchone()
        return item_id[0] if item_id else None

    def get_all_items(self):
        self.cursor.execute('SELECT item_name, start_bid FROM items')
        items = self.cursor.fetchall()
        return [f'{item_name} - Начальная цена: {start_bid}' for item_name, start_bid in items]
