"""
Модуль с константами пользователя состояний для ConversationHandler.
"""
ASK_AGE = 0
'Возраст'
ASK_WEIGHT = 1
'Вес'
ASK_HEIGHT = 2
'Рост'
ASK_GENDER = 3
'Пол'
ASK_EMAIL = 4
'почта'

ASK_CONST_STRING_END = "Конец"

state_texts = {
    ASK_AGE: "Возраст",
    ASK_WEIGHT: "Вес",
    ASK_HEIGHT: "Рост",
    ASK_GENDER: "Пол",
    ASK_EMAIL: "Почта",
    -1: ASK_CONST_STRING_END,
}

def get_state_text(state):
    return state_texts.get(state, "Неизвестное состояние")