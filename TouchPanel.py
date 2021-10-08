## @file TouchPanel.py
#  Brief doc for TouchPanel.py
#
#  Detailed doc for TouchPanel.py
#  This is a class for the touch panel
#
#  @author Fernando Estevez
#
#  @copyright License Info
#
#  @date Febuary 27, 2021
import pyb
import utime

## Touch panel class 
class TouchPanel:
    
    ## Constructor for the TouchPanel Class
    #
    #  Constructor allows users to select their pins. As well as set their
    #  width, lenght and center position.
    #
    #  @param PinXm Arbitrary Pin for Xm
    #  @param PinYm Arbitrary Pin for Ym
    #  @param PinXp Arbitrary Pin for Xp
    #  @param PinYp Arbitrary Pin for Yp
    #  @param w Width of the touch panel
    #  @param l Lenght of the touch pannel
    #  @param c Center of the touch pannel
    def __init__(self, PinXm, PinYm, PinXp, PinYp, w, l, c):
        self.Xm = pyb.Pin(PinXm, pyb.Pin.OUT_PP)
        self.Ym = pyb.Pin(PinYm, pyb.Pin.OUT_PP)
        self.Xp = pyb.Pin(PinXp, pyb.Pin.OUT_PP)
        self.Yp = pyb.Pin(PinYp, pyb.Pin.OUT_PP)
        self.width  = w
        self.length = l
        self.center = c
        self.ADCVal = 4000
        self.totalTime = 0

        
    ## Scan X direction
    #
    #  Scans the x, horizontal location of the contact point.
    #  @returns X postiont of the ball 
    def x_scan(self):
        startTime = utime.ticks_us()
        # Pin Xp configured to push-pull ouput and set to high
        self.Xp.init(mode=pyb.Pin.OUT_PP, value=1)
        # Pin Xm configured to pushh-pull ouput and set to low
        self.Xm.init(mode=pyb.Pin.OUT_PP, value=0)
        # Floating Yp
        self.Yp.init(mode=pyb.Pin.IN)
        # Configure pin Ym to read a voltage from 
        self.Ym.init(mode=pyb.Pin.ANALOG)
        # Create a ADC object used on pin Ym
        YmADC = pyb.ADC(self.Ym)
        endTime = utime.ticks_us()
        # Calculate total time 
        self.totalTime += utime.ticks_diff(endTime, startTime)
        return(YmADC.read() - 
               self.ADCVal/2)*self.length/self.ADCVal - self.center[0]

    ## Scan Y direction
    #
    #  Scans the y, Vertical location of the contact point.
    #  @returns Y postiont of the ball 
    def y_scan(self):
        startTime = utime.ticks_us()
        # Pin Xp configured to push-pull ouput and set to high
        self.Yp.init(mode=pyb.Pin.OUT_PP, value=1)
        # Pin Xm configured to pushh-pull ouput and set to low
        self.Ym.init(mode=pyb.Pin.OUT_PP, value=0)
        # Floating Xp
        self.Xp.init(mode=pyb.Pin.IN)
        # Crate an ADC object from pin Xm
        self.Xm.init(mode=pyb.Pin.ANALOG)
        XmADC = pyb.ADC(self.Xm)
        endTime = utime.ticks_us()
        #Calcualte the total time 
        self.totalTime += utime.ticks_diff(endTime, startTime)
        return (XmADC.read() - self.ADCVal/2
                )*self.width/self.ADCVal - self.center[1]
    
    ## Scan Z 
    #
    #  Scaning Z determins whether or not their is contact on the touch panel.
    #  @returns boolean returns true if their is contact on panel else false
    def z_scan(self):
        startTime = utime.ticks_us()
        # Pin Xp configured to push-pull ouput and set to high
        self.Yp.init(mode=pyb.Pin.OUT_PP, value=1)
        # Pin Xm configured to pushh-pull ouput and set to low
        self.Xm.init(mode=pyb.Pin.OUT_PP, value=0)
        # Floating Xp
        self.Xp.init(mode=pyb.Pin.IN)
        # Crate an ADC object from pin Ym
        self.Ym.init(mode=pyb.Pin.ANALOG)
        YmADC = pyb.ADC(self.Ym)
        endTime = utime.ticks_us()
        self.totalTime += utime.ticks_diff(endTime, startTime)
        # Check if the volateg reading is High return true
        if YmADC.read() > self.ADCVal:
            return False
        
        # else no conntact is made on the panel
        return True
        
    
    ## Scan X direction
    #
    #  Scans the x, horizontal location of the contact point.
    #  @returns X postiont of the ball 
    def scan(self):
        return self.x_scan(), self.y_scan(), self.z_scan()
    
    ## Get total time
    # Returns the total time it took to run the system 
    def get_Total_Time(self):
        return self.totalTime