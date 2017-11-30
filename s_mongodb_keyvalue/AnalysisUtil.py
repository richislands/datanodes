#encoding:utf8
'''
Created on 2017-10-18
@author: Administrator
'''

import pb_config_mongodb_pb2

'''
反序列化，protobuf对象。获取配置信息
'''

def analysisConfig(pbConfig_type, config):
    if pbConfig_type == 'pb_config_mongodb':
        target = pb_config_mongodb_pb2.pb_config_mongodb()
        try:
            target.ParseFromString(config)
            cfgDict = {}
            cfgDict['mongodb_id'] = target.mongodb_id
            cfgDict['ip'] = target.ip
            cfgDict['port'] = target.port
            cfgDict['user_name'] = target.user_name
            cfgDict['user_password'] = target.user_password
            cfgDict['cycle'] = target.cycle
            cfgDict['database_name'] = target.database_name
            cfgDict['collection_name'] = 123
            cfgDict['field_name'] = target.field_name
            cfgDict['search_key_list'] = target.search_key_list
            #print('======================0================',cfgDict)
            return cfgDict
        except BaseException:
            #print('======================1================')
            return False
    else :
        #print('======================2================')
        return False

'''
反序列化，protobuf对象。数据信息
'''

def analysisData(pbData_type, dataList, dataDict, dataName):
    if pbData_type == 'm_config':
        import pb_data_mongodb_pb2
        try:
            target = pb_data_mongodb_pb2.m_config()
            target.ParseFromString(dataList)
            dataDict[dataName] = {target.config_key:target.config_value}
            return True
        except BaseException:
            return False
    else:
        return False

