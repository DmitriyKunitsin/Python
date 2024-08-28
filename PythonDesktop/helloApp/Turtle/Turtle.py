import turtle as Turtle
import time
import random

def square(lenght):
    for i in range(4):
        Turtle.forward(lenght)
        Turtle.left(90)


def main():
    Turtle.speed(10)
    Turtle.bgcolor('Black')
    turns = 1000
    distance = 20
    for x in range(turns):
        right = Turtle.right(random.randint(0,360))
        left = Turtle.left(random.randint(0,360))
        Turtle.color(random.choice(['Blue', 'Red', 'Green', 'Cyan', 'Magenta', 'Pink', 'Violet']))
        random.choice([right,left])
        Turtle.fd(distance)
    # Turtle.color("green")
    # for angle in range(0,360,10):
    #     Turtle.seth(angle)
    #     Turtle.circle(100)
    # square(150)
    # time.sleep(4)
    # Turtle.bye()
    


if __name__ == '__main__':
    main()