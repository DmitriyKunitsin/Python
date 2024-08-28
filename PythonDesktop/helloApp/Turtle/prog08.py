import turtle as Turtle
Turtle.speed(0)
Turtle.bgcolor('Black')
colors = ['Red', 'Yellow', 'Pink', 'Orange']
for x in range(300):
    Turtle.color(colors[x%4])
    Turtle.forward(x)
    Turtle.left(90)