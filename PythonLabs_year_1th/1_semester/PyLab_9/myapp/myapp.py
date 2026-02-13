from jinja2 import Environment, PackageLoader, select_autoescape
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from controllers.databasecontroller import CurrencyRatesCRUD, UserCRUD
from models import Author, App, User
from utils.currencies_api import get_all_currencies, get_currencies

env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)

main_author = Author('Dao Manh Duong', 'P3121')
app = App("CurrenciesListApp", "1.0.0 Mega", main_author)

class CurrencyRatesMock:
    def __init__(self):
        # self.__values = [("USD", "90"),
        #                  ("EUR", "91"),
        #                  ("GBP", '100'),
        #                  ("AUD", '52.8501')]
        res = get_all_currencies()
        if 'Valute' in res:
            self.__values = res['Valute']
        else:
            self.__values = []
    @property
    def values(self):
        return self.__values

class UserMock:
    def __init__(self):
        self.__values = ["Duong Nhan Hau",
                         "Phan Tuan Anh",
                         "Chu Ngoc Truong",
                         "Truong Tuan Kiet",
                         "Tang Vu Hoang Nguyen",
                         "Nguyen Xuan Canh",
                         "Toi Ten Foo",
                         "Toi Ten Bar",
                         "No Name"
                        ]


    @property
    def values(self):
        return self.__values

c_r = CurrencyRatesMock()
c_r_controller = CurrencyRatesCRUD(c_r)
c_r_controller._create()
# print(c_r.values)

user_mock = UserMock()
user_mock_controller = UserCRUD(user_mock)
user_mock_controller._create()
# print(user_mock.values)
# print(user_mock_controller._read())

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    # Định nghĩa router: path -> handler method
    ROUTES = {
        '/': "handle_index", # root url
        '/author': "handle_author",
        '/users': "handle_users",
        '/user': {"func": "handle_user_show", "params": ["query_dict"]},
        '/user/show': "handle_user_show",
        '/user/update': {"func": "handle_user_update", "params": ["query_dict"]},
        '/user/delete': {"func": "handle_user_delete", "params": ["query_dict"]},
        '/currencies': "handle_currencies",
        '/currency/show': "handle_currency_show",
        '/currency/update': {"func": "handle_currency_update", "params": ["query_dict"]},
        '/currency/delete': {"func": "handle_currency_delete", "params": ["query_dict"]},
        '/login': "handle_login",
        '/register': "handle_register",
    }
    def do_GET(self):
        #method 1
        parsed_url = urlparse(self.path)
        # print(parsed_url)           #/currencies?id=10 => ParseResult(scheme='', netloc='', path='/currencies', params='', query='id=10', fragment='')
        # print(parsed_url.path)             #/currencies?id=10&name=duong => /currencies
        # print(parsed_url.query)            #/currencies?id=10&name=duong => {'id': ['10'], 'name': ['duong']}

        #method 2
        url_query_dict = parse_qs(self.path.rpartition('?')[-1])
        # print(url_query_dict)       #{'id': ['10']}

        if parsed_url.path in self.ROUTES:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')

            # handler = self.ROUTES[parsed_url.path] #  "handle_index"
            # result = handler() #dont work because noncallable "handle_index"()
            if isinstance(self.ROUTES[parsed_url.path], str):
                handler = getattr(self, self.ROUTES[parsed_url.path]) #get attribute by name (string)
                result = handler()
            else:
                handler = getattr(self, self.ROUTES[parsed_url.path]["func"]) #get attribute by name (string)
                result = handler(url_query_dict)

            self.end_headers()
            self.wfile.write(bytes(result, "utf-8"))
        else:
            self.send_response(404)
            result = self.handle_404()
            self.end_headers()
            self.wfile.write(bytes(result, "utf-8"))

    def handle_index(self):
        index_template = env.get_template("index.html")
        result = index_template.render(
            myapp_name=app.name,
            author_name=main_author.name,
            author_group=main_author.group,
            navigation=[{'caption': 'Основная страница', 'href': "/"},
                        {'caption': 'Об авторе', 'href': '/author'},
                        {'caption': 'Пользователи', 'href': "/users"},
                        {'caption': 'Валюты', 'href': "/currencies"},
                        {'caption': 'Войти', 'href': "/login"},
                        {'caption': 'Регистрация', 'href': "/register"}
                        ],
        )
        return result

    def handle_author(self):
        author_template = env.get_template("author.html")
        result = author_template.render(
            myapp_name=app.name,
            author_name=main_author.name,
            author_group=main_author.group,
        )
        return result

    def handle_users(self, res: tuple= None):
        author_template = env.get_template("users.html")
        result = author_template.render(
            myapp_name=app.name,
            users=user_mock_controller._read(),
            msg = res[0] if res else "",
            msg_color = res[1] if res else "",
        )
        return result
    
    def handle_user_show(self, query_dict: dict):
        currencies_template = env.get_template("user.html")
        result = currencies_template.render(
            myapp_name=app.name,
            author_name=main_author.name,
            author_group=main_author.group,
            user=user_mock_controller._read(query_dict),
        )
        return result
        # result = self.handle_users()
        # return result

    def handle_user_update(self, query_dict: dict):
        dict_key = list(query_dict.keys())[0].upper()
        dict_value = query_dict[list(query_dict.keys())[0]][0]

        c_r_controller._update({dict_key: dict_value})
        msg, msg_color = f'Обновление валюта {dict_key} с значением {dict_value} завершено', "green"
        result = self.handle_currencies(tuple([msg, msg_color]))
        return result

    def handle_user_delete(self, query_dict: dict):
        c_r_controller._delete(query_dict['id'][0])
        result = self.handle_currencies()
        return result

    def handle_currencies(self, res: tuple= None):
        currencies_template = env.get_template("currencies.html")
        result = currencies_template.render(
            myapp_name=app.name,
            author_name=main_author.name,
            author_group=main_author.group,
            currencies=c_r_controller._read(),
            msg = res[0] if res else "",
            msg_color = res[1] if res else "",
        )
        return result

    def handle_currency_show(self):
        result = self.handle_currencies()
        return result

    def handle_currency_update(self, query_dict: dict):
        # c_r_controller._update(query_dict['id'][0])
        # localhost:8080/currencies/update?usd=100000.100

        # query_dict = {'usd', [12345.67]} => "USD", 12345.67
        dict_key = list(query_dict.keys())[0].upper()
        dict_value = query_dict[list(query_dict.keys())[0]][0]

        c_r_controller._update({dict_key: dict_value})
        msg, msg_color = f'Обновление валюта {dict_key} с значением {dict_value} завершено', "green"
        result = self.handle_currencies(tuple([msg, msg_color]))
        return result

    def handle_currency_delete(self, query_dict: dict):
        # print(self.path.rpartition('?')[-1])
        c_r_controller._delete(query_dict['id'][0])
        # print(user_params_dict['id'][0])
        # c_r_controller._delete(user_id = )
        result = self.handle_currencies()
        return result

    def handle_login(self):
        login_template = env.get_template("login.html")
        result = login_template.render(
            myapp_name=app.name,
        )
        return result

    def handle_register(self):
        register_template = env.get_template("register.html")
        result = register_template.render(
            myapp_name=app.name,
        )
        return result

    def handle_404(self):
        error404_template = env.get_template("error404.html")
        result = error404_template.render()
        return result

if __name__ == "__main__":
    httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    print('server is running')
    httpd.serve_forever()