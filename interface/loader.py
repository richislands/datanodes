#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import subprocess
import os
import threading
import sys
import data_service_interface as dsif

g_process = {}

def run_app(app_path):
    try:
        p = subprocess.Popen(app_path, shell=False)
        handle_poll = None
        n = 0
        while n < 3:
            handle_poll = p.poll()
            time.sleep(0.5)
            n += 1
        if handle_poll is None:
            return p
        else:
            return None
    except Exception as e:
        raise e

def run_service(env, service_name, exe_name, ip, index):
    path = os.path.join(env, 'bin', service_name, exe_name)
    if not os.path.exists(path):
        return -1

    cmd = 'python %s' % path if path.endswith('.py') else path
    run_path = '%s %s %s %s' % (cmd, ip, service_name, 1)

    print('正在启动数据节点[%s]-路径[%s]......' % (service_name, path))
    p = run_app(run_path)
    if p:
        print('数据节点[%s]启动成功.' % service_name)
        return 1
    else:
        print('数据节点[%s]启动失败.' % service_name)
        return -1

def stop_app(name):
    try:
        if g_process[name]:
            g_process[name].terminate()
        time.sleep(2)
    except Exception as e:
        raise e

def start_service(name, service_name, ip, port, config, config_type):
    print('数据节点[%s]正在 bind service ......' % service_name)
    ret = dsif.bindService(ip, port, service_name, name)

    if eval(str(ret)) == 1:
        print('数据节点[%s] bind service 成功.' % service_name)
        # bind config
        print('数据节点[%s]正在 bind config ......' % service_name)
        ret = dsif.bindConfig(name, config_type, config, 'bind_config')
        if eval(str(ret)) == 1:
            print('数据节点[%s] bind config 成功.' % service_name)
            print('数据节点[%s]正在 start ......' % service_name)
            ret = dsif.start(name, 'bind_config')
            if eval(str(ret)) == 1:
                print('数据节点[%s] start 成功.' % service_name)
                return 1
            else:
                print('数据节点[%s] start 失败(%s).' % (service_name,ret))
                return -1
        else:
            print('数据节点[%s] bind config 失败(%s).' % (service_name,ret))
            return -1
    else:
        print('数据节点[%s] bind service 失败(%s).' % (service_name,ret))
        return -1

def start_node(path, name, ip, port, node_name, config, config_type):
    global g_process
    '''
    启动数据节点，并start和bind config
    '''
    try:


        is_start = False
        print('正在启动[%s]......' % path)
        p = run_app(path)
        if p:
            print('启动[%s]成功.' % path)
            g_process[name] = p
            # bind service
            print('数据节点[%s]正在 bind service ......' % node_name)
            ret = dsif.bindService(ip, port, node_name, name)
            if eval(str(ret)) == 1:
                print('数据节点[%s] bind service 成功.' % node_name)
                # bind config
                print('数据节点[%s]正在 bind config ......' % node_name)
                ret = dsif.bindConfig(name, config_type, config, 'bind_config')
                print('bindconfig-----------type(ret):',type(ret))
                if eval(str(ret)) == 1:
                    print('数据节点[%s] bind config 成功.' % node_name)
                    print('数据节点[%s]正在 start ......' % node_name)
                    ret = dsif.start(name, 'bind_config')
                    if eval(str(ret)) == 1:
                        print('数据节点[%s] start 成功.' % node_name)
                        is_start = True
                    else:
                        print('数据节点[%s] start 失败(%s).' % (node_name,ret))
                else:
                    print('数据节点[%s] bind config 失败(%s).' % (node_name,ret))
            else:
                print('数据节点[%s] bind service 失败(%s).' % (node_name,ret))

            if not is_start:
                stop_app(name)
        else:
            print('启动[%s]失败.' % path)

        return is_start
    except Exception as e:
        print('启动[%s]失败,原因:%s.' % (path,repr(e)))

def write_data(name, node_name, data_name, data_type, list_data):
    print('正在向数据节点[%s]中写入数据......' % node_name)
    # bind data
    is_write_ok = False
    for data in list_data:
        bind_ret = dsif.bindData(name, data_type, data, data_name)
        if eval(str(bind_ret)) == 1:
            set_ret = dsif.setData(name, data_name, data_type, data)
            if eval(str(set_ret)) == 1:
                print('数据节点[%s]写入数据[%s]成功.' % (node_name, data_type))
                is_write_ok = True
            else:
                print('数据节点[%s]写入数据[%s]失败(%s).' % (node_name, data_type, set_ret))
        else:
            print('数据节点[%s]写入数据[%s]失败(%s).' % (node_name, data_type, bind_ret))

    return is_write_ok

