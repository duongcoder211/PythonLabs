import requests
import xmltodict
import xml.parsers

def get_currencies(currency_codes: list,
                   url: str = "https://www.cbr.ru/scripts/XML_daily.asp?date_req=09.10.2025") -> tuple[dict[str, float], str]: #dict[str, float]:

    """
    Получает курсы валют с API Центробанка России.

    Args:
        currency_codes (list): Список символьных кодов валют (например, ['USD', 'EUR']).

    Returns:
        dict: Словарь, где ключи - символьные коды валют, а значения - их курсы.
              Возвращает None в случае ошибки запроса.
    """
    try:
        response = requests.get(url)
        # print(response.url, response.status_code, response.text, response.content)
        response.raise_for_status()  # Проверка на ошибки HTTP
        # data = response.json()
        data = xmltodict.parse(response.text)
        # print(data)
        date = url.split("?date_req=")[1]
        currencies = {}

        if "ValCurs" in data:
            if data["ValCurs"]["Valute"]:
                new_data_dict = {c["CharCode"]: c for c in data["ValCurs"]["Valute"]}
                for code in currency_codes:
                    if code.upper() in new_data_dict:
                        currencies[code.upper()] = float(new_data_dict[code.upper()]["Value"].replace(",", "."))
                    else:
                        currencies[code.upper()] = f"Код валюты '{code}' не найден."
        # print(currencies)
        return currencies, date

    except requests.exceptions.RequestException as re:
        # print(f"Ошибка при запросе к API: {re}", file=handle)
        # handle.write(f"Ошибка при запросе к API: {re}\n")
        # raise requests.exceptions.RequestException('Упали с исключением')
        raise requests.exceptions.RequestException(f"Ошибка при запросе к API: {re}\n")

    # except requests.exceptions.ConnectionError as ce:
    #     # handle.write(f"API недоступен: {ce}\n")
    #     raise requests.exceptions.ConnectionError(f"API недоступен: {ce}\n")

    except xml.parsers.expat.ExpatError as ee:
        # handle.write(f"Некорректный XML: {ee}\n")
        raise xml.parsers.expat.ExpatError(f"Некорректный XML: {ee}\n")

    except KeyError as ke:
        # handle.write(f"Нет ключа “Valute”: {ke}\n")
        raise KeyError(f"Нет ключа “Valute”: {ke}\n")

    except TypeError as te:
        # handle.write(f"Курс валюты имеет неверный тип: {te}\n")
        raise TypeError(f"Курс валюты имеет неверный тип: {te}\n")

def get_all_currencies(url: str = "https://www.cbr.ru/scripts/XML_daily.asp?date_req=09.10.2025") -> list[str, list[dict]]:
    """
        Получает курсы валют с API Центробанка России в течение сутки.

        Args:
            url: сылка в централный российский банк

        Returns:
            dict: Словарь всех курсов
        """

    try:
        response = requests.get(url)
        # print(response.url, response.status_code, response.text, response.content)
        response.raise_for_status()  # Проверка на ошибки HTTP
        # data = response.json()
        data = xmltodict.parse(response.text)
        # print(data)

        if "ValCurs" in data:
            return data["ValCurs"]

    except requests.exceptions.RequestException as re:
        # print(f"Ошибка при запросе к API: {re}", file=handle)
        # handle.write(f"Ошибка при запросе к API: {re}\n")
        # raise requests.exceptions.RequestException('Упали с исключением')
        raise requests.exceptions.RequestException(f"Ошибка при запросе к API: {re}\n")

    # except requests.exceptions.ConnectionError as ce:
    #     # handle.write(f"API недоступен: {ce}\n")
    #     raise requests.exceptions.ConnectionError(f"API недоступен: {ce}\n")

    except xml.parsers.expat.ExpatError as ee:
        # handle.write(f"Некорректный XML: {ee}\n")
        raise xml.parsers.expat.ExpatError(f"Некорректный XML: {ee}\n")

    except KeyError as ke:
        # handle.write(f"Нет ключа “Valute”: {ke}\n")
        raise KeyError(f"Нет ключа “Valute”: {ke}\n")

    except TypeError as te:
        # handle.write(f"Курс валюты имеет неверный тип: {te}\n")
        raise TypeError(f"Курс валюты имеет неверный тип: {te}\n")

# print(get_currencies(["usd"]))
# print(get_all_currencies())