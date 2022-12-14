import sqlite3


class DataBase:
    def __init__(self):
        self.database = sqlite3.connect('shop.db', check_same_thread=False)

    def manager(self, sql, *args,
                fetchone: bool = False,
                fetchall: bool = False,
                commit: bool = False):
        with self.database as db:
            cursor = db.cursor()
            cursor.execute(sql, args)
            if commit:
                result = db.commit()
            if fetchone:
                result = cursor.fetchone()
            if fetchall:
                result = cursor.fetchall()
            return result

    def create_categories_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS categories(
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name VARCHAR(20) UNIQUE
        )
        '''
        self.manager(sql, commit=True)

    def insert_into_categories(self, category_name):
        sql = '''
        INSERT OR IGNORE INTO categories(category_name) VALUES (?)
        '''
        self.manager(sql, category_name, commit=True)

    def create_products_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS products(
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT UNIQUE,
            price INTEGER,
            image TEXT,
            link TEXT,
            characteristics TEXT,
            category_id INTEGER REFERENCES categories(category_id)
        )
        '''
        self.manager(sql, commit=True)

    def get_category_id(self, category_name):
        sql = '''
        SELECT category_id FROM categories WHERE category_name = ?
        '''
        return self.manager(sql, category_name, fetchone=True)[0]

    def insert_into_products(self, product_name, price, image, link, characteristics, category_id):
        sql = '''
        INSERT OR IGNORE INTO 
        products(product_name, price, image, link, characteristics, category_id)
        VALUES (?,?,?,?,?,?)
        '''
        self.manager(sql, product_name, price, image, link, characteristics, category_id, commit=True)

    def create_users_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS users(
            telegram_id BIGINT PRIMARY KEY,
            full_name VARCHAR(100),
            contact VARCHAR(20) UNIQUE
        )
        '''
        # INT - INTEGER -2 147 483 648 ???? 2 147 483 647
        # BIGINT -9.223.372.036.854.775.808 ???? 9.223.372.036.854.775.808
        # TINYINT -128 ???? 127
        self.manager(sql, commit=True)

    def get_user_by_id(self, telegram_id):
        sql = '''SELECT * FROM users WHERE telegram_id = ?'''
        return self.manager(sql, telegram_id, fetchone=True)

    def register_user(self, telegram_id, full_name, contact):
        sql = '''
        INSERT INTO users(telegram_id, full_name, contact) VALUES (?,?,?)
        '''
        self.manager(sql, telegram_id, full_name, contact, commit=True)

    def create_locations(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS locations(
        location_id INTEGER PRIMARY KEY AUTOINCREMENT,
        latitude FLOAT,
        longitude FLOAT,
        location_name TEXT
        )
        '''
        self.manager(sql, commit=True)

    def insert_locations(self):
        sql = '''
        INSERT INTO locations(latitude, longitude, location_name) VALUES 
        (41.26501661724239, 69.20014780886424, '???????????????? 41 ???????????? ???1'),
        (41.29691342529716, 69.27442629920108, '?????????? 14 ???????????? ???2'),
        (41.29757483886135, 69.27379473362318, '?????????? 16 ???????????? ???3')
        '''
        self.manager(sql, commit=True)

    def get_locations(self):
        sql = '''
        SELECT * FROM locations
        '''
        return self.manager(sql, fetchall=True)

    def get_loc_by_name(self, name):
        sql = '''SELECT * FROM locations WHERE location_name = ?'''
        return self.manager(sql, name, fetchone=True)

    def get_categories(self):
        sql = '''SELECT category_name FROM categories'''
        return self.manager(sql, fetchall=True)  # [('12312', ), ('12312, )]

    def get_count_products_in_category(self, category_name):
        sql = '''
        SELECT COUNT(product_id) FROM products
        WHERE category_id = (
            SELECT category_id FROM categories WHERE category_name = ?
        )
        '''
        return self.manager(sql, category_name, fetchone=True)[0]

    def get_products_to_page(self, category_name, offset, limit):
        sql = '''
        SELECT * FROM products
        WHERE category_id = (
            SELECT category_id FROM categories WHERE category_name = ?
        )
        LIMIT ?
        OFFSET ?
        '''
        return self.manager(sql, category_name, limit, offset, fetchall=True)

    def get_detail_product(self, product_id):
        sql = '''
        SELECT * FROM products WHERE product_id = ?
        '''
        return self.manager(sql, product_id, fetchone=True)

    def get_category_name_by_id(self, category_name):
        sql = '''
        SELECT category_name FROM categories WHERE category_id = ?
        '''
        return self.manager(sql, category_name, fetchone=True)[0]
