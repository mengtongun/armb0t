# From https://github.com/araffin/python-arduino-serial
from robust_serial import Order, write_order, write_i8, write_i16
from robust_serial.utils import open_serial_port

# Open serial port with a baudrate of 9600 (bits/s)
serial_file = open_serial_port(baudrate=9600)

# Send the order "MOTOR", i.e. to change the speed of the car
# equivalent to write_i8(serial_file, Order.MOTOR.value)
write_order(serial_file, Order.MOTOR)
# with parameter speed=56 (going forward at 56% of the maximum speed)
# The parameter "speed" is encoded as a 8 bits (1 bytes) signed int
write_i8(serial_file, 56)

# Send the order "SERVO",
# i.e. to change the direction of the car (the servomotor is controlled in angle)
write_order(serial_file, Order.SERVO)
# with parameter angle=156°
# The parameter "angle" is encoded as a 16 bits (2 bytes) signed int
write_i16(serial_file, 156)
