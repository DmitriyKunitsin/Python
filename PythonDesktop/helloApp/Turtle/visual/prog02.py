import turtle as Turtle

def drawfib(n, len_ang):
    Turtle.forward(2 * len_ang)
    if n == 0 or n == 1:
        pass
    else:
        Turtle.left(len_ang)
        drawfib(n - 1, len_ang)
        Turtle.right(2 * len_ang)
        drawfib(n - 2, len_ang)
        Turtle.left(len_ang)

    Turtle.backward(2 * len_ang)

Turtle.left(90)
Turtle.speed(0)
drawfib(70,20)