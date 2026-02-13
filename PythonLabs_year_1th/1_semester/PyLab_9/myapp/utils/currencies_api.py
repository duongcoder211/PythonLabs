import requests
import xmltodict
import xml.parsers

def get_all_currencies(url: str = "https://www.cbr.ru/scripts/XML_daily.asp?date_req=09.10.2025") -> dict[str, str | list[dict[str, str | float]]]:
    """
        Получает курсы валют с API Центробанка России в течение сутки.

        Args:
            url: сылка в централный российский банк

        Returns:
            dict: Словарь всех курсов
        """

    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = xmltodict.parse(response.text)

        if "ValCurs" in data:
            return data["ValCurs"]

    except requests.exceptions.RequestException as re:
        raise requests.exceptions.RequestException(f"Ошибка при запросе к API: {re}\n")

    except xml.parsers.expat.ExpatError as ee:
        raise xml.parsers.expat.ExpatError(f"Некорректный XML: {ee}\n")

    except KeyError as ke:
        raise KeyError(f"Нет ключа “Valute”: {ke}\n")

    except TypeError as te:
        raise TypeError(f"Курс валюты имеет неверный тип: {te}\n")

def get_currencies(currency_codes: list, url: str = "https://www.cbr.ru/scripts/XML_daily.asp?date_req=09.10.2025") -> tuple[dict[str, float], str]:
    """
    #     Получает курсы валют с API Центробанка России.
    #
    #     Args:
    #         currency_codes (list): Список символьных кодов валют и дата (например, (['USD', 'EUR'])).
    #
    #     Returns:
    #         dict: Словарь, где ключи - символьные коды валют, а значения - их курсы.
    #               Возвращает None в случае ошибки запроса.
    #     """
    currencies = {}
    data = get_all_currencies(url)
    date = url.split("?date_req=")[1]
    if data["Valute"]:
        new_data_dict = {c["CharCode"]: c for c in data["Valute"]}
        for code in currency_codes:
            if code.upper() in new_data_dict:
                currencies[code.upper()] = float(new_data_dict[code.upper()]["Value"].replace(",", "."))
            else:
                currencies[code.upper()] = f"Код валюты '{code}' не найден."
    return currencies, date

# print(get_currencies(["USD", "VND"]))