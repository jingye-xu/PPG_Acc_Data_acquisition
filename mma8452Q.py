import smbus


class MMA8452Q:

    def __init__(self, channel=1, address=0x1d):
        # Get I2C bus
        self.channel = channel
        self.bus = smbus.SMBus(self.channel)
        self.address = address

        # MMA8452Q address, 0x1D
        # Select Control register, 0x2A(42)
        #       0x00(00)    StandBy mode
        self.bus.write_byte_data(self.address, 0x2A, 0x00)
        # MMA8452Q address, 0x1D
        # Select Control register, 0x2A(42)
        #       0x01(01)    Active mode
        self.bus.write_byte_data(self.address, 0x2A, 0x01)
        # MMA8452Q address, 0x1D
        # Select Configuration register, 0x0E(14)
        #       0x00(00)    Set range to +/- 2g
        self.bus.write_byte_data(self.address, 0x0E, 0x00)

    # MMA8452Q address, 0x1D
    # Read data back from 0x00(0), 7 bytes
    # Status register, X-Axis MSB, X-Axis LSB, Y-Axis MSB, Y-Axis LSB, Z-Axis MSB, Z-Axis LSB
    def read(self):

        data = self.bus.read_i2c_block_data(self.address, 0x00, 7)

        # Convert the data
        x_accl = (data[1] * 256 + data[2]) / 16
        if x_accl > 2047:
            x_accl -= 4096

        y_accl = (data[3] * 256 + data[4]) / 16
        if y_accl > 2047:
            y_accl -= 4096

        z_accl = (data[5] * 256 + data[6]) / 16
        if z_accl > 2047:
            z_accl -= 4096

        return x_accl, y_accl, z_accl
