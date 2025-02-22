from dataclasses import dataclass
from random import choice, randint
from src.constants.user_data import Sex, MenNames, WomenNames, Role, Email
from string import ascii_letters, digits


@dataclass
class UserData:
    """Класс описывающий мужского пользователя."""

    def __init__(self) -> None:
        self.id = randint(1, 99)
        self.sex = Sex.get_random_item()
        self.__sex_names = MenNames if self.sex == Sex.MALE else WomenNames
        self.first_name = self.get_random_first_name()
        self.last_name = self.get_random_last_name()
        self.middle_name = self.get_random_middle_name()
        self.full_name = f"{self.last_name} {self.first_name} {self.middle_name}"
        self.role = Role.get_random_item()
        self.email = f"{generate_string()}@{Email.get_random_item().value}"
        self.age = randint(18, 100)
        self.password = generate_string(8)

    def get_random_first_name(self) -> str:
        """Получаем случайное имя."""
        return choice(self.__sex_names.first_names)

    def get_random_last_name(self) -> str:
        """Получаем случайную фамилию."""
        return choice(self.__sex_names.last_names)

    def get_random_middle_name(self) -> str:
        """Получаем случайное отчество."""
        return choice(self.__sex_names.middle_names)


def generate_string(count_chars: int = 6) -> str:
    """Генерирует случайную строку."""
    return ''.join(choice(ascii_letters + digits) for _ in range(randint(count_chars, 30)))