import minimalmodbus

class TC:
    def __init__(self, slave_address=1, serial_port='/dev/ttyUSB0', timeout=0.25, baud_rate=9600, decimal=0, debug=False):
        self.instrument = minimalmodbus.Instrument(serial_port, slave_address, debug=debug)
        self.instrument.serial.baudrate = baud_rate
        self.instrument.serial.timeout = timeout
        self.decimal = 1 if (0 < decimal < 2) else 0
        self.write_register(641, self.decimal, 0)  # Set decimal

    def write_register(self, address, value, decimal_points=0):
        signed = value < 0
        self.instrument.write_register(address, value, decimal_points, functioncode=6, signed=signed)

    def read_register(self, address, decimal_points=0):
        return self.instrument.read_register(address, decimal_points, functioncode=3)

    def get_power(self):
        return self.read_register(4, 2)

    def tune_pid(self, enable=True):
        self.write_register(696, 1 if enable else 0)

    def get_pid_params(self):
        p = self.read_register(700, self.decimal)
        i = self.read_register(701, self.decimal)
        d = self.read_register(702, self.decimal)
        return [p, i, d]

    def set_temperature(self, value, range_=2):
        high = value + range_
        low = value - range_

        # Set alarm configuration first
        self.write_register(666, 4)  # Set alarm type
        self.write_register(667, 5)  # Set alarm function
        self.write_register(668, high * (10 ** self.decimal), self.decimal)  # Set high alarm
        self.write_register(669, low * (10 ** self.decimal), self.decimal)  # Set low alarm
        self.write_register(660, 3)  # Set output function
        self.write_register(661, 1)  # Set alarm linkage

        # Then set the temperature
        value_scaled = value * (10 ** self.decimal)
        self.write_register(6, value_scaled, self.decimal)  # Set temperature

    def get_temperature(self):
        return self.read_register(1, self.decimal) / (10 ** self.decimal)

    def reset_to_defaults(self):
        self.write_register(19, -481)
