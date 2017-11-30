#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xlrd  
import sys
sys.path.append('E:/python_workspace/test/interface')
import pb_config_opcda_client
import pb_config_tag

opcda_id = 0
all_tag_list = []

def __set_opcda_server(opc_server, server_config):
    opc_server.opc_server_ip, opc_server.opc_server_prgid, opc_server.opc_server_clsid, opc_server.opc_server_domain, \
    opc_server.opc_server_user, opc_server.opc_server_password = map(str, server_config)

def get_opcda_config(opc_config_file):
    global opcda_id

    try:
        wb = xlrd.open_workbook(opc_config_file)
    except Exception as e:
        raise e
    
    if wb is None:
        return -1

    server_sheet = wb.sheet_by_name('opc_server')
    if server_sheet is None:
        return -1

    # opc_servers = list(map(lambda x: [__get_opcserver(x.row_values(i)) for i in range(1, x.nrows)], [wb.sheet_by_name(u'opc_server')]))
    server_configs = [server_sheet.row_values(i) for i in range(1, server_sheet.nrows)]
    if server_configs is None:
        return -1

    opcda_id += 1
    opcda = pb_config_opcda_client.pb_config_opcda_client()
    opcda.opcda_client_id = opcda_id
    __set_opcda_server(opcda.main_opc_server, server_configs[0])
    if len(server_configs) > 1:
        __set_opcda_server(opcda.back_opc_server, server_configs[1])

    # 获取workbook中所有的表格 
    sheets = wb.sheets()
    # group_sheets = filter(lambda x: x.name.find('-')>-1, sheets)
    group_tags = list(map(lambda x: {x.name : [x.row_values(i) for i in range(1, x.nrows)]} if x.name.find('-') > -1 else None, sheets))
    if group_tags is not None:
        for gt in group_tags:
            if isinstance(gt, dict):
                for grp_key in gt:
                    __set_opcda_group(opcda, grp_key.split('-')[0], grp_key.split('-')[1], gt[grp_key])
        return opcda

group_id = 0
def __set_opcda_group(opc_da, group_name, group_cycle, tag_config_list):
    global group_id
    group_id += 1
    group = opc_da.opc_groups.add()
    group.group_id = group_id
    group.group_name = group_name
    group.collect_cycle = int(group_cycle)

    if tag_config_list is not None:
        for tag_config in tag_config_list:
            if __set_opcda_tag(group, tag_config) == -1:
                print('set_opcda_tag failed.')
    else:
        return -1

tag_id = 0
def __set_opcda_tag(opc_group, tag_config):
    global tag_id
    if tag_config is not None and len(tag_config) > 2:
        tag_id += 1
        tag = opc_group.opc_tags.add()
        tag.tag_id = tag_id
        tag.tag_name = tag_config[0]
        tag.save_tag_name = str(tag_id)
        tag.publish_tag_name = tag_config[2]
        if tag_config[1] == '文本量':
            tag.data_type = pb_config_tag.ENUM_STRING
        elif tag_config[1] == '开关量':
            tag.data_type = pb_config_tag.ENUM_UINT32
        elif tag_config[1] == '模拟量':
            tag.data_type = pb_config_tag.ENUM_FLOAT
        else:
            tag.data_type = pb_config_tag.ENUM_STRING
            print('data type %s is unknow.' % tag_config[1])
        tag.data_format = 1234
        tag.string_data_encoding = pb_config_tag.UTF8
        tag.correct_coefficient = 1.0
        tag.adiust_parameters = 0.0

        all_tag_list.append(tag_config)

        return 1
    else:
        return -1

def get_not_read_tags(config_tags, read_tags):
    read_tag_name_list = [read_tag.name for read_tag in read_tags]
    count = 0
    for config_tag in config_tags:
        tag_name = config_tag[0].strip()
        if not (tag_name in read_tag_name_list):
            print('tag[%s] read failed.' % tag_name)
            count += 1
    print('read failed tags number is %s' % count)

if __name__ == '__main__':
    opc_config_file = 'c:\\opc_tags.xlsx'
    opcdaconfig = get_opcda_config(opc_config_file)
    # print(opcdaconfig)

    import pb_data_sensor
    tags = []
    tag1 = pb_data_sensor.pb_data_sensor()
    tag1.name = 'FIX.F_1000.F_CV'
    tag1.size = 5
    tags.append(tag1)
    tag2 = pb_data_sensor.pb_data_sensor()
    tag2.name = 'FIX.F_981.F_CV'
    tag2.size = 1
    tags.append(tag2)
    tag3 = pb_data_sensor.pb_data_sensor()
    tag3.name = 'FIX.F_110.F_CV'
    tag3.size = 50
    tags.append(tag3)
    tag4 = pb_data_sensor.pb_data_sensor()
    tag4.name = 'FIX.F_101.F_CV'
    tag4.size = 10
    tags.append(tag4)
    tag6 = pb_data_sensor.pb_data_sensor()
    tag6.name = 'FIX.S999.A_CV'
    tag6.size = 53
    tags.append(tag6)
    tag5 = pb_data_sensor.pb_data_sensor()
    tag5.name = 'FIX.B53.F_CV'
    tag5.size = 13
    tags.append(tag5)

    get_not_read_tags(all_tag_list, tags)
