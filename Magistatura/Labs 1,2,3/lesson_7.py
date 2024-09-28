import random


def generated_password( len_password ):
    sequence = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+{}[]|\\:";\'<>,.?/'
    answer = ''
    while len_password > len(answer):
        answer += random.choice(sequence)
    return answer


def main():
    len_password = input('Введите колличество символов в пароле\n')
    if len_password.isdigit():
        print(f'Ваш сгенерированый пароль : {generated_password(int(len_password))}')
    else:
        print('Введите число')

if __name__ == '__main__':
    main()