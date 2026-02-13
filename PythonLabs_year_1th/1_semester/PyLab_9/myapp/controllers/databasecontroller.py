from abc import ABC, abstractmethod #abc = adstract base class
import sqlite3

class BaseCRUD(ABC):
    def __init__(self):
        self._con = sqlite3.connect(':memory:')
        self._cursor = self._con.cursor()
        self._createtable()
    
    @abstractmethod
    def _createtable(self):
        pass
    
    @abstractmethod
    def _create(self, *args, **kargs):
        pass

    @abstractmethod
    def _read(self, *args, **kargs):
        pass

    @abstractmethod
    def _update(self, *args, **kargs):
        pass

    @abstractmethod
    def _delete(self, *args, **kargs):
        pass

    def _close(self):
        if self._con:
            self._cursor = None
            self._con.close()

    def __del__(self):
        self._close()

# class CurrencyRatesCRUD:
#     def __init__(self, currency_rates_obj):
#         self.__con = sqlite3.connect(':memory:')
#         self.__cursor = self.__con.cursor()
#         self.__createtable()
#         self.__currency_rates_obj = currency_rates_obj

#     def __createtable(self):
#         self.__con.execute(
#             "CREATE TABLE IF NOT EXISTS currency("
#             "id INTEGER PRIMARY KEY AUTOINCREMENT, "
#             "cur TEXT,"
#             "date TEXT DEFAULT CURRENT_TIMESTAMP,"
#             "value FLOAT);")
#         self.__con.commit()

#     def _create(self):
#         __params = self.__currency_rates_obj.values
#         # [("USD", "02-04-2025 11:10", "90"), ("EUR", "02-04-2025 11:11", "91")]
#         __sqlquery = "INSERT INTO currency(cur,  value) VALUES(?, ?)"

#         # TODO: реализовать именованный стиль запроса
#         # This is the named style used with executemany():
#         # data = (
#         #     {"name": "C", "year": 1972},
#         #     {"name": "Fortran", "year": 1957},
#         #     {"name": "Python", "year": 1991},
#         #     {"name": "Go", "year": 2009},
#         # )
#         # cur.executemany("INSERT INTO lang VALUES(:name, :year)", data)

#         self.__cursor.executemany(__sqlquery, __params)
#         self.__con.commit()

#     def _read(self):
#         # TODO: Реализовать параметризованный запрос на получение значения валют по коду: строка из трех символов
#         cur = self.__con.execute("SELECT * FROM currency")
#         # result_data = list(zip(['id', 'cur', 'date', 'value'], cur))
#         result_data = []
#         for _row in cur:
#             _d = {'id': int(_row[0]), 'cur': _row[1], 'date': _row[2], 'value': float(_row[3])}
#             result_data.append(_d)

#         return result_data

#     def _update(self, currency: dict['str': float]):
#         # ...._update({'USD': 101.1})
#         currency_code = tuple(currency.keys())[0]
#         currency_value = tuple(currency.values())[0]
#         upd_statement = f"UPDATE currency SET value = {currency_value} WHERE cur = '" + str(currency_code) + "'"
#         print(upd_statement)
#         self.__cursor.execute(upd_statement)
#         self.__con.commit()

#     def _delete(self, currency_id):
#         del_statement = "DELETE FROM currency WHERE id = " + str(currency_id)
#         print(del_statement)
#         self.__cursor.execute(del_statement)
#         self.__con.commit()
#         pass

#     def __del__(self):
#         self.__cursor = None
#         self.__con.close()

