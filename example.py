import serial
from voice.protocol import *

if __name__ == '__main__':
    s = serial.Serial('/dev/ttyUSB0',9600,timeout=1)

    v = Voice(s)
    res = v.clear_recognizer()
    res = v.load_voice_record([0,1])
    print(res)
    res = v.recognize()
    print("Record {0} -> {1}".format(res['record'],res['signature']))
    s.close()