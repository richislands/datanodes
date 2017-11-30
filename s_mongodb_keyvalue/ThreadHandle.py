'''
Created on 2017-10-12
@author: hjq
'''

import time
import threading

class ThreadHandleClass(threading.Thread):
    
    def __init__(self , threadID, threadName, mongoDBHandle, configName, ip, prot):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadName = threadName
        self.mongoDBHandle = mongoDBHandle
        self.configName = configName
        self.ip = ip
        self.prot = prot
        
    def run(self):
        if self.threadID == 1:
            try:
                self.mongoDBHandle.start(self.configName)
            except Exception:
                pass
        if self.threadID == 2:
            import zmq
            import CallHandle as callHandle
            context = zmq.Context()
            socket = context.socket(zmq.REP)
            socket.bind("tcp://%s:%d" % (self.ip, self.prot))
            while True:
                msg = socket.recv_multipart()
                cmd = bytes.decode(msg[0])
                if cmd == 'bind_config':
                    pbConfig_type = bytes.decode(msg[1])
                    config = msg[2]
                    configName = bytes.decode(msg[3])
                    dd = callHandle.bind_config(self.mongoDBHandle, pbConfig_type, config, configName)
                elif cmd == 'bind_data':
                    begin_time = int(round(time.time() * 1000))
                    pbData_type = bytes.decode(msg[1])
                    dataList = msg[2]
                    dataName = bytes.decode(msg[3])
                    dd = callHandle.bind_data(self.mongoDBHandle, pbData_type, dataList, dataName)
                    end_time = int(round(time.time() * 1000))
                    print('bind_data use time: ', (end_time - begin_time))
                elif cmd == 'start_service':
                    configName = bytes.decode(msg[1])
                    dd = callHandle.start_service(self.mongoDBHandle, configName)
                elif cmd == 'set_data':
                    begin_time = int(round(time.time() * 1000))
                    pdData_type = bytes.decode(msg[1])
                    dataList = msg[2]
                    dataName = bytes.decode(msg[3])
                    dd = callHandle.set_data(self.mongoDBHandle, pdData_type, dataList, dataName)
                    end_time = int(round(time.time() * 1000))
                    print('set_data use time: ', (end_time - begin_time))
                elif cmd == 'stop_service':
                    configName = bytes.decode(msg[1])
                    dd = callHandle.stop_service(self.mongoDBHandle, configName)
                elif cmd == 'dispose_data':
                    configName = bytes.decode(msg[1])
                    dataName = bytes.decode(msg[2])
                    dd = callHandle.dispose_data(self.mongoDBHandle, configName, dataName)
                elif cmd == 'get_data':
                    begin_time = int(round(time.time() * 1000))
                    dataName = bytes.decode(msg[1])
                    dataDict = callHandle.get_data(self.mongoDBHandle, dataName)
                    type = self.mongoDBHandle.typeDict
                    try:
                        if type[dataName] == 'm_config':
                            if dataDict == False:
                                list = [zmq.Frame("m_config".encode('utf8')), b'']
                                socket.send_multipart(list)
                            else:
                                import pb_data_mongodb_pb2
                                data = pb_data_mongodb_pb2.m_config()
                                for u in dataDict:
                                    data.config_key = u
                                    data.config_value = dataDict[u]
                                sdata = data.SerializeToString()
                                list = [zmq.Frame("m_config".encode('utf8')), sdata]
                                socket.send_multipart(list)
                        if type[dataName] == 'pb_data_sensor_list':
                            if dataName == 'all_status':
                                #print('----------------------------haojiaqi==================',type(self.mongoDBHandle.allstatus),self.mongoDBHandle.allstatus)
                                list = [zmq.Frame("pb_data_sensor_list".encode('utf8')), self.mongoDBHandle.allstatus]
                                socket.send_multipart(list)
                            else:
                                if dataDict == False:
                                    list = [zmq.Frame("pb_data_sensor_list".encode('utf8')), b'']
                                    socket.send_multipart(list)
                                else:
                                    for u in dataDict:
                                        socket.send_multipart([zmq.Frame(u.encode('utf8')), dataDict[u]])
                        end_time = int(round(time.time() * 1000))
                        print('get_data use time: ', (end_time - begin_time))
                    except Exception:
                        list = [zmq.Frame("m_config".encode('utf8')), b'']
                        socket.send_multipart(list)
                if cmd != 'get_data':
                    socket.send_string(str(dd))

