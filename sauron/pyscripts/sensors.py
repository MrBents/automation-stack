import RPi.GPIO as GPIO
from datetime import datetime

ObstaclePin1 = 3
ObstaclePin2 = 5

velocity = 0
sensor_dist = 6
camera_dist = 53
now1 = True
now2 = True
downtime1 = datetime.now()
downtime2 = 0
sleep = 250000
timer1 = queue.Queue()
timer2 = queue.Queue()




def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(ObstaclePin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  	GPIO.setup(ObstaclePin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)





def loop():
	while True:
    if (datetime.now() > downtime1):
      now1 = True

	if (0 == GPIO.input(ObstaclePin1)) and now1:
		print "Obstacle First!"
		now1 = False
      	downtime1 = datetime.now() + datetime(0, 0, 0, 0, 0, 0, 0, sleep)
		timer1.push(datetime.now())

    if (datetime.now() > downtime2):
      now1 = True

	if (0 == GPIO.input(ObstaclePin2)) and now1:
		print "Obstacle Second!"
		now2 = False
		timer2.push(datetime.now())




def destroy():
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
