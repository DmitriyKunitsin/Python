class UserProfile:
    def __init__(self, user_data = None, new_user = None):
        if user_data:
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
        elif new_user:
            self.id = new_user.id
            self.username = new_user.username
            self.first_name = new_user.first_name
            self.last_name = new_user.last_name
            self.full_name = new_user.full_name
            self.premium = 1
            self.height = None
            self.weight = None
            self.iwm = 0
            self.gender = None
            self.age = None
            self.email = None
            self.register_date = None
        else:
            self.id = 0
            self.username = 0
            self.first_name = 0
            self.last_name = 0
            self.full_name = 0
            self.premium = 0
            self.height = 0
            self.weight = 0
            self.iwm = 0
            self.gender = 0
            self.age = 0
            self.email = 0
            self.register_date = 0
        
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
    
    @staticmethod
    def init_user(new_user):
        user = UserProfile(new_user=new_user)
        return user
    
    @staticmethod
    def load_foarm(user_id):
        from db.sqliteDb import get_user_data
        user = get_user_data(user_id=user_id)
        if user is None:
            return None
        return UserProfile(user)
        
