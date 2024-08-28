## Рекурсия
def fibo(n):
    if n <= 1:
        return n
    else:
        return (fibo(n - 1) + fibo(n - 2))

def factorial(n):
    if n == 1:
        return n
    else:
        return n * factorial(n - 1)

def print_msg(msg, count):
    if count != 0:
        print(f"count = {count}",msg)
        print_msg(msg, count - 1)

## Косвенная рекурсия
## В простейшей форме косвенной рекурсии подррограмма А вызывает подпрограмму В
#  а подпрограмма В вызывает подпрограмму А
def ping(i):
    if i > 0:
        print("Ping : " + str(i))
        return pong(i - 1)
    return 0

def pong(i):
    if i > 0:
        print("Pong : " + str(i))
        return ping(i-1)
    return 1
def main():
    print_msg('Test String...', 10)
    print(factorial(5))
    print(fibo(15))
    ping(30)

if __name__ == "__main__":
    main()