import time

class Command:
    Check_System = 0x00
    Check_Recognizer = 0x01
    Check_Record_Train_Status = 0x02
    Check_Signature_One_record = 0x03
    Restore_System = 0x10
    Set_Baudrate = 0x11
    Set_IO_Mode = 0x12
    Set_IO_Pulse_Width = 0x13
    Reset_Output_IO = 0x14
    Set_Power_On_Auto_Load = 0x15
    Train = 0x20
    Train_With_Signature = 0x21
    Set_Signature = 0x22
    Load = 0x30
    Clear_Recognizer = 0x31
    Group_Control = 0x32

class TrainStatus:
    Untrained = 0x00
    Trained = 0x01
    Out_Of_Range = 0xFF

class BaudRate:
    B9600 = 0
    B2400 = 1
    B4800 = 2
    B19200 = 4
    B38400 = 5

class IOMode:
    Pulse = 0
    Toggle = 1
    Clear = 2
    Set = 3

class AutoLoad:
    Disable = 0
    Enable = 1

class GroupControl:
    Disable = 0
    System_Group = 1
    User_Group = 2

class PulseWidth:
    P10MS = 0x00
    P15MS = 0x01
    P20MS = 0x02
    P25MS = 0x03
    P30MS = 0x04
    P35MS = 0x05
    P40MS = 0x06
    P45MS = 0x07
    P50MS = 0x08
    P75MS = 0x09
    P100MS = 0xA
    P200MS = 0xB
    P300MS = 0xC
    P400MS = 0xD
    P500MS = 0xE
    P1S = 0xF

class BitMap:
    Zero = 0
    One = 1
    Two = 3
    Three = 7
    Four = 0xF
    Five = 0x1F
    Six = 0x3F
    Seven = 0x7F

