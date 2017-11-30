#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cuiwei'
__version__ = '0.1.0.0'

import time
import zmq
import pylogger
from enum import Enum

# 数据服务配置
service_config = {}
# 运行状态配置
status_config = {}

#--------------------------------------------------------------
# 超时时间(毫秒)
REQUEST_TIMEOUT = 10000
# 尝试重连次数
REQUEST_RETRIES = 3
# 数据服务运行状态枚举
SERVICE_STATUS = Enum('SERVICE_STATUS', ('NONE','CONFIG','RUN','ERROR'))
# 本期只允许绑定一路配置,名称定位config_name
CONFIG_NAME = 'config_name'
# 业务接口异常头(层+id)
EXCEPT_HEAD = '0x0201'
# 业务接口可调用函数枚举
FUNCTIONS = Enum('FUNCTIONS', ('BIND_SERVICE','BIND_CONFIG','START','BIND_DATA',\
    'GET_DATA', 'SET_DATA', 'STOP', 'DISPOSE'))
# 业务接口异常类型枚举
EXCEPTIONS = Enum('EXCEPTIONS', ('INPUT_PARAMS_ERROR','NET_COMM_ERROR','GET_STATUS_ERROR','NOT_BIND_CONFIG',\
    'HAVE_BIND_CONFIG', 'NOT_START', 'HAVE_START', 'APP_ERROR', 'RTN_ERROR', 'UNKNOW_ERROR', 'OUTPUT_PARAM_ERROR', \
    'DATA_NOT_EXIST', 'NOT_BIND_SERVICE'))
# 业务接口异常类型对应描述信息枚举
EXCEPTIONS_REMARK = {
    EXCEPTIONS.INPUT_PARAMS_ERROR:'输入参数异常',\
    EXCEPTIONS.NET_COMM_ERROR:'网络通信异常',\
    EXCEPTIONS.GET_STATUS_ERROR:'获取状态异常',\
    EXCEPTIONS.NOT_BIND_CONFIG:'节点未配置',\
    EXCEPTIONS.HAVE_BIND_CONFIG:'节点已配置',\
    EXCEPTIONS.NOT_START:'节点未运行',\
    EXCEPTIONS.HAVE_START:'节点正在运行',\
    EXCEPTIONS.APP_ERROR:'节点运行异常',\
    EXCEPTIONS.RTN_ERROR:'节点返回异常',\
    EXCEPTIONS.UNKNOW_ERROR:'未知异常',\
    EXCEPTIONS.OUTPUT_PARAM_ERROR:'返回参数异常',\
    EXCEPTIONS.DATA_NOT_EXIST:'获取数据不存在',\
    EXCEPTIONS.NOT_BIND_SERVICE:'数据服务未绑定',\
}
# 业务接口可调用函数对应指定枚举
FUNCTION_COMMAND = {
    FUNCTIONS.BIND_CONFIG:'bind_config',\
    FUNCTIONS.START:'start_service',\
    FUNCTIONS.BIND_DATA:'bind_data',\
    FUNCTIONS.GET_DATA:'get_data',\
    FUNCTIONS.SET_DATA:'set_data',\
    FUNCTIONS.STOP:'stop_service',\
    FUNCTIONS.DISPOSE:'dispose_data',\
}
# 业务接口可调用函数对应异常字典
FUNCTION_ERROR = {
    FUNCTIONS.BIND_SERVICE:[EXCEPTIONS.INPUT_PARAMS_ERROR],
    ########################################################
    FUNCTIONS.BIND_CONFIG:[EXCEPTIONS.INPUT_PARAMS_ERROR, EXCEPTIONS.NET_COMM_ERROR, 
    EXCEPTIONS.GET_STATUS_ERROR, EXCEPTIONS.HAVE_BIND_CONFIG, EXCEPTIONS.HAVE_START,
    EXCEPTIONS.APP_ERROR, EXCEPTIONS.RTN_ERROR, EXCEPTIONS.OUTPUT_PARAM_ERROR],
    ########################################################
    FUNCTIONS.START:[EXCEPTIONS.INPUT_PARAMS_ERROR, EXCEPTIONS.NET_COMM_ERROR,
    EXCEPTIONS.GET_STATUS_ERROR, EXCEPTIONS.NOT_BIND_CONFIG, EXCEPTIONS.HAVE_START,
    EXCEPTIONS.APP_ERROR, EXCEPTIONS.RTN_ERROR, EXCEPTIONS.OUTPUT_PARAM_ERROR],
    ########################################################
    FUNCTIONS.STOP:[EXCEPTIONS.INPUT_PARAMS_ERROR, EXCEPTIONS.NET_COMM_ERROR,
    EXCEPTIONS.GET_STATUS_ERROR, EXCEPTIONS.NOT_START, EXCEPTIONS.APP_ERROR, 
    EXCEPTIONS.RTN_ERROR, EXCEPTIONS.OUTPUT_PARAM_ERROR],
    ########################################################
    FUNCTIONS.DISPOSE:[EXCEPTIONS.INPUT_PARAMS_ERROR, EXCEPTIONS.NET_COMM_ERROR,
    EXCEPTIONS.GET_STATUS_ERROR, EXCEPTIONS.HAVE_START, EXCEPTIONS.APP_ERROR, 
    EXCEPTIONS.RTN_ERROR, EXCEPTIONS.OUTPUT_PARAM_ERROR],
    ########################################################
    FUNCTIONS.BIND_DATA:[EXCEPTIONS.INPUT_PARAMS_ERROR, EXCEPTIONS.NET_COMM_ERROR,
    EXCEPTIONS.GET_STATUS_ERROR, EXCEPTIONS.NOT_BIND_CONFIG, EXCEPTIONS.APP_ERROR, 
    EXCEPTIONS.RTN_ERROR, EXCEPTIONS.OUTPUT_PARAM_ERROR],
    ########################################################
    FUNCTIONS.GET_DATA:[EXCEPTIONS.INPUT_PARAMS_ERROR, EXCEPTIONS.NET_COMM_ERROR,
    EXCEPTIONS.GET_STATUS_ERROR, EXCEPTIONS.NOT_BIND_CONFIG, EXCEPTIONS.NOT_START, 
    EXCEPTIONS.APP_ERROR, EXCEPTIONS.RTN_ERROR, EXCEPTIONS.OUTPUT_PARAM_ERROR],
    ########################################################
    FUNCTIONS.SET_DATA:[EXCEPTIONS.INPUT_PARAMS_ERROR, EXCEPTIONS.NET_COMM_ERROR,
    EXCEPTIONS.GET_STATUS_ERROR, EXCEPTIONS.NOT_BIND_CONFIG, EXCEPTIONS.NOT_START, 
    EXCEPTIONS.APP_ERROR, EXCEPTIONS.RTN_ERROR, EXCEPTIONS.OUTPUT_PARAM_ERROR],
}

