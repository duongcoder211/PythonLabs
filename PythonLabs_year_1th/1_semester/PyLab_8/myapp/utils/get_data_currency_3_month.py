import re
from utils.currencies_api import get_currencies
def get_data_currency_3_month(valute: str = "USD", date: str = "9/Oct/2025"):
    months = {
        "Jan": ["01", 31],
        "Feb": ["02", 28],  # 29 in leap year
        "Mar": ["03", 31],
        "Apr": ["04", 30],
        "May": ["05", 31],
        "Jun": ["06", 30],
        "Jul": ["07", 31],
        "Aug": ["08", 31],
        "Sep": ["09", 30],
        "Oct": ["10", 31],
        "Nov": ["11", 30],
        "Dec": ["12", 31],
        "1": ["01", 31],
        "2": ["02", 28],  # 29 in leap year
        "3": ["03", 31],
        "4": ["04", 30],
        "5": ["05", 31],
        "6": ["06", 30],
        "7": ["07", 31],
        "8": ["08", 31],
        "9": ["09", 30],
        "10": ["10", 31],
        "11": ["11", 30],
        "12": ["12", 31],
    }
    date = date.replace(" ", '/')
    current_day = date.split("/")[0]
    year = re.findall("[0-9]{4}", date)[-1]
    monthdate = months[date.split("/")[1]]  # ["12", 31]
    num_month = int(monthdate[0])  # "12"
    # print(date)
    # print(year)
    # print(monthdate)
    # print(num_month)
    date = date.replace(date.split("/")[1], months[date.split("/")[1]][0])
    day_list = []
    val_list = []

    try:
        for m in range(num_month - 2, num_month + 1):
            for d in range(1, months[str(m)][1] + 1):
                if f'{'0' + str(d) if len(str(d)) == 1 else d}/{'0' + str(m) if len(str(m)) == 1 else m}/{year}' == date:
                    break
                url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={'0' + str(d) if len(str(d)) == 1 else d}.{'0' + str(m) if len(str(m)) == 1 else m}.{year if num_month - 2 > 0 else year - 1}"
                # print(url)
                res, url_date = get_currencies([valute], url=url)
                if res[valute] == f"Код валюты '{valute}' не найден.":
                    msg = f"Код валюты '{valute}' не найден."
                    return [], [], msg, "red"
                day_list.append(f"{d}/{m}/{year if num_month - 2 > 0 else year - 1}")
                val_list.append(res[valute])
                # print(day_list)
                # print(val_list)
    except Exception as e:
        raise f'Error: {e}'

    return day_list, val_list, "Request was successfully executed", "green"