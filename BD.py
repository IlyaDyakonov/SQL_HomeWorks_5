import psycopg2
import time

class Customers:
    def __init__(self, dbname, user, passw):
        self.conn = psycopg2.connect(database=dbname, user=user, password=passw, host='127.0.0.1', port='5432')


    def create(self):                                       # 1. создание таблицы
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                id SERIAL UNIQUE PRIMARY KEY,
                first_name VARCHAR(40) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(386) UNIQUE NOT NULL,
                phone_number VARCHAR(386) []);
            """)
            self.conn.commit()


    def add_client(self, first_name, last_name, email, phone_number = []):   # 2. добавление клиентов
        with self.conn.cursor() as cur:
            cur.execute("""INSERT INTO customers
                (first_name, last_name, email, phone_number)
                VALUES(%s, %s, %s, %s) RETURNING id;""",
                (first_name, last_name, email, phone_number))
            print(f'Клиент {first_name} {last_name} успешно добавлен.')
            self.conn.commit()
        time.sleep(1)
        print("_" * 50)
        print()


    def add_phone(self, last_name, phone_number):                           # 3. добавление номера телефона
        with self.conn.cursor() as cur:
            cur.execute("""SELECT id, phone_number FROM customers WHERE last_name = %s;""",
                        (last_name,))
            row = cur.fetchone()
            if row is not None:
                if phone_number is None:
                    phone_number = [phone_number]
                else:
                    phone_number = [phone_number[0]]
                cur.execute("""UPDATE customers SET phone_number = array_append(phone_number, %s) WHERE last_name = %s;""",
                            (phone_number[0], last_name))
                self.conn.commit()
                print(f'Номер телефона {phone_number} успешно добавлен пользователю {last_name}.')
            else:
                print(f"Клиент с фамилией {last_name} не найден.")
        time.sleep(1)
        print("_" * 50)
        print()


    def change_client(self, id, first_name=None, last_name=None, email=None, phone_number=None): # 4. изменение данных клиента
        with self.conn.cursor() as cur:
            if first_name is not None:
                cur.execute("""UPDATE customers SET first_name = %s WHERE id = %s;""", (first_name, id))
                print(f'Имя успешно обновлено на {first_name}.')
                time.sleep(0.3)
            if last_name is not None:
                cur.execute("""UPDATE customers SET last_name = %s WHERE id = %s;""", (last_name, id))
                print(f'Фамилия успешно обновлена на {last_name}.')
                time.sleep(0.3)
            if email is not None:
                cur.execute("""UPDATE customers SET email = %s WHERE id = %s;""", (email, id))
                print(f'Электронная почта успешно обновлена на {email}.')
                time.sleep(0.3)
            if phone_number is not None:
                cur.execute("""UPDATE customers SET phone_number = %s WHERE id = %s;""", (phone_number, id))
                print(f'Телефон успешно обновлена на {phone_number}.')
                time.sleep(0.3)
            self.conn.commit()
        time.sleep(1)
        print("_" * 50)
        print()


    def delete_phone(self, id, phone_number):           # 5. удаление телефона
        with self.conn.cursor() as cur:
            cur.execute("""UPDATE customers SET phone_number = array_remove(phone_number, %s) WHERE id = %s;""", (phone_number, id))
            print(f"Телефон {phone_number} успешно удалён.")
            self.conn.commit()
        time.sleep(1)
        print("_" * 50)
        print()


    def delete_client(self, id):                 # 6. удаление клиента
        with self.conn.cursor() as cur:
            cur.execute("""DELETE FROM customers WHERE id = %s;""", (id,))
            print(f"Пользователь с id: '{id}' успешно удалён.")
            time.sleep(1)
            print("_" * 50)
            print()
        self.conn.commit()


    def find_client_info(self, first_name=None, last_name=None, email=None, phone_number=None):
        with self.conn.cursor() as cur:
            cur.execute("""SELECT * FROM customers WHERE first_name = %s OR last_name = %s OR email = %s OR phone_number = %s;
            """, (first_name, last_name, email, phone_number))
            result = cur.fetchone()
            if not result:
                time.sleep(1)
                print("Клиент не найден")
            else:
                client_info = {
                    "id": result[0],
                    "first_name": result[1],
                    "last_name": result[2],
                    "email": result[3],
                    "phone_number": result[4]
                }
                print(client_info)
                time.sleep(1)
                print("_" * 50)
        self.conn.commit()


    def close(self):
        self.conn.close()



new_db = Customers("netology_db_hw5", "postgres", "13245342")
new_db.create()

new_db.add_client("Джон", "Сноу", "Snow@gmail.com", ["+7 123 456-7890", "+7 987 654-3210"])
new_db.add_client("Джонни", "Сильверхенд", "Johnny.Silwer@gmail.com", ["+7 123 654-0987"])
new_db.add_client("Петр", "Петров", "petr@gmail.com")

new_db.add_phone("Петров", ["+7 123 758-4873"])

new_db.change_client(3, "Илья", "Дьяконов", "theApuoX@gmail.com", ["+7 123 574-4848"])
new_db.change_client(3, first_name = "Кирилл")

new_db.delete_phone(1, "+7 123 456-7890")

new_db.delete_client(1)

new_db.find_client_info(email = "theApuoX@gmail.com")

new_db.close()