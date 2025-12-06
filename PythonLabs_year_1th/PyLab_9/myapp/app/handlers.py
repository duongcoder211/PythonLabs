from urllib.parse import parse_qs, urlparse
import json
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)

def render_template(template_name : str, context : dict = None):
    """Рендеринг HTML шаблона"""
    if context is None:
        context = {}
    template = env.get_template(template_name)
    return template.render(**context)

# Базовый обработчик
class BaseHandler:
    def __init__(self, request_handler):
        self.request_handler = request_handler
        self.template = "index.html"

    def get_query_params(self):
        """Получить параметры запроса"""
        parsed_url = urlparse(self.request_handler.path)
        return parse_qs(parsed_url.query)

    def get_post_data(self):
        """Получить данные POST запроса"""
        content_length = int(self.request_handler.headers.get('Content-Length', 0))
        post_data = self.request_handler.rfile.read(content_length)
        return parse_qs(post_data.decode('utf-8'))

# Главная страница
class HomeHandler(BaseHandler):
    def handle(self):
        context = {
            "myapp_name": "CurrenciesListApp",
            "navigation": [
                {'caption': 'Основная страница', 'href': "/"},
                {'caption': 'Об авторе', 'href': '/author'},
                {'caption': 'Пользователи', 'href': "/users"},
                {'caption': 'Валюты', 'href': "/currencies"},
                {'caption': 'Войти', 'href': "/login"},
                {'caption': 'Регистрация', 'href': "/register"}
            ],
            "author_name": self.request_handler.main_author.name,
            "author_group": self.request_handler.main_author.group,
            "currencies": self.request_handler.c_r_controller._read()
        }
        return render_template(self.template, context)