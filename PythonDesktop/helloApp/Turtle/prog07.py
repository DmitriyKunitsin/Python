import turtle as Turtle
Turtle.speed(0)
Turtle.bgcolor('Black')
colors = ['Red', 'Yellow', 'Purple', 'Cyan', 'Orange', 'Pink']
for x in range(100):
    Turtle.circle(x)
    Turtle.color(colors[x%6])
    Turtle.left(60)