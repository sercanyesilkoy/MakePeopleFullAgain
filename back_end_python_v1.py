import sqlite3
from datetime import datetime
import pandas as pd

# Function for Database connection
def get_db_connection():
    return sqlite3.connect('kiosk.db')

# Database setup, tables...
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        income INTEGER NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS meal_logs (
        user_id INTEGER NOT NULL,
        menu_type TEXT NOT NULL,
        time TEXT NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu_counts (
        menu_type TEXT PRIMARY KEY,
        remaining_count INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    INSERT OR IGNORE INTO menu_counts (menu_type, remaining_count) VALUES
    ('low_income_middle_age_menu', 50),
    ('low_income_high_age_menu', 50),
    ('middle_income_low_age_menu', 50),
    ('middle_income_high_age_menu', 50)
    ''')

    conn.commit()
    conn.close()

def insert_user(id, name, age, income, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (id, name, age, income, password) VALUES (?, ?, ?, ?, ?)',
                   (id, name, age, income, password))
    conn.commit()
    conn.close()

def authenticate_user(id, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ? AND password = ?', (id, password))
    user = cursor.fetchone()
    conn.close()
    return user

def log_meal(user_id, menu_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    date = now.strftime("%Y-%m-%d")
    cursor.execute('INSERT INTO meal_logs (user_id, menu_type, time, date) VALUES (?, ?, ?, ?)',
                   (user_id, menu_type, time, date))
    cursor.execute('UPDATE menu_counts SET remaining_count = remaining_count - 1 WHERE menu_type = ?',
                   (menu_type,))
    conn.commit()
    conn.close()

def has_eaten_today(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute('SELECT * FROM meal_logs WHERE user_id = ? AND date = ?', (user_id, today))
    meal_log = cursor.fetchone()
    conn.close()
    return meal_log is not None

def get_meal_count(menu_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT remaining_count FROM menu_counts WHERE menu_type = ?', (menu_type,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_user_details(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def list_tables_and_columns():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query to list all tables #! just for check the Database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    tables_and_columns = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        tables_and_columns[table_name] = columns
    
    conn.close()
    return tables_and_columns

def print_tables_and_columns(tables_and_columns):
    for table_name, columns in tables_and_columns.items():
        print(f"Table: {table_name}")
        for column in columns:
            print(f"  Column: {column[1]}, Type: {column[2]}, Nullable: {column[3]}, Default: {column[4]}, PK: {column[5]}")
        print()

def view_table(table_name):
    conn = get_db_connection()
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# AdminSettings (Monostate Singleton pattern)
class AdminSettings:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        if not self._shared_state:
            self.configure()

    def configure(self, **kwargs):
        self._shared_state.update(kwargs)

    def get_config(self):
        return self._shared_state

    def reset_day(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM meal_logs')
        cursor.execute('UPDATE menu_counts SET remaining_count = 50')
        conn.commit()
        conn.close()
        print("Day reset completed. All records cleared and meal counts reset.")

# Chain of Responsibility Pattern
class EligibilityHandler:
    def __init__(self):
        self._next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    def check(self, request):
        if self._next_handler:
            return self._next_handler.check(request)
        return True


class AccountEligibilityHandler(EligibilityHandler):
    def check(self, request):
        print("AccountEligibilityHandler: Checking account eligibility.")
        return super().check(request)


class AgeEligibilityHandler(EligibilityHandler):
    def check(self, request):
        if request['age'] < 18:
            return f"User {request['name']} is not eligible based on age"
        print("AgeEligibilityHandler: Age check passed.")
        return super().check(request)


class IncomeEligibilityHandler(EligibilityHandler):
    def check(self, request):
        if request['income'] > 20000:
            return f"User {request['name']} is not eligible based on income"
        print("IncomeEligibilityHandler: Income check passed.")
        return super().check(request)


class IsThisPersonExistHandler(EligibilityHandler):
    def check(self, request):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (request['id'],))
        user = cursor.fetchone()
        conn.close()
        if user:
            return f"User {request['name']} already exists"
        print("IsThisPersonExistHandler: Person does not exist in records.")
        return super().check(request)


class LoginEligibilityHandler(EligibilityHandler):
    def check(self, request):
        user = authenticate_user(request['id'], request['password'])
        if not user:
            return "Invalid ID or password"
        print("LoginEligibilityHandler: Login check passed.")
        return super().check(request)


class AlreadyAteHandler(EligibilityHandler):
    def check(self, request):
        if has_eaten_today(request['id']):
            return f"User {request['name']} has already received a meal today"
        print("AlreadyAteHandler: Check passed, user has not eaten today.")
        return super().check(request)


class CapacityHandler(EligibilityHandler):
    def __init__(self, menu_type):
        super().__init__()
        self.menu_type = menu_type

    def check(self, request):
        meal_count = get_meal_count(self.menu_type)
        if meal_count <= 0:
            return f"Meal capacity for {self.menu_type.replace('_', ' ')} has been reached"
        print("CapacityHandler: Capacity check passed.")
        return super().check(request)


# Strategy Pattern
class MenuStrategy:
    def get_menu(self):
        raise NotImplementedError


class LowIncomeMiddleAgeStrategy(MenuStrategy):
    def get_menu(self):
        return "low_income_middle_age_menu"


class LowIncomeHighAgeStrategy(MenuStrategy):
    def get_menu(self):
        return "low_income_high_age_menu"


class MiddleIncomeLowAgeStrategy(MenuStrategy):
    def get_menu(self):
        return "middle_income_low_age_menu"


class MiddleIncomeHighAgeStrategy(MenuStrategy):
    def get_menu(self):
        return "middle_income_high_age_menu"


# Menu Factory for creating the appropriate strategy #! not sure would be edit to use factory pattern
class MenuFactory:
    def get_menu_strategy(self, user):
        if user['income'] < 20000 and 18 <= user['age'] <= 45:
            return LowIncomeMiddleAgeStrategy()
        elif user['income'] < 20000 and user['age'] > 45:
            return LowIncomeHighAgeStrategy()
        elif user['income'] >= 20000 and user['age'] <= 45:
            return MiddleIncomeLowAgeStrategy()
        else:
            return MiddleIncomeHighAgeStrategy()


# Facade pattern
class KioskFacade:
    def __init__(self):
        self.admin_settings = AdminSettings()
        self.menu_factory = MenuFactory()
        self.create_account_chain()

    def create_account_chain(self):
        self.account_eligibility_handler = AccountEligibilityHandler()
        self.age_handler = self.account_eligibility_handler.set_next(AgeEligibilityHandler())
        self.income_handler = self.age_handler.set_next(IncomeEligibilityHandler())
        self.is_this_person_exist_handler = self.income_handler.set_next(IsThisPersonExistHandler())

    def login_chain(self, user):
        self.login_eligibility_handler = LoginEligibilityHandler()
        self.already_ate_handler = self.login_eligibility_handler.set_next(AlreadyAteHandler())
        menu_strategy = self.assign_menu(user)
        self.capacity_handler = self.already_ate_handler.set_next(CapacityHandler(menu_strategy.get_menu()))

    def start(self):
        self.admin_settings.configure()
        print("Starting kiosk...")

    def check_eligibility(self, user, action):
        if action == "create_account":
            result = self.account_eligibility_handler.check(user)
        elif action == "login":
            full_user = get_user_details(user['id'])
            if full_user:
                user.update({
                    'age': full_user[2],
                    'income': full_user[3],
                })
                self.login_chain(user)
                result = self.login_eligibility_handler.check(user)
            else:
                result = "User not found"
        else:
            result is True  # Assume admin login or other actions are always allowed for simplicity
        if result is True:
            return True
        else:
            print(result)
            return False

    def create_account(self, user):
        if self.check_eligibility(user, "create_account"):
            insert_user(user['id'], user['name'], user['age'], user['income'], user['password'])
            print(f"User {user['name']} has been successfully registered.")
        else:
            print(f"User {user['name']} could not be registered.")

    def login(self, user):
        if self.check_eligibility(user, "login"):
            full_user = get_user_details(user['id'])
            if full_user:
                user.update({
                    'age': full_user[2],
                    'income': full_user[3],
                })
                menu_strategy = self.assign_menu(user)
                self.record_meal(user, menu_strategy)
                print(f"User {user['name']} has logged in and received a meal.")
            else:
                print(f"User {user['name']} not found in the database.")
        else:
            print(f"User {user['name']} could not log in.")

    def record_meal(self, user, menu_strategy):
        log_meal(user['id'], menu_strategy.get_menu())
        print(f"Recorded meal for user {user['name']}: {menu_strategy.get_menu()}")

    def finish_meal(self, user):
        print(f"User {user['name']} has finished their meal")

    def get_menu_description(self, menu_item):
        return menu_item.get_description()

    def assign_menu(self, user):
        return self.menu_factory.get_menu_strategy(user)


# MenuItem #! may change/delete
class MenuItem:
    def __init__(self, description):
        self.description = description

    def get_description(self):
        return self.description
