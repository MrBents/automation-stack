import RPi.GPIO as GPIO
from datetime import datetime, timedelta
import Queue

ObstaclePin1 = 3
ObstaclePin2 = 5

velocity = 0
sensor_dist = 6
camera_dist = 53
now1 = True
now2 = True
downtime1 = datetime.now()
downtime2 = datetime.now()
sleep = timedelta(microseconds=250000)
queue1 = Queue.Queue()
timer1 = Queue.Queue()
timer2 = Queue.Queue()

def convert_time(time1):
    sec_to_micr = time1.seconds * 1000000
    final_micro = sec_to_micr + time1.microseconds
    return final_micro

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(ObstaclePin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ObstaclePin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def loop():
    global downtime1
    global downtime2
    
    while True:
        if (datetime.now() > downtime1):
            now1 = True

        if (1 == GPIO.input(ObstaclePin1)) and now1:
                print "Obstacle First!"
                now1 = False
                timer1.put(datetime.now())
                downtime1 = datetime.now() + sleep


        if (datetime.now() > downtime2):
            now2 = True

        if (1 == GPIO.input(ObstaclePin2)) and now2:
            print "Obstacle Second!"
            now2 = False
            timer2.put(datetime.now())
            downtime2 = datetime.now() + sleep
##            velocity = (sensor_dist/(convert_time(timer2.get()-timer1.get())))
##            time_to = datetime.now() + timedelta(microseconds=(camera_dist/velocity))
            #queue1.put(time_to)

        if (queue1.qsize() > 0):
            if(queue1.queue[0] < datetime.now()):
                queue1.get()
                print('1')



def destroy():
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