# 数据服务运行状态名称
log = pylogger.Logger('业务接口')

#--------------------------------------------------------------
def __sendData(service_name, send_data):
    '''
    ---------------------
    通过zmq方式发送数据
    ---------------------
    args:
        service_name: 绑定的数据服务名称
        send_data:    要发送的数据
    returns:
        -1:           数据发送失败
        其他:         发送接收到的返回值
    raises
        Exception: 网络通信异常
    '''
    if not __checkInputParams(service_name, send_data):
        return -1

    connect_string = "tcp://%s:%s" % (service_config[service_name][0], 
        service_config[service_name][1])

    log.debug('connect : %s' %connect_string)

    try:
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect(connect_string)

        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)
        retries_left = REQUEST_RETRIES
        reply = None
        while retries_left:
            socket.send_multipart(send_data)
            expect_reply = True
            while expect_reply:
                socks = dict(poll.poll(REQUEST_TIMEOUT))
                if socks.get(socket) == zmq.POLLIN:
                    reply = socket.recv_multipart()
                    if not reply:
                        break
                    else:
                        # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " Server replied OK " ,reply)
                        retries_left = 0
                        expect_reply = False
                else:
                    try:
                        log.error(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " No response from server, retrying…")
                        socket.setsockopt(zmq.LINGER, 0)
                        socket.close()
                        poll.unregister(socket)
                        retries_left -= 1
                        if retries_left == 0:
                            log.error(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " error:connect Server failure")
                            break
                        log.debug(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " Reconnecting and resending ", send_data)
                        socket = context.socket(zmq.REQ)
                        socket.connect(connect_string)
                        poll.register(socket)
                        socket.send(send_data)
                    except Exception as e:
                        pass

                    time.sleep(1)
                    break
        return reply
    except Exception as e:
        log.error("send data failed, because %s" % repr(e))
        return -1

