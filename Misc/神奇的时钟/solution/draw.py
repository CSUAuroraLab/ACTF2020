from turtle import *
 
def Skip(step):
	penup()
	forward(step)
	pendown()
 
def mkHand(name, length):
	reset()
	Skip(-length*0.1)
	begin_poly()
	penup()
	forward(length*1.1)
	pendown()
	end_poly()
	handForm = get_poly()
	register_shape(name, handForm)

def Init(i):
	global minHand, secHand
	hideturtle()
	mkHand("minHand" + str(i), 5)
	mkHand("secHand" + str(i), 10)
	minHand = Turtle()
	minHand.shape("minHand" + str(i))
	secHand = Turtle()
	secHand.shape("secHand" + str(i))
	for hand in [minHand, secHand]:
		hand.shapesize(1, 1, 1.2)
		hand.speed(10)

def Tick(xi, yi, sec):
	hideturtle()
	m, second = divmod(sec, 60)
	h, m = divmod(m, 60)
	minute = m + second/60.0
	minHand.penup()
	secHand.penup()
	minHand.goto(-1120 + xi * 20, 380 - yi * 20)
	secHand.goto(-1120 + xi * 20, 380 - yi * 20)
	minHand.down()
	secHand.down()
	secHand.setheading(6*second)
	minHand.setheading(6*minute)
 
def main(line):
	screensize(2280, 540, None)
	mode("logo")
	xi = 0
	yi = 0
	for i in range(len(data)):
		if i >= line and i % line == 0:
			xi = 0
			yi += 1
		tracer(False)
		Init(i)
		tracer(True)
		Tick(xi, yi, int(data[i]))
		xi += 1
	mainloop()

def readcsv():
	database = []
	with open("abort_hour.csv") as f:
		data = f.read().split('\n')
	for i in data:
		database += i.split(',')
	return database
 
if __name__ == '__main__':
	data = readcsv()
	main(112)
