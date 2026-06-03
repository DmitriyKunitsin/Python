from PersonFile import Person
from CalendarReportFile import CalendarReport

if __name__ == "__main__":
    # Список из 7 человек (ник, фамилия)
    team = [
        Person("А", "Афонин", color="#e74c3c"),   # красный
        Person("Г", "Голенков", color="#3498db"),   # синий
        Person("Т", "Тейтельбаум", color="#2ecc71"),   # зеленый
        Person("Н", "Насибулин", color="#f1c40f"),# желтый
        Person("С", "Сергеев", color="#9b59b6"),  # фиолетовый
        Person("М", "Мышко", color="#1abc9c"),# бирюзовый
        Person("К", "Куницин", color="#e67e22")   # оранжевый
    ]

    # Генерируем календарь на июнь 2026
    report = CalendarReport(team, 2026, 6, start_index=0)
    report.generate_html("duty_june2026_colored.html")