import turtle as Turtle

Turtle.bgcolor('Black')
colors=["Red","White","Cyan","Yellow","Green","Orange"]
for x in range(300):
    Turtle.color(colors[x%6])
    Turtle.fd(x)
    Turtle.left(59)