def __getFrameList(*values):
    '''
    -----------------------
    生成要发送的数据帧集合
    -----------------------
    args:
        *values: 可变的发送数据元组
    returns:
        数据帧集合
    raises
        无
    '''
    frameList = []
    for value in values:
        if isinstance(value, str):
            frameList.append(zmq.Frame(value.encode('utf8')))
        elif isinstance(value, bytes):
            frameList.append(value)
        else:
            print('unknow value: ', value)
    return frameList

def __checkInputObjectAndType(type_name, obj):
    return True if type_name == str(type(obj)).split('.')[-1][:-2] else False

def __checkInputParams(*params):
    '''
    ------------------------
    校验输入的参数是否为空
    ------------------------
    args:
        *params: 可变的参数元组
    returns:
        False:校验失败  
        True: 校验成功
    raises
        无
    '''
    for param in params:
        if param is None:
            return False
    return True

def __send(service_name, cmd, *context):
    '''
    ------------------------
    发送数据
    ------------------------
    args:
        service_name:   绑定的数据服务名称
        cmd:            命令字符串
        *context:       要发送的可变数据内容
    returns:
        -1:             发送失败
        其他:           发送接收到的返回值
    raises
        无
    '''
    list_data = __getFrameList(cmd, *context)
    if len(list_data) < 1:
        return -1

    respose = __sendData(service_name, list_data)

    if (respose is None) or (respose == -1):
        return -1
    else:
        if isinstance(respose, list):
            if len(respose) > 1:
                return respose
            else:
                return str(respose[0], encoding = "utf-8")
        else:
            return respose

def __checkIP(ip_str):
    ''''' 
    ---------------------------------------------
    判断ip_str是否是合法IP地址(正则匹配方法)
    ---------------------------------------------
    args:
        ip:     要校验的ip地址
    returns:
        True:   有效
        False:  无效
    raises
        无
    '''
    import re
    compile_ip=re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')    
    if compile_ip.match(ip_str):    
        return True    
    else:    
        return False 

def __checkPort(port):
    ''''' 
    -----------------------
    判断port是否合法
    -----------------------
    args:
        port:   端口号
    returns:
        True:   有效
        False:  无效
    raises
        无
    '''
    try:
        port = int(port) if not isinstance(port, int) else port
        if port > 0 and port <= 65535:
            return True
        else:
            return False
    except Exception as e:
        return False

import pb_data_sensor_list
def __getRunStatus(service_name):
    '''
    ------------------------
    获取数据服务运行状态
    ------------------------
    args:
        service_name:   绑定的数据服务名称
    returns:
        :             发送失败
        其他:           发送接收到的返回值
    raises
        无
    '''
    if status_config[service_name] == '':
        return None

    status_name = status_config[service_name]
    command = 'get_data'
    respose = __send(service_name, command, 'all_status')
    if isinstance(respose, list):
        if len(respose) > 1:
            datatype = str(respose[0], encoding = "utf-8")
            # print('datatype: %s' % datatype)
            status_data = pb_data_sensor_list.pb_data_sensor_list()
            status_data.ParseFromString(respose[1])
            # print('all_status: %s' % status_data)
            status_list = [status.value for status in status_data.pb_data_sensors if status.name == status_name]
            if len(status_list) > 0:
                return status_list[0]
            else:
                # 状态不存在
                return -2
        else:
            # 返回参数异常
            return -3
    else:
        # 网络异常
        return -1

def __getErrorCode(fun, exce):
    '''
    根据函数和异常,生成异常码
    '''
    code = '%s%s%s' % (EXCEPT_HEAD, '%02d' % fun.value, '%02d' % exce.value)
    return code

def __getErrorMessage(fun, exce):
    '''
    根据异常和消息,生成异常消息
    '''
    message = '%s异常,原因:%s' % (fun.name, EXCEPTIONS_REMARK[exce])
    return message