class Voice(object):
    def __init__ (self,serial_port):
        self.__serial = serial_port
        #assert self.__serial.is_open(), 'Serial Port not Open'


    def __create_frame(self,data):

        assert isinstance(data,list), 'Parameter data harus list'
        assert len(data) != 0, 'Data yang akan dikirim kosong'

        frame_length = len(data) + 1

        frame = b'\xaa' + bytes([frame_length]) + bytes(data) + b'\x0a'

        return frame

    def __read_frame(self):
        
        while True:
            try:
                resp = self.__serial.read()
            except:
                continue

            if not resp:
                continue

            time.sleep(0.2)

            while self.__serial.in_waiting > 0:
                resp += self.__serial.read(self.__serial.in_waiting)

            break

        if resp[0] != 0xaa:
            return []

        data = resp[2:-1]

        return list(data)

    def check_system_setting (self):
        frame = self.__create_frame([Command.Check_System])

        self.__serial.write(frame)

        resp = self.__read_frame()

        if not resp:
            return {'status' : 'No response'}

        if resp[0] != Command.Check_System:
            return {'status' : 'Command Response mismatch'}

        obj = {}

        if resp[1] == TrainStatus.Untrained:
            obj['trained_status'] = 'Untrained'
        elif resp[1] == TrainStatus.Trained:
            obj['trained_status'] = 'Trained'
        elif resp[1] == TrainStatus.Out_Of_Range:
            obj['trained_status'] = 'Out of Range'
        else:
            obj['trained_status'] = 'Unknown'

        if resp[2] == BaudRate.B9600:
            obj['baudrate'] = '9600'
        elif resp[2] == BaudRate.B4800:
            obj['baudrate'] = '4800'
        elif resp[2] == BaudRate.B2400:
            obj['baudrate'] = '2400'
        elif resp[2] == BaudRate.B19200:
            obj['baudrate'] = '19200'
        elif resp[2] == BaudRate.B38400:
            obj['baudrate'] = '38400'
        else:
            obj['baudrate'] = 'Unknown'

        if resp[3] == IOMode.Pulse:
            obj['output_io_mode'] = 'Pulse'
        elif resp[3] == IOMode.Toggle:
            obj['output_io_mode'] = 'Toggle'
        elif resp[3] == IOMode.Clear:
            obj['output_io_mode'] = 'Clear/Low'
        elif resp[3] == IOMode.Set:
            obj['output_io_mode'] = 'Set/High'
        else:
            obj['output_io_mode'] = 'Unknown'

        if resp[4] == PulseWidth.P10MS:
            obj['pulse_width'] = '10ms'
        elif resp[4] == PulseWidth.P15MS:
            obj['pulse_width'] = '15ms'
        elif resp[4] == PulseWidth.P20MS:
            obj['pulse_width'] = '20ms'
        elif resp[4] == PulseWidth.P25MS:
            obj['pulse_width'] = '25ms'
        elif resp[4] == PulseWidth.P30MS:
            obj['pulse_width'] = '30ms'
        elif resp[4] == PulseWidth.P35MS:
            obj['pulse_width'] = '35ms'
        elif resp[4] == PulseWidth.P40MS:
            obj['pulse_width'] = '40ms'
        elif resp[4] == PulseWidth.P45MS:
            obj['pulse_width'] = '45ms'
        elif resp[4] == PulseWidth.P50MS:
            obj['pulse_width'] = '50ms'
        elif resp[4] == PulseWidth.P75MS:
            obj['pulse_width'] = '75ms'
        elif resp[4] == PulseWidth.P100MS:
            obj['pulse_width'] = '100ms'
        elif resp[4] == PulseWidth.P200MS:
            obj['pulse_width'] = '200ms'
        elif resp[4] == PulseWidth.P300MS:
            obj['pulse_width'] = '300ms'
        elif resp[4] == PulseWidth.P400MS:
            obj['pulse_width'] = '400ms'
        elif resp[4] == PulseWidth.P500MS:
            obj['pulse_width'] = '500ms'
        elif resp[4] == PulseWidth.P1S:
            obj['pulse_width'] = '1s'
        else:
            obj['pulse_width'] = 'Unknown'

        if resp[5] == AutoLoad.Disable:
            obj['auto_load'] = 'Disable'
        elif resp[5] == AutoLoad.Enable:
            obj['auto_load'] = 'Enable'
        else:
            obj['auto_load'] = 'Unknown'

        if resp[6] == GroupControl.Disable:
            obj['group_control'] = 'Disable'
        elif resp[6] == GroupControl.System_Group:
            obj['group_control'] = 'System Group'
        elif resp[6] == GroupControl.User_Group:
            obj['group_control'] = 'User Group'
        else:
            obj['group_control'] = 'Unknown'

        return obj

    def check_recognizer(self):
        frame = self.__create_frame([Command.Check_Recognizer])

        self.__serial.write(frame)

        resp = self.__read_frame()

        if not resp:
            return {'status' : 'No response'}

        if resp[0] != Command.Check_Recognizer:
            return {'status' : 'Command Response mismatch'}

        obj = {}

        obj['rvn'] = int(resp[1])
        obj['rtn'] = int(resp[9])

        return obj

    def check_record_train_status(self,rec):

        if not isinstance(rec,list):
            return {'status' : 'rec not list'}

        frame = self.__create_frame([Command.Check_Record_Train_Status] + rec)

        self.__serial.write(frame)

        resp = self.__read_frame()

        if not resp:
            return {'status' : 'No response'}

        if resp[0] != Command.Check_Record_Train_Status:
            return {'status' : 'Command Response mismatch'}

        obj = {}

        num = int(resp[1])
        obj['number_record'] = num

        for rn in range(0,num):

            i = (rn + 1) * 2

            obj['record_' + format(rn, 'X').zfill(2)] = int(resp[i])

            if resp[i + 1] == TrainStatus.Untrained:
                obj['status_' + format(rn, 'X').zfill(2)] = 'Untrained'
            elif resp[i + 1] == TrainStatus.Trained:
                obj['status_' + format(rn, 'X').zfill(2)] = 'Trained'
            elif resp[i + 1] == TrainStatus.Out_Of_Range:
                obj['status_' + format(rn, 'X').zfill(2)] = 'Out of range'
            else:
                obj['status_' + format(rn, 'X').zfill(2)] = 'Unknown'

        return obj

    def check_signature_one_record(self,rec):
        frame = self.__create_frame([Command.Check_Signature_One_record,rec])

        self.__serial.write(frame)

        resp = self.__read_frame()

        if not resp:
            return {'status' : 'No response'}

        if resp[0] != Command.Check_Signature_One_record:
            return {'status' : 'Command Response mismatch'}

        obj = {}

        obj['signature_len'] = int(resp[1])
        obj['signature'] = resp[2:]

        return obj

    def restore_system_setting(self):
        frame = self.__create_frame([Command.Restore_System])

        self.__serial.write(frame)

        resp = self.__read_frame()

        if not resp:
            return {'status' : 'No response'}

        if resp[0] != Command.Restore_System:
            return {'status' : 'Command Response mismatch'}

        obj = {}
        if resp[1] == 0:
            obj['status'] = 'Ok'
        else:
            obj['status'] = hex(resp[1])

        return obj

    def set_baudrate(self,baud):
        frame = self.__create_frame([Command.Set_Baudrate,baud])

        self.__serial.write(frame)

        resp = self.__read_frame()

        if not resp:
            return {'status' : 'No response'}

        if resp[0] != Command.Set_Baudrate:
            return {'status' : 'Command Response mismatch'}

        obj = {}
        if resp[1] == 0:
            obj['status'] = 'Ok'
        else:
            obj['status'] = hex(resp[1])

        return obj

    def set_output_io_mode(self,mode):
        frame = self.__create_frame([Command.Set_IO_Mode,mode])

        self.__serial.write(frame)

        resp = self.__read_frame()

        if not resp:
            return {'status' : 'No response'}

        if resp[0] != Command.Set_IO_Mode:
            return {'status' : 'Command Response mismatch'}

        obj = {}
        if resp[1] == 0:
            obj['status'] = 'Ok'
        else:
            obj['status'] = hex(resp[1])

        return obj

    def set_output_io_pulse_width(self,width):
        frame = self.__create_frame([Command.Set_IO_Pulse_Width,width])

        self.__serial.write(frame)

        resp = self.__read_frame()

        if not resp:
            return {'status' : 'No response'}

        if resp[0] != Command.Set_IO_Pulse_Width:
            return {'status' : 'Command Response mismatch'}

        obj = {}
        if resp[1] == 0:
            obj['status'] = 'Ok'
        else:
            obj['status'] = hex(resp[1])

        return obj

    def reset_output(self,pin):

        if not isinstance(pin,list):
            return {'status' : 'Parameter harus list'}

        frame = self.__create_frame([Command.Reset_Output_IO] + pin)

        self.__serial.write(frame)

        resp = self.__read_frame()

        if not resp:
            return {'status' : 'No response'}

        if resp[0] != Command.Reset_Output_IO:
            return {'status' : 'Command Response mismatch'}

        obj = {}
        if resp[1] == 0:
            obj['status'] = 'Ok'
        else:
            obj['status'] = hex(resp[1])

        return obj

    def set_auto_load(self,rec):

        if not isinstance(rec,list):
            return {'status' : 'Parameter harus list'}

        map = 0

        for i in range(0,len(rec)):
            map |= (1 << i)

        frame = self.__create_frame([Command.Set_Power_On_Auto_Load,map] + rec)

        self.__serial.write(frame)

        resp = self.__read_frame()

        if not resp:
            return {'status' : 'No response'}

        if resp[0] != Command.Set_Power_On_Auto_Load:
            return {'status' : 'Command Response mismatch'}

        obj = {}
        if resp[1] == 0:
            obj['status'] = 'Ok'
        else:
            obj['status'] = hex(resp[1])

        return obj

    def disable_auto_load(self):
        return self.set_auto_load([])

    def train(self,rec):

        if not isinstance(rec,list):
            return {'status' : 'Parameter harus list'}

        if len(rec) == 0:
            return {'status' : 'Isilah minilah satu record'}

        
        frame = self.__create_frame([Command.Train] + rec)

        self.__serial.write(frame)

        obj = {}

        while True:
            resp = self.__read_frame()

            if not resp:
                obj['status'] = 'No response'
                break

            #print(resp)

            if resp[0] == 0x0A:
                if 0xaa in resp:
                    idx = resp.index(0xaa)
                    txt = ''.join([chr(c) for c in resp[2: (idx - 1)]])
                    print(txt)

                    sresp = resp[idx + 2:]

                    if sresp[0] == Command.Train:
                        for rn in range(0,sresp[1]):
                            i = (rn + 1) * 2
                            record = 'Record_{}'.format(sresp[i])
                            sts = sresp[i + 1]

                            if sts == 0:
                                obj[record] = 'Success'
                            elif sts == 1:
                                obj[record] = 'Timeout'
                            elif sts == 2:
                                obj[record] = 'Out Range'
                            else:
                                obj[record] = 'Unknown'
                        obj['status'] = 'Ok'

                    break

                else:
                    txt = ''.join([chr(c) for c in resp[2:]])
                    print(txt)
            elif resp[0] == Command.Train:

                for rn in range(0,resp[1]):
                    i = (rn + 1) * 2
                    record = 'Record_{}',format(resp[i])
                    sts = resp[i + 1]

                    if sts == 0:
                        obj[record] = 'Success'
                    elif sts == 1:
                        obj[record] = 'Timeout'
                    elif sts == 2:
                        obj[record] = 'Out Range'
                    else:
                        obj[record] = 'Unknown'

                obj['status'] = 'Ok'
                break
            else:
                break

        return obj
        
    def train_with_signature(self,rec,sig):

        frame = self.__create_frame([Command.Train_With_Signature,rec] + [ord(c) for c in sig])

        self.__serial.write(frame)

        obj = {}

        while True:
            resp = self.__read_frame()

            if not resp:
                obj['status'] = 'No response'
                break

            #print(resp)

            if resp[0] == 0x0A:
                if 0xaa in resp:
                    idx = resp.index(0xaa)
                    txt = ''.join([chr(c) for c in resp[2: (idx - 1)]])
                    print(txt)

                    sresp = resp[idx + 2:]

                    if sresp[0] == Command.Train:
                        i =  2
                        record = 'Record_{}'.format(sresp[i])
                        sts = sresp[i + 1]

                        if sts == 0:
                            obj[record] = 'Success'
                        elif sts == 1:
                            obj[record] = 'Timeout'
                        elif sts == 2:
                            obj[record] = 'Out Range'
                        else:
                            obj[record] = 'Unknown'
                        obj['status'] = 'Ok'

                    break

                else:
                    txt = ''.join([chr(c) for c in resp[2:]])
                    print(txt)
            elif resp[0] == Command.Train:
                i = 2
                record = 'Record_{}',format(resp[i])
                sts = resp[i + 1]

                if sts == 0:
                    obj[record] = 'Success'
                elif sts == 1:
                    obj[record] = 'Timeout'
                elif sts == 2:
                    obj[record] = 'Out Range'
                else:
                    obj[record] = 'Unknown'

                obj['status'] = 'Ok'
                break
            else:
                break

        return obj

    def set_signature(self,rec,sig):

        frame = self.__create_frame([Command.Set_Signature,rec] + [ord(c) for c in sig])

        self.__serial.write(frame)

        resp = self.__read_frame()

        if not resp:
            return {'status' : 'No response'}

        if resp[0] != Command.Set_Signature:
            return {'status' : 'Command Response mismatch'}

        obj = {}
        if resp[1] == 0:
            obj['status'] = 'Ok'
        else:
            obj['status'] = hex(resp[1])

        return obj

    def delete_signature(self,rec):
        return self.set_signature(rec,'')

    def load_voice_record(self,rec):

        if not isinstance(rec,list):
            return {'status' : 'Data is not list'}

        if len(rec) == 0:
            return {'status' : 'Minimum choose 1 record'}

        frame = self.__create_frame([Command.Load] + rec)

        self.__serial.write(frame)

        resp = self.__read_frame()

        if not resp:
            return {'status' : 'No response'}

        if resp[0] != Command.Load:
            return {'status' : 'Command Response mismatch'}

        num = resp[1]

        obj = {}

        for rn in range(0,num):

            i = (rn + 1) * 2

            record = 'Record_{}'.format(resp[i])

            if resp[ i + 1] == 0:
                obj[record] = 'Success'
            elif resp[ i + 1] == 0xff:
                obj[record] = 'Record value out of range'
            elif resp[ i + 1] == 0xfe:
                obj[record] = 'Record untrained'
            elif resp[ i + 1] == 0xfd:
                obj[record] = 'Recognizer full'
            elif resp[ i + 1] == 0xff:
                obj[record] = 'Record already in recognizer'
            else:
                obj[record] = 'Unknown'

        obj['status'] = 'Ok'

        return obj

    def clear_recognizer(self):
        frame = self.__create_frame([Command.Clear_Recognizer])

        self.__serial.write(frame)

        resp = self.__read_frame()

        if not resp:
            return {'status' : 'No response'}

        if resp[0] != Command.Clear_Recognizer:
            return {'status' : 'Command Response mismatch'}

        obj = {}

        if resp[1] == 0:
            obj['status'] = 'Ok'
        else:
            obj['status'] = resp[1]

        return obj
