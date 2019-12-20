class DiffieHellman:

    __private_key = None
    __mixed_key = None

    def __init__(self, a: int, p: int, g: int = 3):
        self.__a = a
        self.__p = p
        self.__g = g

    @property
    def mixed_key(self):
        """
        Возвращает смешанный ключ

        :return:
        """

        return self.__mix()

    def generate_key(self, mixed_key):
        """
        Возвраащет приватный ключ

        :param mixed_key:
        :return:
        """

        self.__private_key = mixed_key ** self.__a % self.__p
        return self.__private_key

    def __mix(self):
        """
        Миксует ключ с модулем

        :return:
        """

        self.__mixed_key = self.__g ** self.__a % self.__p
        return self.__mixed_key


if __name__ == '__main__':

    # 1. Обмен сервера и клиента g и p

    g = 3
    p = 32 + 32 ** 32  # Надо что-то длинное и случайное

    # 2. Микс ключей на каждой стороне и обмен ими

    S_key = 1233  # И тут
    Server = DiffieHellman(a=S_key, p=p, g=g)
    server_mixed_key = Server.mixed_key
    print(server_mixed_key)

    C_key = 4563  # И тут
    Client = DiffieHellman(a=C_key, p=p, g=g)
    client_mixed_key = Client.mixed_key
    print(client_mixed_key)

    # 3. Вычисление приватного ключа

    private_key_1 = Server.generate_key(client_mixed_key)
    private_key_2 = Client.generate_key(server_mixed_key)
    print(private_key_1)
    print(private_key_2)

    # 4. Взлом. При этом g, p, S_key и C_key перехвачены. private_key для проверки
    # Но узнать реальный ключ в жизни, только перебором :/ А там система заблокирует

    def encrypt(p, server_mixed_key, private_key):
        for key in range(1000):
            if server_mixed_key ** key % p == private_key:
                return server_mixed_key ** key % p
        return None

    print(
        "Нашел" if encrypt(p, server_mixed_key, private_key_1) else "Не нашел"
    )
