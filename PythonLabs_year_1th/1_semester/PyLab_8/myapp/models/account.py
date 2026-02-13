class Account:
    def __init__(self, islogin ,username, password):
        self.is_login = islogin
        self.username = username
        self.password = password

    @property
    def username(self):
        return self.__username
    @username.setter
    def username(self, username):
        if isinstance(username, str) and (len(username) > 0) and (len(username) < 32):
            self.__username = username
        else:
            raise TypeError('username must be between 32 characters long')

    @property
    def password(self):
        return f"Encoded password {self.__password}"

    @password.setter
    def password(self, password):
        if isinstance(password, str) and (len(password) > 0) and (len(password) < 32):
            self.__password = password
        else:
            raise TypeError('password must be between 32 characters long')

    @property
    def is_login(self):
        return self.__is_login

    @is_login.setter
    def is_login(self, islogin):
        if isinstance(islogin, bool):
            self.__is_login = islogin
        else:
            raise TypeError('login status must be bool')