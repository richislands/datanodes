__version__ = '0.1.1'

import data_service_interface as dsif
import pb_data_sensor_list
import pb_config_tag
import time

ip = '192.168.28.42'
port = 41009
number = 30

ret = dsif.bindService(ip, port, 's_rtds', 'rtds')
print('bindService return:',ret)
print('%s bindService over %s' % ('-'*number, '-'*number))

#-------------------------------------------------------------
import pb_config_rtds
config = pb_config_rtds.pb_config_rtds()
config.rtds_id = 1
config.update_cycle = 5
data1 = config.tag_infors.add()
data1.name = '10001'
data2 = config.tag_infors.add()
data2.name = '10002'
data3 = config.tag_infors.add()
data3.name = 'tag3'

ret = dsif.bindConfig('rtds', 'pb_config_rtds', config, 'rtds_01')
print('bindConfig return:', ret)
print('%s bindConfig over %s' % ('-'*number, '-'*number))

#------------------------------------------------------------
ret = dsif.start('rtds', 'rtds_01')
print('start return:', ret)
print('%s start over %s' % ('-'*number, '-'*number))
time.sleep(3)

#------------------------------------------------------------
ret = dsif.stop('rtds', 'rtds_01')
print('stop return:', ret)
print('%s stop over %s' % ('-'*number, '-'*number))

#------------------------------------------------------------
ret = dsif.start('rtds', 'rtds_01')
print('start return:', ret)
print('%s start over %s' % ('-'*number, '-'*number))

#------------------------------------------------------------
bindData = pb_data_sensor_list.pb_data_sensor_list()
bindData.list_id = 1
sensor1 = bindData.pb_data_sensors.add()
sensor1.name = '10001'
sensor2 = bindData.pb_data_sensors.add()
sensor2.name = '10002'
# sensor3 = bindData.pb_data_sensors.add()
# sensor3.name = 'run_status_rtds_01'

ret = dsif.bindData('rtds', 'pb_data_sensor_list', bindData, 'get_sensor_01')
print('bindData return:', ret)
print('%s bindData over %s' % ('-'*number, '-'*number))

#------------------------------------------------------------
setData = pb_data_sensor_list.pb_data_sensor_list()

setData.list_id = 1
set_sensor1 = setData.pb_data_sensors.add()
set_sensor1.name = '10001'
set_sensor1.type = pb_config_tag.ENUM_INT32
set_sensor1.size = 4
set_sensor1.value = b'100'
set_sensor1.time = int(time.time())
set_sensor2 = setData.pb_data_sensors.add()
set_sensor2.name = '10002'
set_sensor2.type = pb_config_tag.ENUM_INT32
set_sensor2.size = 4
set_sensor2.value = b'200'
set_sensor2.time = int(time.time())
ret = dsif.setData('rtds', 'get_sensor_01', 'pb_data_sensor_list', setData)
print('setData return:', ret)
print('%s setData over %s' % ('-'*number, '-'*number))

#------------------------------------------------------------
time.sleep(3)
getData = pb_data_sensor_list.pb_data_sensor_list()
ret = dsif.getData('rtds', 'get_sensor_01', 'pb_data_sensor_list', getData)
print('getData return: %s, data: %s' % (ret, getData))
print('%s getData over %s' % ('-'*number, '-'*number))

#------------------------------------------------------------
ret = dsif.stop('rtds', 'rtds_01')
print('stop return:', ret)
print('%s stop over %s' % ('-'*number, '-'*number))

#------------------------------------------------------------
ret = dsif.dispose('rtds', 'rtds_01', 'get_sensor_01')
print('dispose return:', ret)
print('%s dispose over %s' % ('-'*number, '-'*number))
