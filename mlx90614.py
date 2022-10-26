import smbus
from time import sleep


class MLX90614:

    def __init__(self, channel=1, address=0x5a):
        # Get I2C bus
        self.channel = channel
        self.bus = smbus.SMBus(self.channel)
        self.address = address

    # MLX90614 ambient temperature data address, 0x06
    # MLX90614 ambient object data address, 0x07
    def read(self):

        self.bus.write_byte_data(self.address, 0x07, 0x01)
        object_temp = self.bus.read_i2c_block_data(self.address, 0x07, 3)

        object_temperature = object_temp[1] * 256 + object_temp[0]
        object_temperature = (object_temperature * 0.02) - 0.01
        object_temperature = object_temperature - 273.15

        self.bus.write_byte_data(self.address, 0x06, 0x01)
        ambient_temp = self.bus.read_i2c_block_data(self.address, 0x06, 3)

        ambient_temperature = ambient_temp[1] * 256 + ambient_temp[0]
        ambient_temperature = (ambient_temperature * 0.02) - 0.01
        ambient_temperature = ambient_temperature - 273.15

        return ambient_temperature, object_temperature
