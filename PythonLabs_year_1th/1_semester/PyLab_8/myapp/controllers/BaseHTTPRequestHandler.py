from http.server import BaseHTTPRequestHandler
from jinja2 import Environment, PackageLoader, select_autoescape
from models import Author, App, Currency, User, Account
from utils.currencies_api import get_currencies, get_all_currencies
from utils.get_data_currency_3_month import get_data_currency_3_month
import re
from urllib.parse import parse_qs
import json

user_account = Account(False, "duongitmo211", "123456789")

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    # def __init__(self, *args, **kwargs):
    def __init__(self, request, client_address, server):
        self.env = Environment(
            loader=PackageLoader("myapp"),
            autoescape=select_autoescape()
        )
        self.main_author = Author('Dao Manh Duong', 'P3121')
        self.main_app = App("Currencies List App", "1.0.0", self.main_author)
        # super().__init__(*args, **kwargs)
        super().__init__(request, client_address, server)

    def do_GET(self):
        # global result
        if self.path == '/':
            result = self.load_index_page()
        # elif self.path == '/users':
        elif self.path == '/users' and user_account.is_login:
            result = self.load_users_page()
        # elif '/users?id=' in self.path:
        elif '/users?id=' in self.path and user_account.is_login:
            result = self.load_user_page_by_ID(int(self.path.split('?id=')[1]))
        # elif self.path == '/currencies':
        elif self.path == '/currencies' and user_account.is_login:
            result = self.load_all_currencies_page()
        # elif '/currencies?valute=' in self.path:
        elif '/currencies?valute=' in self.path and user_account.is_login:
            result = self.load_currencies_page(self.path.split('?valute=')[1])
        # elif self.path == "/courses":
        elif self.path == "/courses" and user_account.is_login:
            result = self.load_courses_page()
        # elif r'/course?valute=' in self.path:
        elif r'/course?valute=' in self.path and user_account.is_login:
            valute = self.path.split('?valute=')[1]
            date = re.findall(pattern=r'\d+ \w+ \d+', string=self.date_time_string())[0]
            result = self.load_chart(valute.upper(), date)
        elif self.path == '/login':
            result = self.load_login_page()
        elif self.path == '/logout':
            result = self.load_logout_page()
        elif self.path == '/register':
            result = self.load_register_page()
        else:
            # result = self.load_index_page()
            result = self.load_login_page()
        self.send_request_response(result)

    def do_POST(self):
        """Xử lý POST request"""

        try:
            # Lấy độ dài content
            content_length = int(self.headers.get('Content-Length', 0))

            # Đọc body data
            post_data = self.rfile.read(content_length).decode('utf-8')

            # Parse form data (application/x-www-form-urlencoded)
            if self.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
                form_data = parse_qs(post_data)
                # print(form_data)
                # Xử lý theo route
                # if self.path == '/submitted':
                result = self.load_submitted_page(form_data)

                if self.path == '/login' and user_account.is_login == False:
                    result = self.load_login_page()

                self.send_request_response(result)
                # elif self.path == '/login':
                #     result = self.handle_login(form_data)
                # elif self.path == '/register':
                #     result = self.handle_register(form_data)
                # else:
                #     result = self.handle_default_post(form_data)

            # Parse JSON data
            # elif self.headers.get('Content-Type') == 'application/json':
            #     json_data = json.loads(post_data)
            #     result = self.handle_json_post(json_data)
            #
            # else:
            #     result = self.handle_unknown_content_type()

        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")

    def send_request_response(self, result):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(bytes(result, "utf-8"))

    def load_index_page(self):
        template_index = self.env.get_template("index.html")
        # main_author = Author('Dao Manh Duong', 'P3121')
        # main_app = App("Currencies List App", "1.0.0", main_author)
        result = template_index.render(
            myapp_name=self.main_app.name,
            myapp_version=self.main_app.version,
            navigation=[{'caption': 'Основная страница',
                         'href': "/"},
                        {'caption': 'Users',
                         'href': "/users"},
                        {'caption': 'Currencies',
                         'href': "/currencies"},
                        {'caption': 'Courses',
                         'href': "/courses"},
                        {'caption': 'Login' if user_account.is_login == False else 'Logout',
                         'href': "/login" if user_account.is_login == False else '/logout'},
                        ({'caption': 'Create new account',
                         'href': "/register"}) if user_account.is_login == False else None,
                        ],
            author_name=self.main_author.name,
            author_group=self.main_author.group
        )
        return result

    def load_users_page(self, get_user_infor = False):
        template_users = self.env.get_template("users.html")
        # main_author = Author('Dao Manh Duong', 'P3121')
        # main_app = App("Currencies List App", "1.0.0", main_author)
        users = []
        users_infor = [{"id": 1, "name": "Phan Tuan Anh"},
                      {"id": 2, "name": "Duong Nhan Hau"},
                      {"id": 3, "name": "Truong Tuan Kiet"},
                      {"id": 4, "name": "Tang Vu Hoang Nguyen"},
                      {"id": 5, "name": "Chu NGoc Truong"},
                      {"id": 6, "name": "Nguyen Dinh Sinh Phuoc"},
                      {"id": 7, "name": "Nguyen Xuan Canh"},
                      ]
        for infor in users_infor:
            user = User(infor['id'], infor['name'])
            users.append(user)

        result = template_users.render(
            myapp_name=self.main_app.name,
            users=users,
    )
        if get_user_infor: return users_infor
        else: return result

    def load_user_page_by_ID(self, id_:int):
        template_users = self.env.get_template("user_by_id.html")
        # main_author = Author('Dao Manh Duong', 'P3121')
        # main_app = App("Currencies List App", "1.0.0", main_author)
        users_infor = self.load_users_page(get_user_infor = True)
        for infor in users_infor:
            if infor['id'] == id_:
                user = User(infor['id'], infor['name'])

                result = template_users.render(
                    myapp_name=self.main_app.name,
                    user=user,
                )
                return result

        template_user_not_found = self.env.get_template("user_not_found.html")
        result = template_user_not_found.render(myapp_name = self.main_app.name, user_id=id_)
        return result

    def load_currencies_page(self, valute = "USD"):
        template_currencies = self.env.get_template("currencies.html")
        # main_author = Author('Dao Manh Duong', 'P3121')
        # main_app = App("Currencies List App", "1.0.0", main_author)
        # currency = Currency(10, 345, "usD", "DOllAR", 6721.21, 200)

        # currency_list = ['USD', 'EUR', 'GBP', "VND", "Rub"]
        currency_list = [valute.upper()]
        data, date = get_currencies(currency_list)
        currencies = []
        id_ = 0

        for code, value in data.items():
            id_ += 1
            c = Currency(id_=f"R{id_}", num_code= str(id_+123), char_code=code, name=code, value=value, nominal=1)
            currencies.append(c)
        result = template_currencies.render(
            myapp_name=self.main_app.name,
            currency_date = date,
            # author_name=main_author.name,
            # author_group=main_author.group
            # currency_id = currency.id,
            # currency_num_code = currency.num_code,
            # currency_char_code = currency.char_code,
            # currency_name = currency.name,
            # currency_value = currency.value,
            # currency_nominal = currency.nominal,
            currencies=currencies,
        )
        return result

    def load_all_currencies_page(self):
        template_currencies = self.env.get_template("currencies.html")
        # main_author = Author('Dao Manh Duong', 'P3121')
        # main_app = App("Currencies List App", "1.0.0", main_author)
        # currency = Currency(10, 345, "usD", "DOllAR", 6721.21, 200)

        data = get_all_currencies()
        currencies = []
        currency_date = data['@Date']
        for valute in data["Valute"]:
            id_ = valute['@ID']
            numcode = valute['NumCode']
            charcode = valute['CharCode']
            nominal = valute['Nominal']
            name = valute['Name']
            value = valute['Value'].replace(",", ".")
            c = Currency(id_=id_, num_code=str(numcode), char_code=str(charcode), name=str(name), value=float(value), nominal=int(nominal))
            currencies.append(c)
        result = template_currencies.render(
            myapp_name=self.main_app.name,
            currency_date = currency_date,
            # author_name=main_author.name,
            # author_group=main_author.group
            # currency_id = currency.id,
            # currency_num_code = currency.num_code,
            # currency_char_code = currency.char_code,
            # currency_name = currency.name,
            # currency_value = currency.value,
            # currency_nominal = currency.nominal,
            currencies=currencies,
        )
        return result

    def load_courses_page(self):
        login_template = self.env.get_template("chart.html")
        result = login_template.render(
            myapp_name=self.main_app.name,
        )
        return result

    def load_chart(self, valute: str = "USD", date: str = "9/Oct/2025"):
        login_template = self.env.get_template("chart.html")
        day_list, val_list, msg, color_res = get_data_currency_3_month(valute, date)
        # print(day_list)
        # print(val_list)
        result = login_template.render(
            myapp_name=self.main_app.name,
            dayList=day_list,
            valList=val_list,
            valute_name=valute,
            message=msg,
            color_res=color_res,
        )
        return result

    def load_login_page(self):
        login_template = self.env.get_template("login.html")
        result = login_template.render()
        return result

    def load_logout_page(self):
        user_account.is_login = False
        return self.load_index_page()

    def load_register_page(self):
        login_template = self.env.get_template("register.html")
        result = login_template.render()
        return result

    def load_submitted_page(self,form_data):
        username = form_data.get('username', [''])[0]
        password = form_data.get('password', [''])[0]
        # print(username, password)
        if username == user_account.username and f"Encoded password {password}" == user_account.password:
            user_account.is_login = True
            # submitted_template = self.env.get_template("submitted.html")
            # result = submitted_template.render()
            # return result
            print("login successful")
            result = self.load_index_page()
        else:
            print("login failed")
            result = self.env.get_template("login.html").render()

        return result
