def divide(a,b):
    try:
            raise Exception("Целенаправленно вызванная ошибка!")
    except Exception as err:
                print("Error: {0}".format(err))
        
    try:
            result = a / b
            print("Result : ",result)
    except ZeroDivisionError as err:
            ''' Деление на ноль '''
            print("Error: {0}".format(err))
    except TypeError as err:
            print("Error: {0}".format(err))
    except Exception as err:
            print("Error: {0}".format(err))
    else:##Если в блоке try ошибок не было, то выполняется блок елсе
            print("This line will be executed...")
    finally:
            print("Executing finally clause")
def main():
    divide(2,1)
    print('\n')
    divide('2', '1')
    print('\n')
    divide(1,0)

if __name__ == '__main__':
    main()