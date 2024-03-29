# author Ingmar Stapel
# version 0.1 BETA
# date 20140810 04:36 AM

import webiopi
from time import sleep

# Enable debug output
# webiopi.setDebug()
GPIO = webiopi.GPIO

# initiales setzen der Beschleunigung
acceleration = 0
turnacceleration = 0
# auf der Stelle drehen = false
spotturn = "false"
	
# Here we configure the PWM settings for
# the two DC motors. It defines the two GPIO
# pins used for the input on the L298 H-Bridge,
# starts the PWM and sets the
# motors' speed initial to 0
MAXSPEED = 100
MAXSTEERSPEED = 50
motorDriveForwardPin = 4 #7
motorDriveReversePin = 17 #11
motorSteerLeftPin = 27 #13
motorSteerRightPin = 22 #15
ledLeftPin = 23 #16
ledRightPin = 24 #18
motorDrivePWM = 5 #29
motorSteerPWM = 6 #31

#setup function is called automatically at WebIoPi startup
def setup():
	GPIO.setFunction(motorDriveForwardPin, GPIO.OUT)
	GPIO.setFunction(motorDriveReversePin, GPIO.OUT)
	GPIO.setFunction(motorSteerLeftPin, GPIO.OUT)
	GPIO.setFunction(motorSteerRightPin, GPIO.OUT)
	GPIO.setFunction(ledLeftPin, GPIO.OUT)
	GPIO.setFunction(ledRightPin, GPIO.OUT)
	GPIO.setFunction(motorDrivePWM, GPIO.PWM)
	GPIO.setFunction(motorSteerPWM, GPIO.PWM)


def initiate():
	global acceleration
	global turnacceleration
	global motorDriveSpeed
	global motorSteerSpeed
	global speedstep
	global maxspeed
	global maxsteerspeed	
	global minspeed
	
	spotturn = "false"
	acceleration = 0
	turnacceleration = 0
	motorDriveSpeed = 0
	motorSteerSpeed = 0
	speedstep = 10
	maxspeed = 100
	maxsteerspeed = 50
	minspeed = 0

def reverse():
    GPIO.digitalWrite(motorDriveForwardPin, GPIO.LOW)
    GPIO.digitalWrite(motorDriveReversePin, GPIO.HIGH)
	
def  forward():
    GPIO.digitalWrite(motorDriveForwardPin, GPIO.HIGH)
    GPIO.digitalWrite(motorDriveReversePin, GPIO.LOW)

def  left():
    GPIO.digitalWrite(motorSteerLeftPin, GPIO.HIGH)
    GPIO.digitalWrite(motorSteerRightPin, GPIO.LOW)
    GPIO.digitalWrite(ledLeftPin, GPIO.HIGH)
    GPIO.digitalWrite(ledRightPin, GPIO.LOW)    

def  right():
    GPIO.digitalWrite(motorSteerLeftPin, GPIO.LOW)
    GPIO.digitalWrite(motorSteerRightPin, GPIO.HIGH)
    GPIO.digitalWrite(ledLeftPin, GPIO.LOW)
    GPIO.digitalWrite(ledRightPin, GPIO.HIGH)

def resetSteer():
	GPIO.digitalWrite(motorSteerLeftPin, GPIO.LOW)
	GPIO.digitalWrite(motorSteerRightPin, GPIO.LOW)
	GPIO.digitalWrite(ledLeftPin, GPIO.LOW)
	GPIO.digitalWrite(ledRightPin, GPIO.LOW)

def flashAll():	
	GPIO.digitalWrite(ledLeftPin, GPIO.HIGH)
	GPIO.digitalWrite(ledRightPin, GPIO.HIGH)
	sleep(0.5)
	GPIO.digitalWrite(ledLeftPin, GPIO.LOW)
	GPIO.digitalWrite(ledRightPin, GPIO.LOW)
	sleep(0.5)
	GPIO.digitalWrite(ledLeftPin, GPIO.HIGH)
	GPIO.digitalWrite(ledRightPin, GPIO.HIGH)
	sleep(0.5)
	GPIO.digitalWrite(ledLeftPin, GPIO.LOW)
	GPIO.digitalWrite(ledRightPin, GPIO.LOW)

# stop the motors
def stop():
	GPIO.digitalWrite(motorDriveForwardPin, GPIO.LOW)
	GPIO.digitalWrite(motorDriveReversePin, GPIO.LOW)
	GPIO.digitalWrite(motorSteerLeftPin, GPIO.LOW)
	GPIO.digitalWrite(motorSteerRightPin, GPIO.LOW)
	GPIO.digitalWrite(ledLeftPin, GPIO.LOW)
	GPIO.digitalWrite(ledRightPin, GPIO.LOW)
	# motorLspeed, motorRspeed, acceleration
	initiate()
	return 0, 0, 0

# stop the motors
def stopSteer():
	GPIO.digitalWrite(motorSteerLeftPin, GPIO.LOW)
	GPIO.digitalWrite(motorSteerRightPin, GPIO.LOW)
	GPIO.digitalWrite(ledLeftPin, GPIO.LOW)
	GPIO.digitalWrite(ledRightPin, GPIO.LOW)


