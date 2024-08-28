class Error(Exception):
    pass

class ValueTooSmallError(Error):
    pass

class ValueTooLArgeError(Error):
    pass

def main():
    num = 10
    try:
        i_num = int(input("Enter a num : "))
        if i_num < num:
            raise ValueTooSmallError
        elif i_num > num:
            raise ValueTooLArgeError
        else:
            print('Perfect!')
    except ValueTooSmallError:
        print('Число слишком мало!')
    except ValueTooLArgeError:
        print("Число слишком велико!")

if __name__ == '__main__':
    main()