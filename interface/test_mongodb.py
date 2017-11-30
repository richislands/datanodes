import time
import data_service_interface as dsif

number = 30
ip = '192.168.28.23'
port = 41010
ret = dsif.bindService(ip, port, 's_mongodb_keyvalue', 's_mongodb_service')

print('bindService return:',ret)
print('%s bindService over %s' % ('-'*number, '-'*number))

#------------------------------------------------------------
import pb_config_mongodb
config = pb_config_mongodb.pb_config_mongodb()
config.mongodb_id = '001'
config.ip = '192.168.28.23'
config.port = 27017
config.user_name = 'root'
config.user_password = 'root'
config.cycle = 5
config.database_name = 'Configs'
config.collection_name = 'config'
config.field_name = 'config_key'
# config.search_key_list.append('config_opc_01')

ret = dsif.bindConfig('s_mongodb_service', 'pb_config_mongodb', config, 'config_name_01')
print('bindConfig return:', ret)
print('%s bindConfig over %s' % ('-'*number, '-'*number))

#------------------------------------------------------------
ret = dsif.start('s_mongodb_service', 'config_name_01')
print('start return:', ret)
print('%s start over %s' % ('-'*number, '-'*number))

#------------------------------------------------------------
import pb_data_mongodb
bindData = pb_data_mongodb.m_config()
bindData.config_key = 'config_opc_01'
bindData.config_value = b''
ret = dsif.bindData('s_mongodb_service', 'm_config', bindData, 'get_config_opc_01')
print('bindData return:', ret)
print('%s bindData over %s' % ('-'*number, '-'*number))

#------------------------------------------------------------
import pb_config_opcda_client
import pb_config_tag
import opcconfig_tool

opc_config_file = 'c:\\opc_tags.xlsx'
opcda = opcconfig_tool.get_opcda_config(opc_config_file)

data_value = opcda.SerializeToString()
data = pb_data_mongodb.m_config()
data.config_key = 'config_opc_01' 
data.config_value = data_value

ret = dsif.setData('s_mongodb_service', 'get_config_opc_01', 'm_config', data)
print('setData return:', ret)
print('%s setData over %s' % ('-'*number, '-'*number))

# 
# opcda = pb_config_opcda_client.pb_config_opcda_client()
# opcda.opcda_client_id = 123

# opcda.main_opc_server.opc_server_ip = '1'
# opcda.main_opc_server.opc_server_prgid = 'abcdefg'
# opcda.main_opc_server.opc_server_clsid = 'gfedcba'
# opcda.main_opc_server.opc_server_domain = 'aaaaaa'
# opcda.main_opc_server.opc_server_user = 'bbbb'
# opcda.main_opc_server.opc_server_password = 'cccc'

# group1 = opcda.opc_groups.add()
# group1.group_id = 11
# group1.group_name = '22'
# group1.collect_cycle = 33
# tag1 = group1.opc_tags.add()
# tag1.tag_id = 111
# tag1.tag_name = 'tag1'
# tag1.save_tag_name = 'tag1_1'
# tag1.publish_tag_name = 'tag1_2'
# tag1.data_type = pb_config_tag.ENUM_DOUBLE
# tag1.data_format = 1234
# tag1.string_data_encoding = pb_config_tag.UTF8
# tag1.correct_coefficient = 1
# tag1.adiust_parameters = 0
# tag1.data_unit = pb_config_tag.WET_KG
# tag2 = group1.opc_tags.add()
# tag2.tag_id = 222
# tag2.tag_name = 'tag2'
# tag2.save_tag_name = 'tag2_1'
# tag2.publish_tag_name = 'tag2_2'
# tag2.data_type = pb_config_tag.ENUM_BOOL
# tag2.data_format = 4321
# tag2.string_data_encoding = pb_config_tag.UTF8
# tag2.correct_coefficient = 2
# tag2.adiust_parameters = 1
# tag2.data_unit = pb_config_tag.WET_TON

# group2 = opcda.opc_groups.add()
# group2.group_id = 11
# group2.group_name = '22'
# group2.collect_cycle = 33
# tag3 = group2.opc_tags.add()
# tag3.tag_id = 333
# tag3.tag_name = 'tag3'
# tag3.save_tag_name = 'tag3_1'
# tag3.publish_tag_name = 'tag3_2'
# tag3.data_type = pb_config_tag.ENUM_DOUBLE
# tag3.data_format = 12345678
# tag3.string_data_encoding = pb_config_tag.UTF8
# tag3.correct_coefficient = 3
# tag3.adiust_parameters = 2
# tag3.data_unit = pb_config_tag.LEN_M

# data_value = opcda.SerializeToString()
# data = pb_data_mongodb.m_config()
# data.config_key = 'config_opc_01' 
# data.config_value = data_value

# ret = dsif.setData('s_mongodb_service', 'get_config_opc_01', 'm_config', data)
# print('setData return:', ret)

#------------------------------------------------------------
import pb_data_sensor_list
getData = pb_data_mongodb.m_config()
ret = dsif.getData('s_mongodb_service', 'get_config_opc_01', 'm_config', getData)
print('getdata',getData)
opcda_obj = pb_config_opcda_client.pb_config_opcda_client()
opcda_obj.ParseFromString(getData.config_value)
print('getData return: %s, data: %s' % (ret, opcda_obj))
print('%s getdata over %s' % ('-'*number, '-'*number))

# ------------------------------------------------------------
ret = dsif.stop('s_mongodb_service', 's_mongodb_service')
print('stop return:', ret)
print('%s stop over %s' % ('-'*number, '-'*number))

#------------------------------------------------------------
ret = dsif.dispose('s_mongodb_service', 's_mongodb_service', 'get_config_opc_01')
print('dispose return:', ret)
print('%s dispose over %s' % ('-'*number, '-'*number))

