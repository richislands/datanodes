#encoding:utf8
'''
Created on 2017-10-18
@author: hjq
'''

from enum import Enum

class ExceptionCode(Enum):
    bind_config_code = "0x030a0101"
    bind_data_code = "0x030a0201"
    start_service_code = "0x030a0301"
    stop_service_code = "0x030a0401"
    get_data_code = "0x030a0501"
    set_data_code = "0x030a0601"
    dispose_data_code = "0x030a0701"

import pb_data_sensor_list_pb2
import pb_data_sensor_pb2
import time

#import pylogger
#log = pylogger.Logger('MongoDB 数据服务','D:\\richisland\\logs')
#pds = pb_data_sensor_pb2.pb_data_sensor()

def set_status(mongoDBHandle, value):
    pbdls = pb_data_sensor_list_pb2.pb_data_sensor_list()
    pds = pbdls.pb_data_sensors.add()
    pbdls.list_id = 1
    mongoDBHandle.all_status = value
    pds.name = 's_mongodb_keyvalue_status_1'
    pds.time = int(round(time.time() * 1000))
    pds.value = bytes(str(value), encoding="utf8")
    pds.status = pb_data_sensor_pb2.GOOD
    data = pbdls.SerializeToString()
    mongoDBHandle.dataTmp['pb_data_sensor_list'] = data

#--------------------------------------------------------------------

'''
绑定配置信息
'''

def bind_config(mongoDBHandle, pbConfig_type, config, configName):
    res = mongoDBHandle.initConfig(pbConfig_type, config, configName)
    if res == True:
        set_status(mongoDBHandle, 2)
        return 1
    else :
        #set_status(mongoDBHandle, 4)
        mongoDBHandle.log.info('绑定配置信息异常')
        return ExceptionCode.bind_config_code.value

'''
绑定获取数据信息
'''

def bind_data(mongoDBHandle, pbData_type, dataList, dataName):
    res = mongoDBHandle.initData(pbData_type, dataList, dataName)
    if res == True:
        return 1
    else :
        mongoDBHandle.log.info('绑定获取数据信息异常')
        return ExceptionCode.bind_data_code.value

'''
开始服务
'''

def start_service(mongoDBHandle, configName):
    #print('-------------------- ',configName,mongoDBHandle.configDict)
    if configName in mongoDBHandle.configDict:
        from ThreadHandle import ThreadHandleClass as threadHandle
        service = threadHandle(1, "Thread-1", mongoDBHandle, configName, '', 0)
        service.setDaemon(True)
        service.start()
        set_status(mongoDBHandle, 3)
        return 1
    else:
        #set_status(mongoDBHandle, 4)
        mongoDBHandle.log.info('启动服务失败，未绑定配置')
        return ExceptionCode.start_service_code.value

'''
停止服务
'''  

def stop_service(mongoDBHandle, configName):
    res = mongoDBHandle.stop(configName)
    if res == True:
        set_status(mongoDBHandle, 2)
        return 1
    else :
        #set_status(mongoDBHandle, 4)
        mongoDBHandle.log.info('停止服务异常')
        return ExceptionCode.stop_service_code.value

'''
获取数据
''' 

def get_data(mongoDBHandle, dataName):
    
    dataDict = mongoDBHandle.getData(dataName)
    if dataDict == False:
        mongoDBHandle.log.info('绑定错误，或者数据库链接异常')
        #mongoDBHandle.log.info(ExceptionCode.get_data_code.value)
        return False
    else :
        return dataDict

'''
设置数据
'''

def set_data(mongoDBHandle, pdData_type, dataList, dataName):
    res = mongoDBHandle.setData(pdData_type, dataList, dataName)
    if res == True:
        return 1
    else :
        mongoDBHandle.log.info('数据库链接异常')
        #mongoDBHandle.log.info(ExceptionCode.set_data_code.value)
        return ExceptionCode.set_data_code.value

'''
清空数据
'''

def dispose_data(mongoDBHandle, configName, dataName):
    res = mongoDBHandle.dispose(configName, dataName)
    if res == True:
        set_status(mongoDBHandle, 1)
        mongoDBHandle.log.debug('清空数据成功')
        return 1
    else :
        set_status(mongoDBHandle, 1)
        mongoDBHandle.log.info('清空数据异常')
        return ExceptionCode.dispose_data_code.value


