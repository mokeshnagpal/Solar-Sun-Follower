from time import sleep
from machine import Pin, ADC
from servo import Servo
import _thread

photo_resistor_down = ADC(27)
photo_resistor_up = ADC(26)
photo_resistor_motor = ADC(28)

servo_up_down = Servo(pin_id=16)

motor_left_right_pin_a = Pin(0,Pin.OUT)
motor_left_right_pin_b = Pin(1,Pin.OUT)

threshold = 1000
one_degree_motor_time = 1/360
five_degree_up_down_time = (5*1.2)/90
duty = 90
degree= 0
servo_up_down.write(90)
servo_up=0
servo_down=0

def right_left():
    global duty
    global threshold
    global servo_up
    global servo_down
    while 1:
        servo_up=photo_resistor_up.read_u16()
        servo_down=photo_resistor_down.read_u16()
        difference_up_down = servo_up - servo_down
        if(difference_up_down > threshold and duty !=180):  #to move up
            duty += 1          
            servo_up_down.write(110)
            sleep(five_degree_up_down_time)
            servo_up_down.write(90)
        elif(difference_up_down < -threshold and duty !=0):  #to move left
            duty -= 1 
            servo_up_down.write(80)
            sleep(five_degree_up_down_time)
            servo_up_down.write(90)
        sleep(0.5)
        
_thread.start_new_thread(right_left, ())     
while 1:
    avg_compare_val = (servo_up+servo_down)/2
    if(abs(avg_compare_val-photo_resistor_motor.read_u16())<threshold):
        motor_left_right_pin_a.value(0)
        motor_left_right_pin_b.value(1)
        sleep(5*one_degree_motor_time)
        motor_left_right_pin_b.value(0)
        degree+=10
    sleep(0.5)
    