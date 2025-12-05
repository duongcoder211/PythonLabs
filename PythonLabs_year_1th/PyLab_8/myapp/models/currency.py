import re
from numbers import Number

class Currency:
    """
    parameters:
        :param id_: уникальный идентификатор
        :param num_code: цифровой код
        :param char_code: символьный код
        :param name: название валюты
        :param value: курс
        :param nominal: номинал (за сколько единиц валюты указан курс)
    """
    def __init__(self, id_: str|None, num_code: str|None, char_code: str|None, name: str|None, value: Number|None, nominal: int|None):
        self.id = id_
        self.num_code = num_code
        self.char_code = char_code
        self.name = name
        self.value = value
        self.nominal = nominal

    @property
    def id(self) -> str:
        return self.__id
    @property
    def num_code(self) -> str:
        return self.__num_code
    @property
    def char_code(self) -> str:
        return self.__char_code
    @property
    def name(self) -> str:
        return self.__name
    @property
    def value(self) -> Number:
        return self.__value
    @property
    def nominal(self) -> int:
        return self.__nominal
    @id.setter
    def id(self, id_: str):
        if isinstance(id_, str) and id_ != "" and re.match(r'[a-zA-Z]', id_[0]) is not None:
            self.__id = id_
        else:
            raise TypeError("id must be a nonempty string start with a letter")

    @num_code.setter
    def num_code(self, num_code: str):
        if isinstance(num_code, str) and len(num_code) >= 0:
            self.__num_code = num_code
        else:
            raise TypeError("num_code must be an string")

    @char_code.setter
    def char_code(self, char_code: str):
        parser = r"[a-zA-Z]+"
        if isinstance(char_code, str) and re.fullmatch(parser, char_code) is not None:
            self.__char_code = char_code.upper()
        else:
            raise TypeError("char_code must be a string of letters")

    @name.setter
    def name(self, name: str):
        if isinstance(name, str) and (len(name) > 0) and (len(name) <= 50):
            self.__name = name.title()
        else:
            raise TypeError("name must be a string length not of None and at most 50 characters long")

    @value.setter
    def value(self, value: Number):
        if isinstance(value, Number) and value > 0:
            self.__value = value
        else:
            raise TypeError("value must be a number greater than zero")

    @nominal.setter
    def nominal(self, nominal: int):
        if isinstance(nominal, int) and nominal >= 0:
            self.__nominal = nominal
        else:
            raise TypeError("nominal must be an integer greater than or equal to zero")
