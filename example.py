import serial
from voice.protocol import *

if __name__ == '__main__':
    s = serial.Serial('/dev/ttyUSB0',9600,timeout=1)

    v = Voice(s)

    res = v.clear_recognizer()

    print(res)

    s.close()