class Author:
    """
    parameter:
        :param name: имя автора;
        :param group: учебная группа;
    """
    def __init__(self, name :str, group :str):
        self.name = name
        self.group = group

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name :str):
        if type(name) is str and len(name) >= 2:
            self.__name = name.title()
        else:
            raise ValueError("Name must be of type str at least 2 characters")

    @property
    def group(self):
        return self.__group

    @group.setter
    def group(self, group :str):
        if type(group) is str and len(group) >= 5:
            self.__group = group
        elif len(group) < 5:
            raise ValueError("Group must be at least 5 characters")
        else:
            raise ValueError("Group must be of type str")

    def __str__(self):
        return f"This app created by {self.__name} in group {self.__group}"