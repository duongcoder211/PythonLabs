import re
class User:
    """
        :param id_: уникальный идентификатор
        :param name: имя пользователя
    """
    def __init__(self, id_: int, name: str):
        self.id = id_
        self.name = name

    @property
    def id(self) -> int:
        return self.__id_
    @property
    def name(self) -> str:
        return self.__name

    @id.setter
    def id(self, id_: int):
        if type(id_) is int and id_ >= 0:
            self.__id_ = id_
        else:
            raise TypeError("id must be an integer greater than or equal to zero")

    @name.setter
    def name(self, name: str):
        parser = r'[a-zA-Z]'
        if (type(name) is str) and (len(name) > 0) and (len(name) <= 30) and re.match(parser, name[0]) is not None:
            self.__name = name.title()
        else:
            raise TypeError("name must be an string not None smaller than 30 and start with a letter")

# User(id_=1234, name="User number 1")