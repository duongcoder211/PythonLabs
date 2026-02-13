from .author import Author
class App:
    """
    parameters:
        :param name: название приложения;
        :param version: версия приложения;
        :param author: объект Author;
    """
    def __init__(self, name :str, version :str, author :Author):
        self.name = name
        self.version = version
        self.author : Author = author #вызов setter -> присвоение в self.__author -> и validate и private

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name :str):
        if type(name) is str and len(name) >= 5:
            self.__name = name
        if type(name) is not str:
            raise TypeError('name must be of type str')
        if len(name) < 5:
            raise TypeError('name length must be greater than 5')

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, version :str):
        if type(version) is str and len(version) >= 5:
            self.__version = version
        elif type(version) is not str:
            raise TypeError('version must be of type str')
        else:
            raise ValueError('version length must be greater than 5')

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, author :Author):
        if isinstance(author, Author):
            self.__author = author
        else:
            raise TypeError('author must be of type Author')