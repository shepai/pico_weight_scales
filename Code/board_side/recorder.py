"""
This code is used to record a dataset of weights
Record each weight individually and change the name each time.
Then you can use this data to make a regression model
"""

import storage
import os
import time
import board
import analogio
from digitalio import DigitalInOut, Direction, Pull
#data store
storage.remount("/",readonly=0)
filename="grams_120.csv"
# Initialize analog input on pin A0 (which is GP26 on the Raspberry Pi Pico)
analog_in = analogio.AnalogIn(board.GP26)
record = DigitalInOut(board.GP16)
record.direction = Direction.INPUT
record.pull = Pull.UP

led = DigitalInOut(board.GP21)
led.direction = Direction.OUTPUT

led.value=0

def get_voltage(pin):
    # Convert raw 16-bit ADC value (0-65535) to a voltage (0-3.3V)
    return (pin.value * 3.3) / 65535

recording=False
file=None
while True:
    raw_value = analog_in.value  # Get raw ADC value (0 to 65535)
    voltage = get_voltage(analog_in)  # Convert to voltage
    if not record.value:
        recording= not recording
        led.value= not led.value
        if type(file)!=type(None):
            file.close()
            file=None
        else:
            file=open(filename,"w")
    print([record.value,raw_value])
    #print(f"Raw ADC: {raw_value}, Voltage: {voltage:.2f}V")  # Print values
    #print(raw_value)
    if recording:
        file.write(str(voltage)+"\n")
    time.sleep(0.2)  # Delay to avoid flooding output

