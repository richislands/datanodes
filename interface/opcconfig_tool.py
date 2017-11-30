#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xlrd  
import sys
sys.path.append('E:/python_workspace/test/interface')
import pb_config_opcda_client
import pb_config_opcda_server
import pb_config_tag

def get_opcda_server_config(opc_server_config_file):
    wb = xlrd.open_workbook(opc_server_config_file)

    opcda_server_id = 1
    #获取workbook中server_config数据
    server_config = list(map(lambda x: [x.row_values(i) for i in range(1, x.nrows)], [wb.sheet_by_name(u'server_config')]))
    opcda_server = pb_config_opcda_server.pb_config_opcda_server()
    opcda_server.opcda_server_id = opcda_server_id
    opcda_server.release_cycle = int(server_config[0][0][0])
    opcda_server.time_mode = int(server_config[0][0][1])

    #获取workbook中tags_config数据
    tags_config = list(map(lambda x: [x.row_values(i) for i in range(1, x.nrows)], [wb.sheet_by_name(u'tags_config')]))
    if len(tags_config[0]) > 0:
        for tag_config in tags_config[0]:
            if __set_opcda_tag(opc_server=opcda_server, tag_config=tag_config) == -1:
                print('set_opcda_tag failed.')
        return opcda_server
    else:
        return -1

opcda_id = 0
def get_opcda_config(opc_config_file):
    global opcda_id
    wb = xlrd.open_workbook(opc_config_file)
    
    opc_servers = list(map(lambda x: [x.row_values(i) for i in range(1, x.nrows)], [wb.sheet_by_name(u'opc_server')]))
    opcda_id += 1
    opcda = pb_config_opcda_client.pb_config_opcda_client()
    opcda.opcda_client_id = opcda_id
    opcda.main_opc_server.opc_server_ip = str(opc_servers[0][0][0])
    opcda.main_opc_server.opc_server_prgid = str(opc_servers[0][0][1])
    opcda.main_opc_server.opc_server_clsid = str(opc_servers[0][0][2])
    opcda.main_opc_server.opc_server_domain = str(opc_servers[0][0][3])
    opcda.main_opc_server.opc_server_user = str(opc_servers[0][0][4])
    opcda.main_opc_server.opc_server_password = str(opc_servers[0][0][5])

    if len(opc_servers[0]) > 1:
        opcda.back_opc_server.opc_server_ip = str(opc_servers[0][1][0])
        opcda.back_opc_server.opc_server_prgid = str(opc_servers[0][1][1])
        opcda.back_opc_server.opc_server_clsid = str(opc_servers[0][1][2])
        opcda.back_opc_server.opc_server_domain = str(opc_servers[0][1][3])
        opcda.back_opc_server.opc_server_user = str(opc_servers[0][1][4])
        opcda.back_opc_server.opc_server_password = str(opc_servers[0][1][5])

    #获取workbook中所有的表格 
    sheets = wb.sheets()
    # group_sheets = filter(lambda x: x.name.find('-')>-1, sheets)
    group_tags = list(map(lambda x: {x.name : [x.row_values(i) for i in range(1, x.nrows)]} if x.name.find('-') > -1 else None, sheets))
    if group_tags is not None:
        for gt in group_tags:
            if isinstance(gt, dict):
                for grp_key in gt:
                    __set_opcda_group(opcda, grp_key.split('-')[0], grp_key.split('-')[1], gt[grp_key])

        return opcda
    else:
        return -1

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
            if __set_opcda_tag(opc_group=group, tag_config=tag_config) == -1:
                print('set_opcda_tag failed.')
    else:
        return -1

tag_id = 10000
def __set_opcda_tag(opc_server=None, opc_group=None, tag_config=None):
    global tag_id
    if tag_config is not None and len(tag_config) > 2:
        tag_id += 1
        if opc_group:
            tag = opc_group.opc_tags.add()
        else:
            tag = opc_server.config_tag_release.add()
        tag.tag_id = tag_id
        tag.tag_name = tag_config[0].strip()
        tag.save_tag_name = str(tag_id)
        tag.publish_tag_name = tag_config[2].strip()
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
        tag.correct_coefficient = 0.0
        tag.adiust_parameters = 0.0
        tag.data_unit = pb_config_tag.WET_KG
        return 1
    else:
        return -1

if __name__ == '__main__':
    # opc_config_file = 'c:\\opc_tags.xlsx'
    # opcdaconfig = get_opcda_config(opc_config_file)

    # print(opcdaconfig.opc_groups[0].opc_tags)
    
    opc_config_file = 'c:\\opc_server_config.xlsx'
    opcda_server_config = get_opcda_server_config(opc_config_file)
    print(opcda_server_config)