def run_test():

    ip = '20.16.10.1'
    env = os.environ.get("richisland_home")
    is_write_data = True
    index = 1

    # ----------------------------------------------------------------------
    # 启动mongodb_keyvalue数据节点
    import pb_config_mongodb
    # env = os.environ.get("richisland_home")
    # if not env:
    #     print('环境变量richisland_home未配置.')
    #     return -1

    # file_path = ''
    # if not os.path.exists(file_path)
    #     print('文件[%s]不存在,请检查......' % file_path)
    #     return -1

    # # ruan_apps: [app_path, ip, service_name, index]
    # run_apps = []
    # with open(file_path, 'r') as run_file:
    #     for line in run_file:
    #         vals = ''.join(line_context).strip('\n').split(',')
    #         if vals and len(vals) == 4:
    #             app_path, ip, service_name, index = vals
    #             run_apps.append(vals)

    #             app_path = os.path.join(env, 'bin', app_path)
    #             run_app = ' '.join(app_path, ip, service_name, index)
    #             run_app = 'python %s' % run_app if run_app.endswith('.py') else run_app
    #             run_apps.append(run_app)

    # if len(run_apps) < 1:
    #     print('文件[%s]中数据格式无效(app_path, ip, service_name, index),请检查......' % file_path)
    #     return -1
    service_name = 's_mongodb_keyvalue'
    exe_name = 'start_service.py'

    # run mongodb数据服务
    ret = run_service(env, service_name, exe_name, ip, index)
    if ret == -1:
        return -1

    name = 's_mongodb_keyvalue_1'
    port = 41010
    config_type = 'pb_config_mongodb'
    config = pb_config_mongodb.pb_config_mongodb()
    config.mongodb_id = '1'
    config.ip = '127.0.0.1'
    config.port = 27017
    config.user_name = 'root'
    config.user_password = 'root'
    config.cycle = 5
    config.database_name = 'Configs'

    # start mongodb数据服务
    ret = start_service(name, service_name, ip, port, config, config_type)
    if ret == -1:
        return -1

    # 向mongodb写入数据(初始化配置信息)
    if ret and is_write_data:
        # set opcda_server_config
        import opcconfig_tool
        import pb_config_opcda_server
        import pb_data_mongodb

        configs = []
        file_server = 'c:/opc_server_config.xlsx'
        opcda_server_config = opcconfig_tool.get_opcda_server_config(file_server)
        if opcda_server_config and opcda_server_config != -1:
            data_value = opcda_server_config.SerializeToString()
            bindData = pb_data_mongodb.m_config()
            bindData.config_key = 'pb_config_opcda_server'
            bindData.config_value = data_value
            configs.append(bindData)

        file_client = 'c:/opc_tags.xlsx'
        opcda_client_config = opcconfig_tool.get_opcda_config(file_client)
        if opcda_client_config and opcda_client_config != -1:
            data_value = opcda_client_config.SerializeToString()
            bindData = pb_data_mongodb.m_config()
            bindData.config_key = 'pb_config_opcda_client'
            bindData.config_value = data_value
            configs.append(bindData)

        is_set_ok = write_data(name, service_name, 'set_opc_config', 'm_config', configs)

        if not is_set_ok:
            return -1

    # ----------------------------------------------------------------------
    # 启动s_rtds数据服务
    if ret:
        time.sleep(1)

        service_name = 's_rtds'
        exe_name = 's_rtds.exe'

        # run rtds数据服务
        ret = run_service(env, service_name, exe_name, ip, index)
        if ret == -1:
            return -1

        name = 'rtds_1'
        port = 41009
        config_type = 'pb_config_rtds'
        import pb_config_rtds
        config = pb_config_rtds.pb_config_rtds()
        config.rtds_id = 1
        config.update_cycle = 5
        for id in range(10001, 40001):
            data = config.tag_infors.add()
            data.name = str(id)
        # start rtds数据服务
        ret = start_service(name, service_name, ip, port, config, config_type)
        if ret == -1:
            return -1

    # 启动opc server数据服务
    if ret:
        time.sleep(1)

        service_name = 'd_opcda_server'
        exe_name = 'd_opcda_server.exe'
        # run opc server数据服务
        ret = run_service(env, service_name, exe_name, ip, index)
        if ret == -1:
            return -1

    # 启动opc server应用程序
    if ret:
        time.sleep(1)

        service_name = 'a_opcda_server'
        exe_name = 'a_opcda_server.py'
        # run opc server应用程序
        ret = run_service(env, service_name, exe_name, ip, index)
        if ret == -1:
            return -1

    # # 启动opc client数据服务
    # if ret:
    #     time.sleep(1)

    #     service_name = 'd_opcda_client'
    #     exe_name = 'd_opcda_client.exe'
    #     # run opc client数据服务
    #     ret = run_service(env, service_name, exe_name, ip, index)
    #     if ret == -1:
    #         return -1

    # # 启动opc client应用程序
    # if ret:
    #     time.sleep(1)

    #     service_name = 'a_opcda_client'
    #     exe_name = 'a_opcda_client.exe'
    #     # run opc client应用程序
    #     ret = run_service(env, service_name, exe_name, ip, index)
    #     if ret == -1:
    #         return -1

RUN_TASK_MANAGE = True
def do():
    ret = run_test()
    if ret == -1:
        if len(g_process) > 0:
            for key in g_process:
                stop_app(key)
        print('loader程序正常退出.')
        sys.exit()
    else:
        while RUN_TASK_MANAGE:
            time.sleep(1)

def run_over(signum, frame):
    global RUN_TASK_MANAGE
    
    RUN_TASK_MANAGE = False
    if len(g_process) > 0:
        for key in g_process:
            stop_app(key)
    sys.exit()

if __name__ == '__main__':
    import signal

    try:
        signal.signal(signal.SIGINT, run_over)

        thread_do = threading.Thread(target = do)
        thread_do.setName('do')
        thread_do.setDaemon(True)
        thread_do.start()

        while True:
            time.sleep(1)
    except Exception as e:
        raise e

