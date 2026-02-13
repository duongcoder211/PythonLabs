import re

class UserCurrency:
    """
        Реализуетсвязь «много ко многим» между пользователями и валютами.
        :param id_: уникальный идентификатор
        :param user_id: внешний ключ к User
        :param currency_id: внешний ключ к Currency
    """

    def __init__(self, id_ :int, user_id :int, currency_id :str):
        self.id = id_
        self.user_id = user_id
        self.currency_id = currency_id

    @property
    def id(self):
        return self.__id
    @property
    def user_id(self):
        return self.__user_id
    @property
    def currency_id(self):
        return self.__currency_id
    @id.setter
    def id(self, id_: int):
        if isinstance(id_,int) and id_ >=0:
            self.__id = id_
        else:
            raise TypeError("id must be an integer greater than or equal to 0")
    @user_id.setter
    def user_id(self, user_id: int):
        if isinstance(user_id, int) and user_id >= 0:
            self.__user_id = user_id
        else:
            raise TypeError("user id must be an integer greater than or equal to 0")
    @currency_id.setter
    def currency_id(self, currency_id):
        if isinstance(currency_id, str) and currency_id != "" and re.match(r'[a-zA-Z]', currency_id[0]) is not None:
            self.__currency_id = currency_id
        else:
            raise TypeError("currency id must be a nonempty string start with a letter")
