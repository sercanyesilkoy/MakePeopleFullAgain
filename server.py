from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import sqlite3
from datetime import datetime
import pandas as pd

# Flask 앱 초기화
app = Flask(__name__)
api = Api(app)

# Database connection
def get_db_connection():
    return sqlite3.connect('kiosk.db', timeout=10)

# Database setup
def create_tables():
    with get_db_connection() as conn:
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

create_tables()

# Helper functions
def insert_user(id, name, age, income, password):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (id, name, age, income, password) VALUES (?, ?, ?, ?, ?)',
                       (id, name, age, income, password))
        conn.commit()

def authenticate_user(id, password):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ? AND password = ?', (id, password))
        user = cursor.fetchone()
    return user

def log_meal(user_id, menu_type):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        date = now.strftime("%Y-%m-%d")
        cursor.execute('INSERT INTO meal_logs (user_id, menu_type, time, date) VALUES (?, ?, ?, ?)',
                       (user_id, menu_type, time, date))
        cursor.execute('UPDATE menu_counts SET remaining_count = remaining_count - 1 WHERE menu_type = ?',
                       (menu_type,))
        conn.commit()

def has_eaten_today(user_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute('SELECT * FROM meal_logs WHERE user_id = ? AND date = ?', (user_id, today))
        meal_log = cursor.fetchone()
    return meal_log is not None

def get_meal_count(menu_type):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT remaining_count FROM menu_counts WHERE menu_type = ?', (menu_type,))
        count = cursor.fetchone()[0]
    return count

def get_user_details(user_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, age, income, password FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
    
    if user:
        return {
            'id': user[0],
            'name': user[1],
            'age': user[2],
            'income': user[3],
            'password': user[4]
        }
    return None

def list_tables_and_columns():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Query to list all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        tables_and_columns = {}
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            tables_and_columns[table_name] = columns
    
    return tables_and_columns

def print_tables_and_columns(tables_and_columns):
    for table_name, columns in tables_and_columns.items():
        print(f"Table: {table_name}")
        for column in columns:
            print(f"  Column: {column[1]}, Type: {column[2]}, Nullable: {column[3]}, Default: {column[4]}, PK: {column[5]}")
        print()

def view_table(table_name):
    with get_db_connection() as conn:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, conn)
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
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM meal_logs')
            cursor.execute('UPDATE menu_counts SET remaining_count = 50')
            conn.commit()
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

# Menu Factory for creating the appropriate strategy
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

    def create_login_chain(self, menu_type):
        self.login_handler = LoginEligibilityHandler()
        self.already_ate_handler = self.login_handler.set_next(AlreadyAteHandler())
        self.capacity_handler = self.already_ate_handler.set_next(CapacityHandler(menu_type))

    def create_account(self, id, name, age, income, password):
        user = {'id': id, 'name': name, 'age': age, 'income': income, 'password': password}
        result = self.account_eligibility_handler.check(user)
        if result is True:
            insert_user(id, name, age, income, password)
            return f"User {name} created successfully"
        else:
            return result

    def login(self, id, password):
        user = get_user_details(id)
        if not user:
            return "User not found"

        menu_strategy = self.menu_factory.get_menu_strategy(user)
        menu_type = menu_strategy.get_menu()
        self.create_login_chain(menu_type)
        request = {'id': id, 'name': user['name'], 'age': user['age'], 'income': user['income'], 'password': password}
        result = self.login_handler.check(request)
        if result is True:
            log_meal(id, menu_type)
            return f"Meal provided to user {user['name']}: {menu_type.replace('_', ' ')}"
        else:
            return result

    def reset_day(self):
        self.admin_settings.reset_day()

# Flask API Resources
class CreateUser(Resource):
    def post(self):
        data = request.get_json()
        id = data.get('id')
        name = data.get('name')
        age = data.get('age')
        income = data.get('income')
        password = data.get('password')

        kiosk = KioskFacade()
        result = kiosk.create_account(id, name, age, income, password)
        return jsonify({'message': result})

class LoginUser(Resource):
    def post(self):
        data = request.get_json()
        id = data.get('id')
        password = data.get('password')

        kiosk = KioskFacade()
        result = kiosk.login(id, password)
        return jsonify({'message': result})

class ResetDay(Resource):
    def post(self):
        kiosk = KioskFacade()
        kiosk.reset_day()
        return jsonify({'message': 'Day reset completed. All records cleared and meal counts reset.'})

# API 엔드포인트 등록
api.add_resource(CreateUser, '/create_user')
api.add_resource(LoginUser, '/login')
api.add_resource(ResetDay, '/reset_day')

if __name__ == '__main__':
    app.run(debug=True)
