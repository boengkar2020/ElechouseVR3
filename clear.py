'''
Created by Sukarno 
Email : sukarnooke@gmail.com
'''

import argparse
import serial
from voice.protocol import *

if __name__ == '__main__':
    my_parser = argparse.ArgumentParser(description='Voice recognizer clear command')
    my_parser.add_argument('Device',
                       metavar='device',
                       type=str,
                       help='Serial port device')
    
    args = my_parser.parse_args()
    serial_port = args.Device
    

    s = serial.Serial(serial_port,9600,timeout=1)
    
    v = Voice(s)
    res = v.clear_recognizer()
    print('Clear process -> {}'.format(res['status']))
    s.close()