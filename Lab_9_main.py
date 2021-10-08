## @file Lab_9_main.py
#  Brief doc for Lab_9_main.py
#
#  Detailed doc for Lab_9_main.py
#  This is the main class for Lab 9 project
#
#  @author Fernando Estevez
#
#  @copyright License Info
#
#  @date March 16, 2021
from MotorDriver import MotorDriver
from EncoderDriver import EncoderDriver
from TouchPanel import TouchPanel
from pyb import Pin, Timer, I2C, ExtInt
import utime

## i2c communication object
i2c = I2C(1, I2C.MASTER)

## Define all our pins used for the Touch Pannel
touchXP = Pin.board.PA7
touchYP = Pin.board.PA6
touchXM = Pin.board.PA1
touchYM = Pin.board.PA0
## Width of the touch panel in meters (m)
width = .100
## Length of the touch panel in meters (m)
length = .176
## Center of the touch panel
center = (0,0)

## Creating a touch screen object 
touch = TouchPanel(touchXM, touchYM, touchXP, touchYP, width, length, center)

## Define all pins for the encoder driver
encoderPin1 = pin=Pin.cpu.B6
encoderPin2 = pin=Pin.cpu.B7
encoderPin3 = pin=Pin.cpu.C6
encoderPin4 = pin=Pin.cpu.C7

## Creating a Timer 4 object 
timer4 = Timer(4, period=0xFFFF, prescaler=0)
## Creating a Timer 8 object
timer8 = Timer(8, period=0xFFFF, prescaler=0)

## Creting an encoder driver 1 object
encoder1 = EncoderDriver(encoderPin1, encoderPin2, timer4)
## Creating an encoder driver 2 object
encoder2 = EncoderDriver(encoderPin3, encoderPin4, timer8)

## Define all pins for motor driver
MotorPIN1 = Pin.cpu.B4
MotorPIN2 = Pin.cpu.B5
MotorPIN3 = Pin.cpu.B0
MotorPIN4 = Pin.cpu.B1
nSLEEP = Pin(Pin.cpu.A15, mode=Pin.OUT_PP, value=1)

## Creating a Timer 3 object
timer3 = Timer(3, freq=20000)
## Creating a motor driver object for both motors
motors = MotorDriver(nSLEEP, MotorPIN1, MotorPIN2, 
                     MotorPIN3, MotorPIN4, timer3)
# Enable the motors
motors.enable()

## Global Flag that toggles to True when the system detects a fault.
faultDetected = False


## External interupt callback method called when nFAULT is triggered
#
#  When call back is triggered, it toggles the fault detected flag to true
#  and disables the motors
#  @param Pin
def callback(Pin):
    global faultDetected
    faultDetected = True
    print('fault detected callback')
    motors.disable()

## External interupt callback method to clear nFAULT trigger
#
#  When button is pressed, reenables motor if a fault was triggered. 
#  Also serves as a way to disable the motor if the fault is not triggered.
#  @param Pin
def clear_fault(Pin):
    print('button callback')
    global faultDetected
    if faultDetected:
        #reenable motor
        externInterupt.disable()
        faultDetected = False
        motors.enable()
        externInterupt.enable()
    else:
        #emergency shutoff button
        faultDetected = True
        motors.disable()

## Active-low pin FAULT with a pull-up resistor that isasserted low by the 
# DRV8847 when it detects a fault. 
nFault = Pin(Pin.board.PB2, Pin.IN, Pin.PULL_UP)
## Blue button pin on Nucleo L476
button = Pin(Pin.board.PC13, Pin.IN, Pin.PULL_UP)

## Sets up an external interupt when a nFault goes low
externInterupt = ExtInt(nFault, mode=ExtInt.IRQ_FALLING, pull = Pin.PULL_UP,
                        callback=callback)

## Sets up an external interupt when the blue button is pressed
externInterupt_button = ExtInt(button, mode=ExtInt.IRQ_FALLING, 
                               pull = Pin.PULL_UP, callback=clear_fault)

## Main function to run the main program. 
def main():
    # K values based on pizza post
    # K = [-3.2839,-9,-9.0905,-3.9995]
    # Controller Gain Tunning 
    K = [90, -10, 75, -47]
    
    R = 2.21
    Vdc = 12
    Kt = 0.0138    
    
    # Angle for the encoder
    encoderAng = (0,0)

    # time of last encoder reading
    encoderTime = utime.ticks_ms()

    # Initial position of the ball
    ballPos = (0,0,False)
    ballTime = utime.ticks_ms()
    # Set motors off
    motors.set_duty(1, 0)
    motors.set_duty(2, 0)

    while True:
        # Read from the touch panel
        newBallPos = touch.scan()
        # Calculate the change on time since last time ball time was read
        balldt = utime.ticks_diff(utime.ticks_ms(), ballTime)/1000
        ballTime = utime.ticks_ms()
        # Only initiate balancing protocall if touchpanel detects a ball 
        if(ballPos[2]):
            # Get the x position of the ball
            xBall = newBallPos[0]
            # Calculate the velocity of the ball
            xDotBall = (xBall - ballPos[0])/ balldt
            
            # Get the y position of the ball
            yBall = newBallPos[1]
            # Calculate the velocity of the ball
            yDotBall = (yBall - ballPos[1])/ balldt
            
            # Update the encoder 
            encoder1.update()
            encoder2.update()
            
            # Get the theta angles of each encoder
            newEncAng = (encoder1.get_position(), encoder2.get_position())
            # Calculate the change in time for the theat angle 
            encoderdt = utime.ticks_diff(utime.ticks_ms(), encoderTime)/1000
            encoderTime = utime.ticks_ms()
            # Calculate angular Velocity
            ythetaDot = (newEncAng[1] - encoderAng[1])/ encoderdt
            xthetaDot = (newEncAng[0] - encoderAng[0])/encoderdt
            encoderAng = newEncAng
            
            # Check to see if the ball is on the platform 
            if newBallPos[2]:
                # Calculate the torque for x and y
                TorqueX = -K[0]*yDotBall - K[1]*xthetaDot - K[2]*yBall - K[3]*newEncAng[0]
                TorqueY = -K[0]*xDotBall - K[1]*ythetaDot - K[2]*xBall - K[3]*newEncAng[1]  
                # Calculate the dutyCylce for x and y 
                dutyCycleY = TorqueY * (R/(Vdc*Kt))
                dutyCycleX = TorqueX * (R/(Vdc*Kt))
                
            # If ball is not on the platform set duty cycle to zero
            else:
                dutyCycleY = 0
                dutyCycleX = 0
                
            # Only accep duty cycle readings if they are with in 30 to 70 % 
            #if dutyCycleX <= 70 and dutyCycleX >= 30 and dutyCycleY <= 70 and dutyCycleY >= 30:
            # Update motors
            motors.set_duty(1, dutyCycleX/2)
            motors.set_duty(2, dutyCycleY/2)

        #Update the ball positon 
        ballPos = newBallPos
        

if __name__ == '__main__':
    main()