def __do(service_name, fun, *params):
    '''
    执行与数据服务通信，并返回接收到的数据
    如果状态异常，返回异常码
    '''
    # 获取数据服务状态
    status = __getRunStatus(service_name)
    is_good_status = False
    # 状态获取失败
    if status is None:
        code = __getErrorCode(fun, EXCEPTIONS.GET_STATUS_ERROR)
        message = '%s(%s)' % (__getErrorMessage(fun, EXCEPTIONS.GET_STATUS_ERROR), EXCEPTIONS_REMARK[EXCEPTIONS.NOT_BIND_SERVICE])
    elif status == -1: # 网络通信异常
        code = __getErrorCode(fun, EXCEPTIONS.GET_STATUS_ERROR)
        message = '%s(%s)' % (__getErrorMessage(fun, EXCEPTIONS.GET_STATUS_ERROR), EXCEPTIONS_REMARK[EXCEPTIONS.NET_COMM_ERROR])
    elif status == -2: # 状态不存在
        code = __getErrorCode(fun, EXCEPTIONS.GET_STATUS_ERROR)
        message = '%s(%s)' % (__getErrorMessage(fun, EXCEPTIONS.GET_STATUS_ERROR), EXCEPTIONS_REMARK[EXCEPTIONS.DATA_NOT_EXIST])
    elif status == -3: # 获取状态返回参数异常
        code = __getErrorCode(fun, EXCEPTIONS.GET_STATUS_ERROR)
        message = '%s(%s)' % (__getErrorMessage(fun, EXCEPTIONS.GET_STATUS_ERROR), EXCEPTIONS_REMARK[EXCEPTIONS.OUTPUT_PARAM_ERROR])        
    # 状态获取成功
    else:
        svc_stt = SERVICE_STATUS(int(status))
        # 状态为运行异常时,返回异常码
        if svc_stt == SERVICE_STATUS.ERROR:
            code = __getErrorCode(fun, EXCEPTIONS.APP_ERROR)
            message = __getErrorMessage(fun, EXCEPTIONS.APP_ERROR)
        # 状态非运行异常
        else:
            # 当调用bind config函数时
            if fun == FUNCTIONS.BIND_CONFIG:
                # 只有当数据服务状态为未配置时，才能调用bing config函数
                if svc_stt == SERVICE_STATUS.NONE:
                    is_good_status = True
                elif svc_stt == SERVICE_STATUS.CONFIG:
                    code = __getErrorCode(fun, EXCEPTIONS.HAVE_BIND_CONFIG)
                    message = __getErrorMessage(fun, EXCEPTIONS.HAVE_BIND_CONFIG)
                elif svc_stt == SERVICE_STATUS.RUN:
                    code = __getErrorCode(fun, EXCEPTIONS.HAVE_START)
                    message = __getErrorMessage(fun, EXCEPTIONS.HAVE_START)
                else:
                    code = __getErrorCode(fun, EXCEPTIONS.UNKNOW_ERROR)
                    message = __getErrorMessage(fun, EXCEPTIONS.UNKNOW_ERROR)
            else:
                # 当调用非bind config函数时
                # 如果运行状态为未配置,则返回异常码
                if svc_stt == SERVICE_STATUS.NONE:
                    code = __getErrorCode(fun, EXCEPTIONS.NOT_BIND_CONFIG)
                    message = __getErrorMessage(fun, EXCEPTIONS.NOT_BIND_CONFIG)
                else:
                    # 当调用start函数时
                    if fun == FUNCTIONS.START:
                        # 只有当运行状态为未配置时，才能调用start函数
                        if svc_stt == SERVICE_STATUS.CONFIG:
                            is_good_status = True
                        elif svc_stt == SERVICE_STATUS.RUN:
                            code = __getErrorCode(fun, EXCEPTIONS.HAVE_START)
                            message = __getErrorMessage(fun, EXCEPTIONS.HAVE_START)
                        else:
                            code = __getErrorCode(fun, EXCEPTIONS.UNKNOW_ERROR)
                            message = __getErrorMessage(fun, EXCEPTIONS.UNKNOW_ERROR)
                    # 当调用bind data函数时,运行状态为已配置和已运行都可以调用bind data
                    elif fun == FUNCTIONS.BIND_DATA:
                        is_good_status = True
                    # 当调用get data、set data和stop函数时
                    elif fun == FUNCTIONS.GET_DATA or fun == FUNCTIONS.SET_DATA or fun == FUNCTIONS.STOP:
                        # 只有当运行状态为运行时，才能调用以上三个函数
                        if svc_stt == SERVICE_STATUS.RUN:
                            is_good_status = True
                        elif svc_stt == SERVICE_STATUS.CONFIG:
                            code = __getErrorCode(fun, EXCEPTIONS.NOT_START)
                            message = __getErrorMessage(fun, EXCEPTIONS.NOT_START)
                        else:
                            code = __getErrorCode(fun, EXCEPTIONS.UNKNOW_ERROR)
                            message = __getErrorMessage(fun, EXCEPTIONS.UNKNOW_ERROR)
                    # 当调用dispose函数时
                    elif fun == FUNCTIONS.DISPOSE:
                        # 只有当运行状态为已运行时，才能调用dispose函数
                        if svc_stt == SERVICE_STATUS.CONFIG:
                            is_good_status = True
                        elif svc_stt == SERVICE_STATUS.RUN:
                            code = __getErrorCode(fun, EXCEPTIONS.HAVE_START)
                            message = __getErrorMessage(fun, EXCEPTIONS.HAVE_START)
                        else:
                            code = __getErrorCode(fun, EXCEPTIONS.UNKNOW_ERROR)
                            message = __getErrorMessage(fun, EXCEPTIONS.UNKNOW_ERROR)
    # 如果读取到的状态是合适的,则获取数据服务返回数据
    if is_good_status:
        command = FUNCTION_COMMAND[fun]
        respose = __send(service_name, command, *params)
        # 当返回多数据时,应该为类型+数值格式
        if isinstance(respose, list):
            if len(respose) > 1:
                datatype = str(respose[0], encoding = "utf-8")
                return respose
            else:
                # 其他格式的返回值,则返回异常码
                code = __getErrorCode(fun, EXCEPTIONS.RTN_ERROR)
                message = __getErrorMessage(fun, EXCEPTIONS.RTN_ERROR)
        # 当返回一个数据时
        else:
            # 如果为-1,则为网络通信异常
            if respose == -1:
                code = __getErrorCode(fun, EXCEPTIONS.NET_COMM_ERROR)
                message = __getErrorMessage(fun, EXCEPTIONS.NET_COMM_ERROR)
            else:
                # 如果返回的数据为非1,则为数据服务返回的异常码
                if eval(str(respose)) != 1:
                    code = __getErrorCode(fun, EXCEPTIONS.RTN_ERROR)
                    message = '%s(%s)' % (__getErrorMessage(fun, EXCEPTIONS.RTN_ERROR), repr(respose))
                else:
                    # 正确的返回值
                    return respose
    log.error(message)
    return code

