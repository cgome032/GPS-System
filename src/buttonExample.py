import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN,pull_up_down=GPIO.PUD_OFF) 
GPIO.input(18)

 
while(1):
    if(GPIO.input(18)):
        print("High")
    else:
        print("Low")
