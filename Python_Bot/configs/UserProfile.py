class UserProfile:
    def __init__(self, user_data):
        self.id = user_data[0]
        self.username = user_data[1]
        self.first_name = user_data[2]
        self.last_name = user_data[3]
        self.full_name = user_data[4]
        self.premium = user_data[7]
        self.height = user_data[8]
        self.weight = user_data[9]
        self.iwm = user_data[10]
        self.gender = user_data[11]
        self.age = user_data[12]
        self.email = user_data[13]
        self.register_date = user_data[14]
        
    def get_is_premium(self):
        if self.premium == 1:
            return "Yes"
        else:
            return "No"
        
    def get_stadia_iwm(self) -> str:
        if self.iwm < 16:
            return "Выраженный дефицит массы тела"
        elif 16 <= self.iwm < 18.5:
            return "Недостаточная масса тела"
        elif 18.5 <= self.iwm < 25:
            return "Норма"
        elif 25 <= self.iwm < 30:
            return "Избыточная масса тела (предожирение)"
        elif 30 <= self.iwm < 35:
            return "Ожирение 1 степени"
        elif 35 <= self.iwm < 40:
            return "Ожирение 2 степени"
        elif self.iwm >= 40:
            return "Ожирение 3 степени (морбидное)"
        else:
            return ""
    def calc_iwm(self) -> str | float:
        try:
            height = (self.height / 100)
            self.iwm = self.weight / (height * height)
            return float('{:.1f}'.format(self.iwm))
        except (ValueError, TypeError) as ex:
            print(f'Ошибка при рассчете ИМТ ({ex})')
            return "Неудалось рассчитать"
        
