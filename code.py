from time import sleep
from machine import Pin, ADC
from servo import Servo
from BlynkLib import Blynk
from network import WLAN,STA_IF

SSID = 'MAJESTIC MOKSH'
PASS = 'Mokesh87654321' 
BLYNK_AUTH = "AF4pnHjYEC07_W2oAFxRys3JTPTeWJF4"

wifi = WLAN(STA_IF)
wifi.active(True)
try:
    wifi.connect(SSID, PASS)

    while not wifi.isconnected():
        pass
    print('Connected to WiFi')
    sleep(2)
    print('IP address: ',wifi.ifconfig()[0])
    sleep(2)
except Exception as e:
    pass

blynk = Blynk(BLYNK_AUTH)

photo_resistor_up = ADC(Pin(4,Pin.IN))
photo_resistor_up.width(ADC.WIDTH_10BIT)
photo_resistor_up.atten(ADC.ATTN_11DB)
photo_resistor_down = ADC(Pin(4,Pin.IN))
photo_resistor_down.width(ADC.WIDTH_10BIT)
photo_resistor_down.atten(ADC.ATTN_11DB)
photo_resistor_left = ADC(Pin(4,Pin.IN))
photo_resistor_left.width(ADC.WIDTH_10BIT)
photo_resistor_left.atten(ADC.ATTN_11DB)
photo_resistor_right = ADC(Pin(4,Pin.IN))
photo_resistor_right.width(ADC.WIDTH_10BIT)
photo_resistor_right.atten(ADC.ATTN_11DB)


my_servo = Servo(pin_id=16)

motor_left_right_pin_a = Pin(0,Pin.OUT)
motor_left_right_pin_b = Pin(1,Pin.OUT)

threshold = 100
one_degree_right_left_time = 1/360
one_degree_up_down_time = 1.2/90
duty = 90
degree= 0
servo_up_down.move(90)


while 1:
    difference_up_down = GPIO.input(photo_resistor_up) - GPIO.input(photo_resistor_down)
    if(difference_up_down > threshold and duty !=180):  #to move up
        duty += 1          
        servo_up_down.move(100)
        sleep(one_degree_up_down_time)
        servo_up_down.move(90)
    elif(difference_up_down < -threshold and duty !=0):  #to move left
        duty -= 1 
        servo_up_down.move(80)
        sleep(one_degree_up_down_time)
        servo_up_down.move(90)
    difference_left_right = GPIO.input(photo_resistor_left) - GPIO.input(photo_resistor_right)
    if(difference_left_right > threshold):  #to move left
        if(degree == 359):
            motor_left_right_pin_b.value(1)
            motor_left_right_pin_a.value(0)
            degree=0
            sleep(one_degree_right_left_time*359)
            motor_left_right_pin_b.value(0)
        else:
            motor_left_right_pin_a.value(1)
            motor_left_right_pin_b.value(0)
            sleep(one_degree_right_left_time)
            degree+=1
            motor_left_right_pin_a.value(0)
    elif(difference < -threshold and duty > one_degree_change):  #to move right
        if(degree == 0):
            motor_left_right_pin_a.value(1)
            motor_left_right_pin_b.value(0)
            degree=0
            sleep(one_degree_right_left_time*359)
            motor_left_right_pin_a.value(0)
        else:
            motor_left_right_pin_b.value(1)
            motor_left_right_pin_a.value(0)
            degree-=1
            sleep(one_degree_right_left_time)
            motor_left_right_pin_b.value(0)
    blynk.virtual_write(0,duty)  #elevation
              
