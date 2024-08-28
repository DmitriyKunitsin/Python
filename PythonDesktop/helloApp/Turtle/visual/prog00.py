import turtle as Turtle

def zigzag(size, lenght):
    if size > 0:
        Turtle.left(45)
        Turtle.forward(lenght)
        Turtle.right(90)
        Turtle.forward(2 * lenght)
        Turtle.left(90)
        Turtle.forward(lenght)
        Turtle.right(45)
        zigzag(size - 1, lenght)

# if __name__ == '__name__':
zigzag(5,50)