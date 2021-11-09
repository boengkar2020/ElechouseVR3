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
    my_parser.add_argument('-s','--start', action='store', type=int, required=True)
    my_parser.add_argument('-e','--end', action='store', type=int, required=True)
    args = my_parser.parse_args()
    serial_port = args.Device
    start = args.start
    end = args.end

    s = serial.Serial(serial_port,9600,timeout=1)
    
    v = Voice(s)
    #clear recognizer terlebih dahulu
    res = v.clear_recognizer()
    rec = [c for c in range(start,end + 1)]
    res = v.load_voice_record(rec)
    
    for rec in res['records']:
        print('Record {0} -> {1}'.format(rec['record'],rec['result']))

    s.close()