#--------------------------------------------------------------
def bindService(ip, port, name, service_name):
    '''
    ---------------------------------------------------------
    绑定数据服务名称与IP、PORT、NAME和对应数据的运行状态名称
    ---------------------------------------------------------
    args:
        ip:             数据服务对应的IP地址
        port:           数据服务对应的PORT
        name:           数据服务名称
        service_name:   设置数据服务绑定的名称
    returns:
        1:              绑定成功
        其他:           异常码
    raises
        无
    '''
    global service_config
    global status_config

    if __checkInputParams(ip, port, name, service_name):
        if __checkIP(ip) and __checkPort(port):
            index = str(port)[1:2]
            status_name = '%s_status_%s' % (name,index)
            service_config[service_name] = (ip, port, name, service_name)
            status_config[service_name] = status_name
            return 1

    code = __getErrorCode(FUNCTIONS.BIND_SERVICE, EXCEPTIONS.INPUT_PARAMS_ERROR)
    message = __getErrorMessage(FUNCTIONS.BIND_SERVICE, EXCEPTIONS.INPUT_PARAMS_ERROR)
    log.error(message)
    return code        

#--------------------------------------------------------------
def bindConfig(service_name, pb_config_type, pb_config, config_name):
    '''
    ---------------------------------
    绑定配置名称与配置内容映射
    ---------------------------------
    args:
        service_name:   绑定的数据服务名称
        pb_config_type: config对象类型
        pb_config:      config对象
        config_name:    config对象名称(本期此配置无效)
    returns:
        执行bind config命令后的返回值或异常码
    raises
        无
    '''
    if not service_config.__contains__(service_name):
        is_params_ok = False
    else:
        is_params_ok = __checkInputParams(service_name, pb_config_type, pb_config, CONFIG_NAME)
        if is_params_ok:
            is_params_ok = __checkInputObjectAndType(pb_config_type, pb_config)

    if not is_params_ok:
        code = __getErrorCode(FUNCTIONS.BIND_CONFIG, EXCEPTIONS.INPUT_PARAMS_ERROR)
        message = __getErrorMessage(FUNCTIONS.BIND_CONFIG, EXCEPTIONS.INPUT_PARAMS_ERROR)
        log.error(message)
        return code

    serialize_data = pb_config.SerializeToString()
    respose = __do(service_name, FUNCTIONS.BIND_CONFIG, pb_config_type, serialize_data, CONFIG_NAME)
    return respose

