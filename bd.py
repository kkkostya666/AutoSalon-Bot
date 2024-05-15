import sqlite3

class Db:
    def __init__(self, db_name="freelance.db"):
        self.connection = sqlite3.connect(db_name)
        self.connection.isolation_level = None  # Автоматически фиксируем изменения
        self.cursor = self.connection.cursor()
        self.connection.execute('pragma foreign_keys=ON')

    def create_table_auto(self):
        with self.connection:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS auto (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code UNIQUE,
                    name_auto TEXT,
                    price TEXT,
                    description TEXT,
                    img TEXT,
                    kolvo REAL,
                    engine_power REAL
                );
            """)
            print("[INFO] Table auto created successfully")

    def select_id_by_name_auto(self, name_auto):
        with self.connection:
            self.cursor.execute("""
                SELECT id FROM auto WHERE name_auto = ?;
            """, (name_auto,))
            row = self.cursor.fetchone()
            if row:
                return row[0]  # Возвращает только первый id, если он найден
            else:
                return None  # Если запись не найдена, возвращается None

    def create_table_kategory(self):
        with self.connection:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS kategory (
                    id_kategory INTEGER PRIMARY KEY AUTOINCREMENT,
                    name_kategory TEXT
                );
            """)
            print("[INFO] Table kategory created successfully")

    def create_table_order(self):
        with self.connection:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    auto_id INTEGER,
                    status TEXT,
                    FOREIGN KEY (user_id) REFERENCES user(id),
                    FOREIGN KEY (auto_id) REFERENCES auto(id)
                );
            """)
            print("[INFO] Table orders created successfully")

    def create_table_user(self):
        with self.connection:
            self.cursor.execute("""
                 CREATE TABLE IF NOT EXISTS user (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     username TEXT
                 );
             """)
            print("[INFO] Table user created successfully")

    def select_all_auto_data(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM auto;")
            rows = self.cursor.fetchall()
            print(rows)
            return rows

    def insert_order(self, user_id, auto_id, status):
        with self.connection:
            self.cursor.execute("""
                INSERT INTO orders (user_id, auto_id, status)
                VALUES (?, ?, ?);
            """, (user_id, auto_id, status))

    def create_table_auto_kategory(self):
        with self.connection:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS auto_kategory (
                    id_auto INTEGER,
                    id_kategory INTEGER,
                    FOREIGN KEY (id_auto) REFERENCES auto(id),
                    FOREIGN KEY (id_kategory) REFERENCES kategory(id_kategory),
                    PRIMARY KEY (id_auto, id_kategory)
                );
            """)
            print("[INFO] Table auto_kategory created successfully")

    def insert_category(self, category):
        with self.connection:
            self.cursor.execute("""
                INSERT INTO kategory (name_kategory)
                VALUES (?)
            """, (category,))
            print("[INFO] Category data inserted successfully")

    def select_category(self):
        with self.connection:
            self.cursor.execute("""
                SELECT * FROM kategory;
            """)
            user_codes = self.cursor.fetchall()
            return user_codes

    def delete_category_by_id(self, category_id):
        with self.connection:
            self.cursor.execute("""
                DELETE FROM kategory
                WHERE id_kategory = ?
            """, (category_id,))
            print("[INFO] Category deleted successfully")

    def fill_auto_table(self, uniqie_code, name_auto, price, description, img, kolvo, engine_power):
        with self.connection:
            self.cursor.execute("""
                INSERT INTO auto (code ,name_auto, price, description, img, kolvo, engine_power)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (uniqie_code, name_auto, price, description, img, kolvo, engine_power))
            print("[INFO] Data inserted into auto table successfully")

    def insert_auto_category_table(self, auto_id, category_id):
        with self.connection:
            self.cursor.execute("""
                INSERT INTO auto_kategory (id_auto, id_kategory)
                        VALUES (?, ?)
             """, (auto_id, category_id))
            print("[INFO] Data inserted into auto table successfully")

    def select_auto_code(self, code):
        with self.connection:
            self.cursor.execute("""
                SELECT id FROM auto WHERE code = ?;
            """, (code,))
            user_codes = self.cursor.fetchall()
            print(user_codes)
            return user_codes



    def add_user(self, username):
        with self.connection:
            self.cursor.execute("""
                INSERT INTO user (username) VALUES (?);
            """, (username,))
            print(f"[INFO] User '{username}' added successfully")

    def select_all_orders_with_details(self):
        with self.connection:
            self.cursor.execute("""
                SELECT orders.id, user.username, auto.name_auto, auto.price, auto.description, auto.img, auto.kolvo, auto.engine_power, orders.status
                FROM orders
                INNER JOIN user ON orders.user_id = user.id
                INNER JOIN auto ON orders.auto_id = auto.id;
            """)
            rows = self.cursor.fetchall()
            return rows

    def select_all_orders_with_details_user(self, username):
        with self.connection:
            self.cursor.execute("""
                SELECT orders.id, user.username, auto.name_auto, auto.price, auto.description, auto.img, auto.kolvo, auto.engine_power, orders.status
                FROM orders
                INNER JOIN user ON orders.user_id = user.id
                INNER JOIN auto ON orders.auto_id = auto.id
                WHERE user.username = ?;
            """, (username,))
            rows = self.cursor.fetchall()
            print(rows)
            return rows

    def update_order_status(self, order_id, new_status):
        with self.connection:
            sql_query = "UPDATE orders SET status = ? WHERE id = ?"
            self.cursor.execute(sql_query, (new_status, order_id))



db = Db()
# db.select_auto_code('32c1e77c')
# db.select_all_auto_category_data()
# db.create_table_user()
# db.add_user("kkkostya666")
# db.create_table_order()
# db.create_table_auto()
# db.create_table_kategory()
# db.create_table_auto_kategory()
# db.select_id_by_name_auto("Lada Granta")
db.select_all_orders_with_details_user("kkkostya666")
