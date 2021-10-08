'''
@file EncoderDriver.py
@brief A file that contains the EncoderDriver class
@details A file that controls intializes and controls an encoder
@author Kevin Lee and Fernando Estevez
@date March 9, 2021
'''
from pyb import Timer, Pin

class EncoderDriver:
    '''
    @brief class that controls an encoder
    @details class that controls and updates the position of an encoder
    '''
    def __init__(self, ENC1_pin, ENC2_pin, timer):
        '''
        @brief constructor for EncoderDriver class
        @details initializes the encoder pins and timer
        @param ENC1_pin pyb.Pin object, B6&7 or C6&7 for hardware 
        @param ENC2_pin pyb.Pin object, B6&7 or C6&7 for hardware
        @param timer Timer object, Timer(4, period=0xFFFF, prescaler=0) for 
        hardware
        '''
        print('Creating a encoder driver')
        ##encoder timer
        self.TIM = timer
        self.TIM.channel(1, mode=Timer.ENC_AB, pin=ENC1_pin)
        self.TIM.channel(2, mode=Timer.ENC_AB, pin=ENC2_pin)
        ##previous encoder value
        self.prev_val = 0
        ##current encoder value
        self.curr_val = 0
        ##encoder position
        self.position = 0
        ##conversion factor from ticks to radians
        self.ticksToRad = 2*3.1416/4000
        
    def update(self):
        '''
        @brief updates the position of the encoder
        @details accounts for overflow of the timer. works as long as readings 
        are less than Per/(2w) apart
        '''
        print('Updating position')
        self.prev_val = self.curr_val
        self.curr_val = self.TIM.counter()
        self.position += self.get_delta()
    
    def get_position(self):
        '''
        @brief returns the current encoder position
        @return int position in encoder ticks
        '''
        print('getting position')
        return self.position*self.ticksToRad
    
    def set_position(self, new_pos):
        '''
        @brief sets the position of the encoder
        @param new_pos int new encoder position
        '''
        self.position = new_pos
    
    def get_delta(self):
        '''
        @brief returns the delta from the previous two values
        @details corrects teh delta value in case of overflow/underflow
        @return int corrected delta in encoder ticks
        '''
        delta = self.curr_val - self.prev_val
        per = 0xFFFF
        if delta > per/2:
            return delta-per
        elif delta < -1*per/2:
            return delta + per
        return delta
    

if __name__ == '__main__':
    pin1 = pin=Pin.cpu.B6
    pin2 = pin=Pin.cpu.B7
    pin3 = pin=Pin.cpu.C6
    pin4 = pin=Pin.cpu.C7
    tim4 = Timer(4, period=0xFFFF, prescaler=0)  
    tim8 = Timer(8, period=0xFFFF, prescaler=0)

    ed1 = EncoderDriver(pin1, pin2, tim4)
    ed2 = EncoderDriver(pin3, pin4, tim8)