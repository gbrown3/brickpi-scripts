# My first attempt at writing a custom script for a BrickPi3 robot. 
# Currently, my plan for the "Gorniebot" is to make a bot that is 
# set up with a launcher similar to another project, which will roam
# around and shoot anything that moves.

# Everything below is copied from https://github.com/DexterInd/BrickPi3/blob/master/Software/Python/Examples/LEGO-Motors.py.

# When this runs, the motor(s) speed will ramp up and down while the touch sensor is pressed. The position for each motor will be printed.
import brickpi3
import time

BP = brickpi3.BrickPi3()

BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH) # Configure for a touch sensor
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.NXT_ULTRASONIC) # Configure for ultrasonic sensor (measures distance)


try:
    print("Press touch sensor on port 1 to start")
    touch_input = 0 # value received from touch sensor, indicates how far sensor is pressed
    ultrasonic_input = 0 # value received from ultrasonic senso, indicates how far away objects are from the sensor

    # Wait for touch sensor to be pressed | GB: not sure this is needed, try removing and see what breaks
    while not touch_input:
        try:
            touch_input = BP.get_sensor(BP.PORT_1)
        except brickpi3.SensorError:
            pass
    
    speed = 50
    while True:
        # Get input from ultrasonic sensor
        try:
            distance = BP.get_sensor(BP.PORT_2) # get distance to closest object in CM, with 255 CM as max range
            print(f'Closest object is {distance} CM away')
        except brickpi3.SensorError as error:
            print(error)

        # Get input from touch sensor
        #
        # BP.get_sensor retrieves a sensor value.
        # BP.PORT_1 specifies that we are looking for the value of sensor port 1.
        try:
            touch_input = BP.get_sensor(BP.PORT_1)
        except brickpi3.SensorError as error:
            print(error)
            touch_input = 0
        
        if not touch_input:
            speed = 0   # Stop motor if touch sensor is no longer being pressed
        else:
            speed = 50    
        
        # Set the motor speed for all four motors
        BP.set_motor_power(BP.PORT_A + BP.PORT_B + BP.PORT_C + BP.PORT_D, speed) 
        
        time.sleep(0.02)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.