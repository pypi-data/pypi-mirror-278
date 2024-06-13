class User:
    """
    Базовий клас для регістрації і входу до системи
    Абстрактний базовий клас

    :param login: Логін користувача
    :type login: str
    :param password: Пароль користувача
    :type password: str
    """
    def __init__(self,
                 login,
                 password):
        self.login = login
        self.password = password

    def check_data(self,login,password):
        """
        Дія перевірки логіну і паролю на співпадіння

        :param login: Логін доля перевірки
        :type login: str
        :param password: Пароль для перевірки
        :type password: str

        :return: True якщо співпало False якщо ні
        :rtype: bool
        """
        if (self.login == login and
            self.password == password):
            return True
        else:
            return False

class Admin(User):
    pass

class Support(User):
    pass

class Author(User):
    pass


def login(user_type:str):
    """
    Дія входу користувачем

    :param user_type: Тип користувача
    :type user_type: str
    """



def registration(user_type:str):
    """
    Дія регістрації користувачем

    :param user_type: Тип користувача
    :type user_type: str
    """




