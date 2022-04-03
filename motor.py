import RPi.GPIO as GPIO
import time
import cv2
import imutils

GPIO.setmode(GPIO.BOARD)

ControlPin_motor1 = [7,11,13,15]
ControlPin_motor2 = [16,18,22,37]

for pin in ControlPin_motor1:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,0)
for pin in ControlPin_motor2:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,0)
    


rev_seq = [ [1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1],
            [1,0,0,1] ]

seq = [ [1,0,0,1],
        [0,0,0,1],
        [0,0,1,1],
        [0,0,1,0],
        [0,1,1,0],
        [0,1,0,0],
        [1,1,0,0],
        [1,0,0,0] ]

def move_one():
    for i in range(8):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(ControlPin_motor1[pin], seq[halfstep][pin])
                time.sleep(0.0009)

def rotate_one():
    for i in range(65):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(ControlPin_motor2[pin], seq[halfstep][pin])
                time.sleep(0.0009)
                
def back_to_start():
    for i in range(75):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(ControlPin_motor1[pin], rev_seq[halfstep][pin])
                time.sleep(0.0009)
    for i in range(25):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(ControlPin_motor1[pin], seq[halfstep][pin])
                time.sleep(0.0009)
    
    
def reset_to_back():
    for i in range(1400):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(ControlPin_motor1[pin], rev_seq[halfstep][pin])
                time.sleep(0.0009)

def set_to_start():
    for i in range(1082):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(ControlPin_motor1[pin], seq[halfstep][pin])
                time.sleep(0.0009)
                
def takePicture(count):
    cap = cv2.VideoCapture("/dev/video0")
    (grabbed, frame) = cap.read()
    time.sleep(0.3) # Wait 300 miliseconds
    image = '/home/pi/New/'+str(count)+'.png'
    cv2.imwrite(image, frame)
    return image

def take_all():
    count = 0
    for i in range(8):
        if(count != 0):  
            rotate_one()
            time.sleep(3)
            
        for i in range(6):
            takePicture(count)
            move_one()
            time.sleep(2)
            
            count += 1
        back_to_start()
        
    
#reset_to_back()
#set_to_start() #move camera to the starting place
take_all()
GPIO.cleanup()
        
        