#--------------------------------------------------------------
def dispose(service_name, config_name, data_name):
    '''
    ------------------------------------------------------------
    清空指定配置名称对应的配置信息和指定数据名称对应的数据信息
    ------------------------------------------------------------
    args:
        service_name:   绑定过的数据服务名称
        config_name:    释放config对象占用资源(本期此配置无效)
        data_name:      绑定的数据名称
    returns:
        执行释放命令后的返回值或异常码
    raises
        无
    '''
    if not service_config.__contains__(service_name):
        is_params_ok = False
    else:
        is_params_ok = __checkInputParams(service_name, CONFIG_NAME, data_name)

    if not is_params_ok:
        code = __getErrorCode(FUNCTIONS.DISPOSE, EXCEPTIONS.INPUT_PARAMS_ERROR)
        message = __getErrorMessage(FUNCTIONS.DISPOSE, EXCEPTIONS.INPUT_PARAMS_ERROR)
        log.error(message)
        return code

    respose = __do(service_name, FUNCTIONS.DISPOSE, CONFIG_NAME, data_name)
    return respose

#--------------------------------------------------------------
def start(service_name, config_name):
    '''
    ---------------------------
    启动服务
    ---------------------------
    args:
        service_name:   绑定过的数据服务名称
        config_name:    config对象名称(本期此配置无效)
    returns:
        执行启动命令后的返回值或异常码
    raises
        无
    '''
    if not service_config.__contains__(service_name):
        is_params_ok = False
    else:
        is_params_ok = __checkInputParams(service_name, CONFIG_NAME)

    if not is_params_ok:
        code = __getErrorCode(FUNCTIONS.START, EXCEPTIONS.INPUT_PARAMS_ERROR)
        message = __getErrorMessage(FUNCTIONS.START, EXCEPTIONS.INPUT_PARAMS_ERROR)
        log.error(message)
        return code

    respose = __do(service_name, FUNCTIONS.START, CONFIG_NAME)
    return respose

#--------------------------------------------------------------
def stop(service_name, config_name):
    '''
    ---------------------------
    停止服务
    ---------------------------
    args:
        service_name:   绑定过的数据服务名称
        config_name:    config对象名称(本期此配置无效)
    returns:
        执行停止命令后的返回值或异常码
    raises
        无
    '''
    if not service_config.__contains__(service_name):
        is_params_ok = False
    else:
        is_params_ok = __checkInputParams(service_name, CONFIG_NAME)

    if not is_params_ok:
        code = __getErrorCode(FUNCTIONS.STOP, EXCEPTIONS.INPUT_PARAMS_ERROR)
        message = __getErrorMessage(FUNCTIONS.STOP, EXCEPTIONS.INPUT_PARAMS_ERROR)
        log.error(message)
        return code

    respose = __do(service_name, FUNCTIONS.STOP, CONFIG_NAME)
    return respose

#--------------------------------------------------------------
def bindData(service_name, pb_data_type, pb_data, data_name):
    '''
    ---------------------------
    绑定数据名称与数据对象映射
    ---------------------------
    args:
        service_name:   绑定过的数据服务名称
        pb_data_type:   要绑定数据的数据类型
        pb_data:        要绑定的数据对象
        data_name:      绑定的数据名称
    returns:
        获取到的数据对象或异常码
    raises
        无
    '''
    if not service_config.__contains__(service_name):
        is_params_ok = False
    else:
        is_params_ok = __checkInputParams(service_name, pb_data_type, pb_data, data_name)
        if is_params_ok:
            is_params_ok = __checkInputObjectAndType(pb_data_type, pb_data)

    if not is_params_ok:
        code = __getErrorCode(FUNCTIONS.BIND_DATA, EXCEPTIONS.INPUT_PARAMS_ERROR)
        message = __getErrorMessage(FUNCTIONS.BIND_DATA, EXCEPTIONS.INPUT_PARAMS_ERROR)
        log.error(message)
        return code

    serialize_data = pb_data.SerializeToString()
    respose = __do(service_name, FUNCTIONS.BIND_DATA, pb_data_type, serialize_data, data_name)
    return respose

