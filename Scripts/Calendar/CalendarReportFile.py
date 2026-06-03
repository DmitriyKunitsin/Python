import calendar
from datetime import datetime
from typing import List, Dict, Optional
from PersonFile import Person
from ProductCalendarFile import ProductionCalendar

class CalendarReport:
    def __init__(self, people: List[Person], year: int, month: int,
                 start_index: int = 0, prod_calendar: ProductionCalendar = ProductionCalendar()):
        if not 1 <= month <= 12:
            raise ValueError("Месяц должен быть от 1 до 12")
        if not people:
            raise ValueError("Список людей не должен быть пустым")
        self._people = people
        self.year = year
        self.month = month
        self._start_index = start_index % len(people)
        self._prod_calendar = prod_calendar

    @property
    def people(self) -> List[Person]:
        return self._people.copy()

    def _build_schedule(self) -> Dict[int, Person]:
        """Расписание дежурств: только рабочие дни по производственному календарю."""
        cal = calendar.monthcalendar(self.year, self.month)
        schedule = {}
        idx = self._start_index
        for week in cal:
            for day_of_week, day in enumerate(week):
                if day == 0:
                    continue
                # Проверяем, рабочий ли день (используем производственный календарь)
                if self._prod_calendar.is_working_day(self.year, self.month, day):
                    schedule[day] = self._people[idx]
                    idx = (idx + 1) % len(self._people)
        return schedule

    def generate_html(self, output_path: str = "calendar_report.html") -> None:
        cal = calendar.monthcalendar(self.year, self.month)
        month_name = calendar.month_name[self.month]
        schedule = self._build_schedule()

        today = datetime.now().day if (
            self.year == datetime.now().year and self.month == datetime.now().month
        ) else None

        html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Календарь дежурств на {month_name} {self.year}</title>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        .calendar {{ border-collapse: collapse; width: 100%; }}
        .calendar th {{ background: #4CAF50; color: white; padding: 10px; }}
        .calendar td {{ border: 1px solid #ddd; vertical-align: top; padding: 8px; height: 100px; }}
        .date {{ font-weight: bold; }}
        .duty-person {{ margin: 5px 0 0 0; font-size: 14px; }}
        .today {{ background-color: #e6ffe6; }}
        .weekend {{ background-color: #f5f5f5; }}
    </style>
</head>
<body>
    <h1>Календарь дежурств на {month_name} {self.year}</h1>
    <table class="calendar">
        <tr>
            <th>Пн</th><th>Вт</th><th>Ср</th><th>Чт</th><th>Пт</th><th>Сб</th><th>Вс</th>
        </tr>
"""
        for week in cal:
            html += "<tr>"
            for day_of_week, day in enumerate(week):
                if day == 0:
                    html += "<td></td>"
                else:
                    is_today = (day == today)
                    is_working = self._prod_calendar.is_working_day(self.year, self.month, day)
                    class_today = "today" if is_today else ""
                    class_weekend = "weekend" if not is_working else ""
                    html += f"<td class='{class_today} {class_weekend}'"

                    if day in schedule:
                        person = schedule[day]
                        # Добавляем inline-стиль с цветом фона для ячейки
                        html += f" style='background-color: {person.color}40;'"  # полупрозрачный цвет
                    html += ">"

                    html += f"<div class='date'>{day}</div>"
                    if day in schedule:
                        person = schedule[day]
                        html += f"<div class='duty-person'>{person.full_name}</div>"
                    html += "</td>"
            html += "</tr>"

        html += """
    </table>
</body>
</html>"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Отчёт сохранён в {output_path}")