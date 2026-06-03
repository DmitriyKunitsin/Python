from dataclasses import dataclass

@dataclass
class Person:
    nick: str
    surname: str
    color: str = "#3498db"  # цвет по умолчанию

    @property
    def full_name(self) -> str:
        return f"{self.nick} ({self.surname})"