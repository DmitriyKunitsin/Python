import turtle as Turtle
import random

Turtle.speed(0)
Turtle.bgcolor('Black')
colors=['Red', 'Yellow', 'Pink', 'Orange',
'Blue', 'Green', 'Cyan', 'White']
for x in range(300):
    Turtle.color(colors[random.randint(0,7)])
    Turtle.forward(x)
    Turtle.left(90)