class CurrencyRatesCRUD(BaseCRUD):
    def __init__(self, currency_rates_obj):
        self.__currency_rates_obj = currency_rates_obj
        super().__init__()

    def _createtable(self):
        # self._con.execute(
        #     "CREATE TABLE IF NOT EXISTS currency("
        #     "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        #     "cur TEXT,"
        #     "date TEXT DEFAULT CURRENT_TIMESTAMP,"
        #     "value FLOAT);")
        # self._con.commit()
        
        self._con.execute(
            "CREATE TABLE IF NOT EXISTS currency("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "valute_id TEXT, "
            "numcode INTEGER, "
            "charcode TEXT CHECK(length(charcode) = 3), "
            "nominal INTEGER, "
            "name TEXT, "
            "value FLOAT, "
            "vunitrate FLOAT, "
            "date TEXT DEFAULT CURRENT_TIMESTAMP);")
        self._con.commit()

    def _create(self):
        # __params = self.__currency_rates_obj.values
        __params = list(map(lambda i: {"ID": i["@ID"], 'NumCode': i['NumCode'], 'CharCode': i['CharCode'], 'Nominal': i['Nominal'], 'Name': i['Name'], 'Value': i['Value'].replace(",","."), 'VunitRate': i['VunitRate'].replace(",",".")}, self.__currency_rates_obj.values))
        # [("USD", "02-04-2025 11:10", "90"), ("EUR", "02-04-2025 11:11", "91")]
        # __sqlquery = "INSERT INTO currency(cur,  value) VALUES(?, ?)"
        __sqlquery = "INSERT INTO currency(valute_id, numcode, charcode, nominal, name, value, vunitrate, date) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"

        # TODO: реализовать именованный стиль запроса
        # This is the named style used with executemany():
        # data = (
        #     {"name": "C", "year": 1972},
        #     {"name": "Fortran", "year": 1957},
        #     {"name": "Python", "year": 1991},
        #     {"name": "Go", "year": 2009},
        # )
        # cur.executemany("INSERT INTO lang VALUES(:name, :year)", data)

        self._cursor.executemany(
            """INSERT INTO currency (valute_id, numcode, charcode, nominal, name, value, vunitrate)
                            VALUES(:ID, :NumCode, :CharCode, :Nominal, :Name, :Value, :VunitRate)""", tuple(__params))
        # self._cursor.executemany(__sqlquery, __params) #execute needs list of tuples or tuple
        self._con.commit()

    def _read(self):
        # TODO: Реализовать параметризованный запрос на получение значения валют по коду: строка из трех символов
        cur = self._con.execute("SELECT * FROM currency")
        # result_data = list(zip(['id', 'cur', 'date', 'value'], cur))
        result_data = []
        for _row in cur:
            # _d = {'id': int(_row[0]), 'cur': _row[1], 'date': _row[2], 'value': float(_row[3])}
            _d = {'id': int(_row[0]), 'valute_id': str(_row[1]), 'numcode': int(_row[2]), 'charcode': str(_row[3]), 'nominal': int(_row[4]), 'name': str(_row[5]), 'value': round(float(_row[6]), 2), 'vunitrate': round(float(_row[7]), 2), 'date': str(_row[8])}
            result_data.append(_d)

        return result_data

    def _update(self, currency: dict['str': float]):
        # ...._update({'USD': 101.1})
        currency_code = tuple(currency.keys())[0]
        currency_value = tuple(currency.values())[0]
        upd_statement = f"UPDATE currency SET value = {currency_value} WHERE charcode = '" + str(currency_code) + "'"
        print(upd_statement)
        self._cursor.execute(upd_statement)
        self._con.commit()

    def _delete(self, currency_id):
        del_statement = "DELETE FROM currency WHERE id = " + str(currency_id)
        print(del_statement)
        self._cursor.execute(del_statement)
        self._con.commit()

class UserCRUD(BaseCRUD):
    def __init__(self, user_obj):
        self.__user_obj = user_obj
        super().__init__()
    
    def _createtable(self):
        self._con.execute(
            "CREATE TABLE IF NOT EXISTS user("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "name TEXT NOT NULL CHECK(length(name) > 1));")
        self._con.commit()

    def _create(self, *args, **kargs):
        __params = [(val,) for val in self.__user_obj.values] # => tuple because executemany() needs list of tuples
        # ["Name_1", "Name_2"]
        __sqlquery = "INSERT INTO user(name) VALUES(?)"

        self._cursor.executemany(__sqlquery, __params)
        self._con.commit()

    def _read(self, query_dict = None, *args, **kargs):
        users = self._con.execute("SELECT * FROM user")
        result_data = []
        if query_dict:
            user_id = query_dict['id'][0]
            sql = "SELECT * FROM user WHERE id = ?"
            self._cursor.execute(sql, (user_id,))
            user = self._cursor.fetchall()  # [(5, 'Tang Vu Hoang Nguyen')]
            # user = self._con.execute(f"SELECT id = {} FROM user") #Incorrect
            if user:
                return {'id': int(user[0][0]), 'name': user[0][1]}
            else:
                return {'id': query_dict['id'][0], 'name': f"User with id = {query_dict['id'][0]} not found!"}
        else:
            for _row in users:
                _d = {'id': int(_row[0]), 'name': _row[1]}
                result_data.append(_d)
        return result_data
    
    def _update(self, *args, **kargs):
        pass
    def _delete(self, *args, **kargs):
        pass