# This functions sets the motor speed.
def setacceleration(value):
	global motorDriveSpeed
	global motorSteerSpeed
	global acceleration
	global minspeed
	global maxspeed
	
	acceleration = acceleration + value
	
	minspeed, maxsteerspeed = getMinMaxSpeed()
	
	#Set Min and Max values for acceleration
	if(acceleration < -MAXSPEED):
		acceleration = -MAXSPEED
	
	if(acceleration > MAXSPEED):
		acceleration = MAXSPEED	
	
	if(acceleration > 0):
		# drive forward
		forward()
		motorDriveSpeed = acceleration
		#print("forward: ", motorLspeed, motorRspeed)
	elif(acceleration == 0):
		# stopp motors
		motorDriveSpeed = acceleration
		motorDriveSpeed, motorSteerSpeed, acceleration = stop()
		#print("stop: ", motorLspeed, motorRspeed)
	else:
		# drive backward
		reverse()
		motorDriveSpeed = (acceleration * -1)
		#print("backward: ", motorLspeed, motorRspeed)
	
	motorDriveSpeed, motorSteerSpeed = check_motorspeed(motorDriveSpeed, motorSteerSpeed)
	#print("check: ", motorLspeed, motorRspeed)

# This functions sets the motor speed.
def setturnacceleration(value):
	global motorDriveSpeed
	global motorSteerSpeed
	global turnacceleration
	global minspeed
	global maxsteerspeed
	
	turnacceleration = turnacceleration + value
	
	minspeed, maxsteerspeed = getMinMaxSteerSpeed()
	
	#Set Min and Max values for acceleration
	if(turnacceleration < -MAXSTEERSPEED):
		turnacceleration = -MAXSTEERSPEED
	
	if(turnacceleration > MAXSTEERSPEED):
		turnacceleration = MAXSTEERSPEED	
	
	if(turnacceleration > 0):
		# drive forward
		left()
		motorSteerSpeed = turnacceleration
		#print("forward: ", motorLspeed, motorRspeed)
	elif(turnacceleration == 0):
		# stopp motors
		motorSteerSpeed = turnacceleration
		motorSteerSpeed, turnacceleration = stopSteer()
		#print("stop: ", motorLspeed, motorRspeed)
	else:
		# drive backward
		right()
		motorSteerSpeed = (turnacceleration * -1)
		#print("backward: ", motorLspeed, motorRspeed)
	
	motorDriveSpeed, motorSteerSpeed = check_motorspeed(motorDriveSpeed, motorSteerSpeed)	

# check the motorspeed if it is correct and in max/min range
def check_motorspeed(motorDriveSpeed, motorSteerSpeed):
	if (motorDriveSpeed < minspeed):
		motorDriveSpeed = minspeed

	if (motorDriveSpeed > maxspeed):
		motorDriveSpeed = maxspeed
		
	if (motorSteerSpeed < minspeed):
		motorSteerSpeed = minspeed

	if (motorSteerSpeed > maxspeed):
		motorSteerSpeed = maxspeed	
		
	return motorDriveSpeed, motorSteerSpeed

# Set Min Max Speed
def getMinMaxSpeed():
	minspeed = 0
	maxspeed = 100
	return minspeed, maxspeed

# Set Min Max Speed
def getMinMaxSteerSpeed():
	minspeed = 0
	maxsteerspeed = 50
	return minspeed, maxsteerspeed
	
# Get the motor speed
def getMotorSpeed():
	global motorDriveSpeed
	global motorSteerSpeed
	
	return motorDriveSpeed, motorSteerSpeed

def getMotorSpeedStep():
	return 10	

def getSteerMotorSpeedStep():
	return 50		
	
@webiopi.macro
def ButtonForward():
	fowardAcc = 0
	fowardAcc = getMotorSpeedStep()

	setacceleration(fowardAcc)
	
	motorDriveSpeed, motorSteerSpeed = getMotorSpeed()
	
	# percent calculation	
	valueDrive =  float(motorDriveSpeed)/100
		
	GPIO.pulseRatio(motorDrivePWM, valueDrive)
	
@webiopi.macro
def ButtonReverse():
	backwardAcc = 0
	backwardAcc = getMotorSpeedStep()

	setacceleration((backwardAcc*-1))
	
	motorDriveSpeed, motorSteerSpeed = getMotorSpeed()
	
	# percent calculation
	valueDrive = float(motorDriveSpeed)/100
		
	GPIO.pulseRatio(motorDrivePWM, valueDrive)


@webiopi.macro
def ButtonTurnLeft():
	left()
	GPIO.pulseRatio(motorSteerPWM, 0.7)	
	sleep(0.3)
	resetSteer()

@webiopi.macro
def ButtonTurnRight():
	right()
	GPIO.pulseRatio(motorSteerPWM, 0.7)
	sleep(0.3)	
	resetSteer()

@webiopi.macro
def ButtonTurnLeftOld():
	global motorSteerSpeed
	global motorDriveSpeed
	global speedstep

	steerLeftAcc = 0
	steerLeftAcc = getSteerMotorSpeedStep()

	setturnacceleration((steerLeftAcc))
	
	motorDriveSpeed, motorSteerSpeed = getMotorSpeed()
	
	# percent calculation
	valueDrive = float(motorSteerSpeed)/100
		
	GPIO.pulseRatio(motorSteerPWM, valueDrive)
	
	#print("LEFT: ",valueL,valueR,spotturn)	
@webiopi.macro
def ButtonTurnRightOld():
	global motorSteerSpeed
	global motorDriveSpeed
	global speedstep

	steerRightAcc = 0
	steerRightAcc = getSteerMotorSpeedStep()

	setturnacceleration((steerRightAcc*-1))
	
	motorDriveSpeed, motorSteerSpeed = getMotorSpeed()
	
	# percent calculation
	valueDrive = float(motorSteerSpeed)/100
		
	GPIO.pulseRatio(motorSteerPWM, valueDrive)
	
	#print("RIGHT: ",valueL,valueR, spotturn)		

@webiopi.macro
def ButtonFlashAll():
	flashAll()

@webiopi.macro
def ButtonStop():	
	stop()
	flashAll()

initiate()