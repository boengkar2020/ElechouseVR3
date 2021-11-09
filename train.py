'''
Created by Sukarno 
Email : sukarnooke@gmail.com
'''

import argparse
import serial
from voice.protocol import *

if __name__ == '__main__':
    my_parser = argparse.ArgumentParser(description='Voice recognizer Train Test')
    my_parser.add_argument('Device',
                       metavar='device',
                       type=str,
                       help='Serial port device')
    my_parser.add_argument('-r','--record', action='store', type=int, required=True)
    my_parser.add_argument('-s','--signature', action='store', type=str, required=True)
    args = my_parser.parse_args()
    serial_port = args.Device
    record = args.record
    signature = args.signature

    s = serial.Serial(serial_port,9600,timeout=1)
    
    v = Voice(s)
    print("--------- Record Procedure Record : {0} {1}-----------".format(record,signature))
    res = v.train_with_signature(record,signature)
    print('------------------------------------------------------')
    s.close()