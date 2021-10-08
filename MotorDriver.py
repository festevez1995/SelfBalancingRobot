'''
@file MotorDriver.py
@brief A file that contains the MotorDriver class
@details A file that controls intializes and controls a motor
@author Kevin Lee and Fernando Estevez
@date March 9, 2021
'''

from pyb import Timer, Pin

class MotorDriver:
    '''
    @brief class that controls a motor
    @details class that enables, disables, and sets the duty cycle of a motor
    '''
    
    def __init__(self, nSLEEP_pin, IN1_pin, IN2_pin, IN3_pin, IN4_pin, timer):
        '''
        @brief constructor for MotorDiver class
        @details initializes the motor timer, input pins and nSLEEP pin
        @param nSLEEP_pin pyb.Pin object, A15 for hardware
        @param IN1_pin pyb.Pin object, use B4 for hardware
        @param IN2_pin pyb.Pin object, use B5 for hardware
        @param IN3_pin pyb.Pin object, use B0 for hardware
        @param IN4_pin pyb.Pin object, use B1 for hardware
        @param timer Timer object Timer 3 at 20000Hz for hardware
        '''
        print('Creating a motor driver')
        ##motor timer
        self.TIM = timer
        ##motor pin 1
        self.IN1 = self.TIM.channel(1, mode=Timer.PWM, pin=IN1_pin)
        ##motor pin 2
        self.IN2 = self.TIM.channel(2, mode=Timer.PWM, pin=IN2_pin)
        ##motor pin 3
        self.IN3 = self.TIM.channel(3, mode=Timer.PWM, pin=IN3_pin)
        ##motor pin 4
        self.IN4 = self.TIM.channel(4, mode=Timer.PWM, pin=IN4_pin)
        ##nSLEEP pin
        self.nSLEEP = Pin(nSLEEP_pin, mode=Pin.OUT_PP, value=1)
        ##max motor duty
        self.MAX = 100
        
    def enable(self):
        '''
        @brief enables the motor
        @details sets the nSLEEP pin high
        '''
        print('Enabling motors')
        self.nSLEEP.high()
        
    def disable(self):
        '''
        @brief disables the motor
        @details sets the nSLEEP pin low
        '''
        print ('Disabling motors')
        self.nSLEEP.low()
        
    def set_duty(self, motor_number, duty):
        '''
        @brief sets the duty of the motor
        @details inputing a positive value rotates the motor fwd and inputting 
        a negative value for reverse
        @param motor_number int 1 or 2 signifies which motor to power
        @param duty int value between -100 and 100, "+" for fwd, "-" for rev
        '''
        # print('Set duty for motor ' + str(motor_number) + ": " + str(duty))
        if motor_number ==1:
            if duty >0:  
                #fwd
                self.IN1.pulse_width_percent(min(duty,self.MAX))
                self.IN2.pulse_width_percent(0) 
            else:
                #rev
                self.IN1.pulse_width_percent(0)
                self.IN2.pulse_width_percent(min(-1*duty,self.MAX))
        elif motor_number ==2:
            if duty >0:  
                #fwd
                self.IN3.pulse_width_percent(min(duty,self.MAX))
                self.IN4.pulse_width_percent(0) 
            else:
                #rev
                self.IN3.pulse_width_percent(0)
                self.IN4.pulse_width_percent(min(-1*duty,self.MAX))
        else: 
            print("invalid motor number \ntry 1 or 2")
    
if __name__ == '__main__':
    nSLEEP = Pin(Pin.cpu.A15, mode=Pin.OUT_PP, value=1)
    tim = Timer(3, freq=20000)
    IN1 = Pin.cpu.B4
    IN2 = Pin.cpu.B5
    IN3 = Pin.cpu.B0
    IN4 = Pin.cpu.B1

    md = MotorDriver(nSLEEP, IN1, IN2, IN3, IN4, tim)
    
    md.enable()
    md.set_duty(10)