#--------------------------------------------------------------
def getData(service_name, data_name, pb_data_type, pb_data):
    '''
    ------------------------
    获取数据
    ------------------------
    args:
        service_name:   绑定过的数据服务名称
        data_name:      绑定的数据名称
        pb_data_type:   要获取数据的数据类型
        pb_data:        要获取的数据对象
    returns:
        获取到的数据对象或异常码
    raises
        无
    '''
    if not service_config.__contains__(service_name):
        is_params_ok = False
    else:
        is_params_ok = __checkInputParams(service_name, data_name, pb_data_type, pb_data)
        if is_params_ok:
            is_params_ok = __checkInputObjectAndType(pb_data_type, pb_data)

    if not is_params_ok:
        code = __getErrorCode(FUNCTIONS.GET_DATA, EXCEPTIONS.INPUT_PARAMS_ERROR)
        message = __getErrorMessage(FUNCTIONS.GET_DATA, EXCEPTIONS.INPUT_PARAMS_ERROR)
        log.error(message)
        return code

    respose = __do(service_name, FUNCTIONS.GET_DATA, data_name)

    if isinstance(respose, list) and len(respose) > 1:
        datatype = str(respose[0], encoding = "utf-8")
        pb_data.ParseFromString(respose[1])
        return 1
    else:
        return respose        

#--------------------------------------------------------------
def setData(service_name, data_name, pb_data_type, pb_data):
    '''
    ------------------------
    设置数据
    ------------------------
    args:
        service_name:   绑定过的数据服务名称
        data_name:      绑定的数据名称
        pb_data_type:   设置数据的数据类型
        pb_data:        要设置的数据对象，当对象为None时为删除操作
    returns:
        设置的返回值或异常码
    raises
        无
    '''
    if not service_config.__contains__(service_name):
        is_params_ok = False
    else:
        if pb_data:
            is_params_ok = __checkInputParams(service_name, pb_data_type, pb_data, data_name)
            if is_params_ok:
                is_params_ok = __checkInputObjectAndType(pb_data_type, pb_data)
            else:
                is_params_ok = False
        else:
            is_params_ok = True

    if not is_params_ok:
        code = __getErrorCode(FUNCTIONS.SET_DATA, EXCEPTIONS.INPUT_PARAMS_ERROR)
        message = __getErrorMessage(FUNCTIONS.SET_DATA, EXCEPTIONS.INPUT_PARAMS_ERROR)
        log.error(message)
        return code

    serialize_data = None
    if pb_data is None:
        serialize_data = b''
    else:
        serialize_data = pb_data.SerializeToString()

    respose = __do(service_name, FUNCTIONS.SET_DATA, pb_data_type, serialize_data, data_name)
    return respose

#--------------------------------------------------------------
def autoGetData(service_name, data_name, cycle, pb_data_type, pb_data):
    '''
    ------------------------
    订阅数据
    ------------------------
    args:
        service_name:   绑定过的数据服务名称
        data_name:      绑定的数据名称
        cycle:          订阅数据的周期
        pb_data_type:   订阅数据的数据类型
        pb_data:        要订阅的数据对象
    returns:
        
    raises
        无
    '''
    if (service_name is None) or (data_name is None) or (cycle is None) or (pb_data_type is None) or (pb_data is None):
        return -1
    pass

#--------------------------------------------------------------
def createExceptionDictory(file_path):
    '''
    创建异常字典文件
    '''
    except_dict = {}
    for (key, value) in FUNCTION_ERROR.items():
        list_name = {eval('%s%s%s' % (EXCEPT_HEAD, '%02d' % key.value, '%02d' % func.value)): '%s异常,原因:%s'%(key.name,EXCEPTIONS_REMARK[func]) for func in value }
        for (k,v) in list_name.items():
            except_dict[k] = v

    from struct import pack
    import binascii  
    with open(file_path,'w') as f:
        f.writelines(['[%s]: %s\n' % ('0x%s' % str(binascii.b2a_hex(pack('>L', item[0])))[2:-1],item[1]) for item in sorted(except_dict.items())])

# createExceptionDictory('c:/inteface_exception.txt')