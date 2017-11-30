# -*- coding: UTF-8 -*-
'''
Created on 2017-10-17
@author: hjq
'''

import time
import AnalysisUtil
import pylogger
from pymongo import MongoClient
import pb_data_sensor_list_pb2
import pb_data_sensor_pb2

class MongoDBHandleClass(object):
    
    dataTmp = {}
    dataDict = {}
    typeDict = {}
    configDict = {}
    search_key_list = []
    allstatus =b''
    
    def __init__(self):
        self.log = pylogger.Logger('MongoDB 数据服务', 'D:\\richisland\\log')
        self.run_status = 0
        self.log.info('初始化服务')
        self.set_status(1)
        self.typeDict['all_status'] = 'pb_data_sensor_list'
        #self.dataDict['all_status'] = {'pb_data_sensor_list':b''}
        
    def initConfig(self, pbConfig_type, config, configName):
        self.log.debug('开始初始化数据服务配置')
        cfgDict = AnalysisUtil.analysisConfig(pbConfig_type, config)
        if cfgDict == False:
            return False
        else:
            self.configDict[configName] = cfgDict
            for u in self.configDict:
                for tmp in self.configDict[u]:
                    if tmp == 'search_key_list':
                        for u in self.configDict[u][tmp]:
                            if u not in self.search_key_list:
                                self.search_key_list.append(u)
            self.set_status(2)
            #print('======================4================',self.dataTmp)
            self.log.debug('初始化数据服务配置完成')
            return True
    
    def initData(self, pbData_type, dataList, dataName):
        self.log.debug('开始初始化获取数据')
        self.typeDict[dataName] = pbData_type
        rel = AnalysisUtil.analysisData(pbData_type, dataList, self.dataDict, dataName)
        self.log.debug('初始化获取数据完成')
        return rel
           
    def start(self, configName):
        if self.run_status == 1:
            self.log.debug('服务已经启动')
            return False
        self.log.debug('启动服务')
        if configName in self.configDict:
            configInfo = self.configDict[configName]
            self.mc = MongoClient(configInfo['ip'], configInfo['port'])
            self.db = self.mc.Configs
            array_keyvalue = self.db.config.find()
            #print('-------123--------- ',array_keyvalue)
            for u in array_keyvalue:
                self.search_key_list.append(u['config_key'])
            num = 1
            while True:
                if self.run_status == 2:
                    print('----------disconnect the database-----------')
                    self.run_status = 0
                    break
                else:
                    self.run_status = 1
                    #begin_time = int(round(time.time() * 1000))
                    array = list(self.db.config.find())
                    for u in array:
                        if u["config_key"] in self.search_key_list:
                            self.dataTmp[u["config_key"]] = u["config_value"]
                    #end_time = int(round(time.time() * 1000))
                    #print('---------------------------', self.run_status, num, (end_time - begin_time))
                    self.log.debug('拷贝数据成功')
                    self.set_status(3)
                    time.sleep(configInfo['cycle'])
                    num += 1
        else :
            self.log.debug('启动服务失败')
            return False
        
    def stop(self, configName):
        self.log.debug('停止服务')
        #conn = self.mc.close()
        self.run_status = 2
        self.set_status(2)
        self.log.debug('停止服务成功')
        return True
    
    def getData(self, dataName):
        if "all_status" == dataName:
            self.log.debug('获取状态')
            return True
        else:
            self.log.debug('开始获取数据')
            if len(self.dataDict) > 0:
                try:
                    dict = {}
                    for u in self.dataDict[dataName]:
                        dict[u] = self.dataTmp[u]
                    self.dataDict[dataName] = dict
                    self.log.debug('获取数据结束')
                    return self.dataDict[dataName]
                except Exception:
                    self.log.debug('获取数据失败')
                    return False
            else:
                self.log.debug('获取数据失败')
                return False
                
    def setData(self, pdData_type, dataList, dataName):
        if self.run_status != 1:
            return False
        else:
            pass
        if len(self.dataDict) == 0:
            return False
        elif dataName not in self.dataDict:
            return False
        if dataList == b'':
            self.log.debug('开始删除数据')
            for u in self.dataDict[dataName]:
                if pdData_type == 'm_config':
                    self.db.config.remove({"config_key":u})
                self.search_key_list.remove(u)
                print('del del del ', u)
                del self.dataTmp[u]
            self.mc.close()
            self.log.debug('删除数据成功')
            return True
        else:
            list1 = list(self.dataDict[dataName].keys())
            if AnalysisUtil.analysisData(pdData_type, dataList, self.dataDict, dataName):
                list2 = list(self.dataDict[dataName].keys())
                ret_list = list((set(list1).union(set(list2))) ^ (set(list1) ^ set(list2)))
                if len(ret_list) < len(list2):
                    return False
                else:
                    m_config_list = []
                    for u in list2:
                        if u in self.search_key_list:
                            if pdData_type == 'm_config':
                                self.log.debug('开始修改数据')
                                self.db.config.update({"config_key":u}, {"$set":{"config_value":self.dataDict[dataName][u]}})
                                self.log.debug('修改数据完成')
                            self.dataTmp[u] = self.dataDict[dataName][u]
                        else:
                            if pdData_type == 'm_config':
                                m_config_list.append({"config_key":u, "config_value":self.dataDict[dataName][u]})
                            self.dataTmp[u] = self.dataDict[dataName][u]
                            self.search_key_list.append(u)
            if pdData_type == 'm_config':
                if len(m_config_list) > 0:
                    self.log.debug('开始新增数据')
                    self.db.config.insert(m_config_list)
                    self.log.debug('新增数据完成')
            self.mc.close()
            
            return True
            
    def dispose(self, configName, dataName):
        self.log.debug('清空数据')
        self.set_status(1)
        #return True
        #print('--------------- ',self.configDict)
        if configName in self.configDict:
            del self.configDict[configName]
        #print('--------------- ',self.dataDict)
        if dataName in self.dataDict:
            del self.dataDict[dataName]
        self.set_status(1)
        return True

    def set_status(self,value):
        pbdls = pb_data_sensor_list_pb2.pb_data_sensor_list()
        pds = pbdls.pb_data_sensors.add()
        pbdls.list_id = 1
        pds.name = 's_mongodb_keyvalue_status_1'
        pds.time = int(round(time.time()))
        pds.value = bytes(str(value), encoding="utf8")
        pds.status = pb_data_sensor_pb2.GOOD
        self.allstatus = pbdls.SerializeToString()
        #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>> ",self.allstatus)

