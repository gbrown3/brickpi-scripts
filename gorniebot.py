# My first attempt at writing a custom script for a BrickPi3 robot. 
# Currently, my plan for the "Gorniebot" is to make a bot that is 
# set up with a launcher similar to another project, which will roam
# around and shoot anything that moves.

# Everything below is copied from https://github.com/DexterInd/BrickPi3/blob/master/Software/Python/Examples/LEGO-Motors.py.

# When this runs, the motor(s) speed will ramp up and down while the touch sensor is pressed. The position for each motor will be printed.
import brickpi3
import time

BP = brickpi3.BrickPi3()

BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH) # Configure for a touch sensor)

try:
    print("Press touch sensor on port 1 to run motors")
    value = 0

    # Wait for touch sensor to be pressed | GB: not sure this is needed, try removing and see what breaks
    while not value:
        try:
            value = BP.get_sensor(BP.PORT_1)
        except brickpi3.SensorError:
            pass
    
    speed = 0
    adder = 1
    while True:
        # BP.get_sensor retrieves a sensor value.
        # BP.PORT_1 specifies that we are looking for the value of sensor port 1.
        # BP.get_sensor returns the sensor value.
        try:
            value = BP.get_sensor(BP.PORT_1)
        except brickpi3.SensorError as error:
            print(error)
            value = 0
        
        if value:                             # if the touch sensor is pressed
            if speed <= -100 or speed >= 100: # if speed reached 100, start ramping down. If speed reached -100, start ramping up.
                adder = -adder
            speed += adder
        else:                                 # else the touch sensor is not pressed or not configured, so set the speed to 0
            speed = 0
            adder = 1
        
        # Set the motor speed for all four motors
        BP.set_motor_power(BP.PORT_A + BP.PORT_B + BP.PORT_C + BP.PORT_D, speed)
        
        try:
            # Each of the following BP.get_motor_encoder functions returns the encoder value (what we want to display).
            print("Encoder A: %6d  B: %6d  C: %6d  D: %6d" % (BP.get_motor_encoder(BP.PORT_A), BP.get_motor_encoder(BP.PORT_B), BP.get_motor_encoder(BP.PORT_C), BP.get_motor_encoder(BP.PORT_D)))
        except IOError as error:
            print(error)    
        
        time.sleep(0.02)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.