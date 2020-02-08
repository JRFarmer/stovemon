import spidev
import ctypes

def ctof(celsius):
    return celsius * 180 / 100 + 32

class Data(ctypes.BigEndianStructure):
    _fields_ = [
        ("temperature",     ctypes.c_int32,     14),
        ("reserved_d17",    ctypes.c_uint32,    1),
        ("fault",           ctypes.c_uint32,    1),
        ("cold_junction",   ctypes.c_int32,     12),
        ("reserved_d03",    ctypes.c_uint32,    1),
        ("short_vcc",       ctypes.c_uint32,    1),
        ("short_gnd",       ctypes.c_uint32,    1),
        ("open_circuit",    ctypes.c_uint32,    1),
    ]

    def to_dict(self):
        r = {}
        r["temperature"]    = ctof(self.temperature / 4)
        r["fault"]          = bool(self.fault)
        r["cold_junction"]  = ctof(self.cold_junction / 16)
        r["short_vcc"]      = bool(self.short_vcc)
        r["short_gnd"]      = bool(self.short_gnd)
        r["open_circuit"]   = bool(self.open_circuit)
        return r

# should be same as ctypes.sizeof(Data)
READ_SIZE = 4

MAX_SPEED_HZ = 5000000
STD_SPEED_HZ = 1000000 # use slower speed for stability

class MAX31855:

    def __init__(self, bus, cs, hz=STD_SPEED_HZ):
        self.sd = spidev.SpiDev(bus, cs)
        self.hz = hz

    def read(self):

        # read the bus
        self.sd.max_speed_hz = self.hz
        d = self.sd.readbytes(READ_SIZE)

        # format and return the data
        s = Data.from_buffer_copy(bytes(d))
        return s.to_dict()
