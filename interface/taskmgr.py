#!/usr/local/python/bin
# coding=utf-8
# 

__author__ = 'cuiwei'
__version__ = '0.1'
__all__ = ['set_status', 'get_stauts']
exception_dict = {'custom':-1, 'Exception':-100, 'IOError':-101}

#---------------------------------------------------------------------------
import subprocess
import os
class task:
    '''
    任务进程对象，包含属性：
    1、执行程序路径
    2、监听ip
    3、端口
    4、数据服务名称
    5、当前状态
    6、进程ID
    '''
    def __init__(self, exe_path, exe_params):
        '''
        task对象构造方法
        args:
            task_context: path, ip, port, name格式的字符串
        returns:
        raises:
        '''
        self.handle, self.exe_path, self.exe_params = None, exe_path, exe_params
        self.status, self.pid, self.status_last_time = 0,0,0
        if exe_params.split(' ') is not None:
            params = exe_params.split(' ')
            self.ip, self.port, self.name = params if len(params) == 3 else ['',0,'']

    def set_status(self, status_value):
        '''
        设置任务对象状态
        args:
            status_value: 状态数值
        returns:
        raises
        '''
        self.status = status_value

    def get_status(self):
        '''
        获取任务对象状态
        args:
        returns:
            状态数值
        raises
        '''
        return self.status

    def get_pid(self):
        '''
        获取任务进程号
        args:
        returns:
            任务进程ID
        raises
        '''
        return self.pid

    def set_status_last_time(self, time_span):
        '''
        设置任务对象状态更新时间
        args:
            time_span: 时间戳
        returns:
        raises
        '''
        self.status_last_time = time_span

    def get_status_last_time(self):
        '''
        获取状态最后一次更新时间戳
        args:
        returns:
            状态最后一次更新的时间戳
        raises
        '''
        return self.status_last_time

    def start_task(self):
        '''
        启动任务管理进程
        args:
        returns:
        raises
        '''
        try:
            is_file_existed = False
            #检查要启动的程序路径有效性
            if len(self.exe_path.split(' ')) > 1:
                if os.path.exists(self.exe_path.split(' ')[1]):
                    is_file_existed = True
            else:
                if os.path.exists(self.exe_path):
                    is_file_existed = True

            if is_file_existed:
                file_out = 'taskmgr_out.txt'
                file_err = 'taskmgr_err.txt'
                self.handle = common.start_exe('%s %s' % (self.exe_path, self.exe_params), file_out, file_err)
                
                n = 0
                handle_poll = None
                while n < 3:
                    handle_poll = self.handle.poll()
                    time.sleep(0.5)
                    n += 1

                if handle_poll is None:
                    self.pid = self.handle.pid
                    self.status_last_time = common.get_current_timespan()
                    return 1
                else:
                    self.dispose()
            else:
                raise custom_exception(exception_dict['custom'], '程序[%s]不存在' % self.exe_path)
        except Exception as e:
            raise custom_exception(exception_dict['custom'], '%s' % repr(e))

    def stop_task(self):
        '''
        停止任务管理进程
        args:
        returns:
            状态最后一次更新的时间戳
        raises
        '''
        try:
            if self.handle is not None:
                self.handle.terminate()
                self.handle = None
                return 1
        except Exception as e:
            self.handle = None
            raise custom_exception(exception_dict['custom'], '%s' % repr(e))
        
    def dispose(self):
        if self.handle is not None:
            self.handle.terminate()

        self.status, self.pid, self.status_last_time, self.handle = 0,0,0,None

#---------------------------------------------------------------------------
class custom_exception(BaseException):
    '''
    通过继承Exception或者BaseException类实现自定义异常类
    '''
    def __init__(self,exception_code=0, exception_message="custom exception"):
        self.code = exception_code
        self.message = exception_message
        BaseException.__init__(self) 

    def __str__(self):
        return repr(self.message)

#---------------------------------------------------------------------------
import time
import re
import os
import subprocess

class common:
    '''
    '''
    def start_exe(exe, file_out, file_error, time_out=30):
        try:
            fdout = open(file_out, 'w')
            fderr = open(file_error, 'w')
            print('exe:',exe)
            p = subprocess.Popen(exe, stdout=fdout, stderr=fderr, shell=True)
            return p
        except Exception as e:
            raise e
        
    def check_file_existed(file_path):
        return os.path.exists(file_path)

    def get_current_timespan():
        return int(time.time())

    def get_datetime_by_timespan(time_span, date_format="%Y-%m-%d %H:%M:%S"):
        timeArray = time.localtime(time_span)
        date_time = time.strftime(date_format, timeArray)
        return date_time

    def regular_match_ip(ip):
        '''进行正则匹配ip，加re.IGNORECASE是让结果返回bool型'''
        pattern=re.match(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',ip,re.IGNORECASE)
        return pattern

    def regular_match_port(port):
        try:
            port = int(port)
            if port >= 0 and port <= 65535:
                return True
            else:
                return False
        except Exception as e:
            return False

    def regular_match_url(url):
        pattern=re.match(r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?',url,re.IGNORECASE)
        return pattern

    def regular_match_email(email):
        pattern=re.match(r'\w+@([0-9a-zA-Z]+[-0-9a-zA-Z]*)(\.[0-9a-zA-Z]+[-0-9a-zA-Z]*)+',email,re.IGNORECASE)
        return pattern

    def check_port(host,port):
        import socket
        s = None
        for res in socket.getaddrinfo(host, port, socket.AF_UNSPEC,socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                s = socket.socket(af, socktype, proto)
            except socket.error as msg:
                s = None
                print (str(msg))
                continue
            try:
                s.settimeout(2)
                s.connect(sa)
            except socket.error as msg:
                print (str(msg))
                s.close()
                s = None
                continue
            break
        if s is None:
            return 0
        s.close()
        return 1

#---------------------------------------------------------------------------
import logger
import os
import threading
import sys

log = logger.logger(logname='log.txt', loglevel=1, logger="taskmgr").getlog()

'''
任务管理程序
'''
RUN_TASK_MANAGE = True
RUN_STATUS_MACHINE = True
UPDATE_STATUS_CYCLE = 5
RUN_TASK_CYCLE = 10
DO_TIME = 10

tasks = []

def __get_line_exe_params(line_context):
    '''
    检查启动内容，并返回有效的命令和参数内容
    args:
        line_context: 文件内容
    returns:
        命令和参数内容
    raises
    '''
    # 检查内容格式长度是否有效
    if len(line_context.split(',')) != 4: 
        # 匹配的内容格式描述
        patten = '[exe_path, ip, port, name]' 
        raise custom_exception(exception_dict['custom'], '%s 格式不匹配%s' % (l, patten))
    else:
        app_path, ip, port, name = ''.join(line_context).strip('\n').split(',')

        # 检查app路径文件是否存在
        # is_file_existed = False
        # if len(app_path.split(' ')) > 1:
        #     if os.path.exists(app_path.split(' ')[1]):
        #         is_file_existed = True
        #     else:
        #         if os.path.exists(app_path):
        #             is_file_existed = True

        # if not is_file_existed:
        #     raise custom_exception(exception_dict['custom'], '文件[%s]不存在,请检查...' % app_path)

        # 检查ip地址是否有效
        if not common.regular_match_ip(ip):
            raise custom_exception(exception_dict['custom'], 'ip地址[%s]无效,请检查...' % ip)

        # 检查端口号是否有效
        if not common.regular_match_port(port):
            raise custom_exception(exception_dict['custom'], '端口号[%s]无效,请检查...' % port)

    return (app_path, ' '.join((ip, port, name)))

def init_tasks(file_path):
    '''
    运行任务管理程序
    args:
        file_path: 被管理程序的列表文件路径
    returns:
        初始化成功个数
    raises
    '''
    #获取启动文件内容
    init_count = 0
    lines = []
    try:
        with open(file_path, 'r') as run_file:
            for line in run_file:
                try:
                    # 判断是否为重复启动程序
                    if line in lines:
                        log.error('[%s]启动失败,原因:该启动程序重复,请检查...' % line)
                    else:
                        # 获取启动程序的命令及参数
                        print('line:',line)
                        exe_params = __get_line_exe_params(line)
                        # 创建任务对象
                        print('exe_params:',exe_params)
                        tk = task(exe_params[0], exe_params[1])
                        # 将启动成功的任务对象加入到任务管理队列中
                        tasks.append(tk)
                        init_count += 1
                # 自定义异常处理
                except custom_exception as ce:
                    log.error('[%s]%s' % (ce.code, ce.message))
    except IOError as ioe:
        log.error('[%s]启动失败,原因:%s' % (exception_dict['IOError'], repr(e))) 

    return init_count

def start_tasks(task_list):
    '''
    启动任务
    args:
    returns:
        启动任务成功个数
    raises
    '''
    start_count = 0
    if len(task_list) > 0:
        for tsk in task_list:
            try:
                log.info('程序[%s]正在启动...' % tsk.name)
                flag = tsk.start_task()
                if flag == 1:
                    start_count += 1
                    log.info('程序[%s]启动成功' % tsk.name)
                else:
                    log.error('程序[%s]启动失败' % tsk.name)
                    log.info('由于启动失败，强制终止程序[%s]' % tsk.name)
                    tsk.dispose()

                time.sleep(1)
            except custom_exception as ce:
                log.error('程序[%s]启动失败,原因:%s' % (tsk.name, ce.message))
            except Exception as e:
                log.error('程序[%s]启动失败,原因:%s' % (tsk.name, e.message))
    return start_count

def stop_tasks(task_list):
    '''
    停止任务
    args:
    returns:
        停止任务成功个数
    raises
    '''
    stop_count = 0
    if len(task_list) > 0:
        for tsk in task_list:
            try:
                if tsk.get_status_last_time() > 0:
                    log.info('程序[%s]正在停止...' % tsk.name)
                    flag = tsk.stop_task()
                    if flag == 1:
                        tsk.dispose()
                        stop_count += 1
                        log.info('程序[%s]停止成功' % tsk.name)
                    else:
                        log.error('程序[%s]停止失败' % tsk.name)
                    time.sleep(1)
            except custom_exception as ce:
                log.error('程序[%s]停止失败,原因:%s' % (tsk.name, repr(ce)))
            except Exception as e:
                log.error('程序[%s]停止失败,原因:%s' % (tsk.name, repr(e)))
    return stop_count

def run_over(signum, frame):
    '''
    任务管理程序运行结束，释放内容
    args:
    returns:
    raises
    '''
    RUN_STATUS_MACHINE = False
    RUN_TASK_MANAGE = False

    if len(tasks) > 0:
        stop_tasks(tasks)
        tasks.clear()

    log.info('任务管理运行正常退出.')
    sys.exit()

def do():
    '''
    任务程序控制器，根据业务要求，通过任务对象的时间和状态判断进行任务启停
    args:
    returns:
    raises
    '''
    while RUN_TASK_MANAGE:
        current_time = common.get_current_timespan()
        for tsk in tasks:
            log.debug('程序[%s]当前状态更新时间为:%s' % (tsk.name, tsk.get_status_last_time()))
            # 当前任务运行状态为非正常(不等于1),且大于等于设定的有效时间，则重启该任务
            if (current_time - tsk.get_status_last_time() >= DO_TIME) and tsk.get_status() != 1:
                # 停止任务
                try:
                    if tsk.handle is not None:
                        flag = tsk.stop_task()
                        time.sleep(1)
                        if flag == 1:
                            tsk.dispose()
                            log.info('程序[%s]停止成功' % tsk.name)
                        else:
                            log.error('程序[%s]停止失败' % tsk.name)
                except custom_exception as ce:
                    log.error('程序[%s]停止失败,原因:%s' % (tsk.name, repr(ce)))
                except Exception as e:
                    log.error('程序[%s]停止失败,原因:%s' % (tsk.name, repr(e)))
                    
                try:
                    if tsk.handle is None:
                        flag = tsk.start_task()
                        time.sleep(1)
                        if flag == 1:
                            log.info('程序[%s]启动成功' % tsk.name)
                        else:
                            log.error('程序[%s]启动失败' % tsk.name)
                except custom_exception as ce:
                    log.error('程序[%s]启动失败,原因:%s' % (tsk.name, repr(ce)))
                except Exception as e:
                    log.error('程序[%s]启动失败,原因:%s' % (tsk.name, repr(e)))

                time.sleep(1)

        time.sleep(RUN_TASK_CYCLE)

def status_machine():
    '''
    状态机，负责定时获取及更新任务对象状态
    '''
    import data_service_interface as dsif
    import pb_data_sensor
    import pb_data_sensor_list

    class _service_status:
        '''
        服务状态对象，提供获取任务状态、更新任务状态功能
        '''
        def __init__(self, task_obj):
            self._task = task_obj
            self._bindService = False

        def refresh_service_status(self):
            _good_status = False
            _status_value = None
            if not self._bindService:
                ret = dsif.bindService(self._task.ip, self._task.port, self._task.name, 'get_status')
                if int(ret) == 1:
                    self._bindService = True
                    log.info('获取[%s]状态bind service成功' % self._task.name)
                else:
                    self._bindService = False
                    log.error('获取[%s]状态bind service异常,原因:%s' % (self._task.name, ret))

            if self._task.handle is not None:
                # 状态数据对象
                bindData = pb_data_sensor_list.pb_data_sensor_list()
                bindData.list_id = 1
                status_tag = bindData.pb_data_sensors.add()
                status_tag.name = '%s_status' % self._task.name
                try:
                    ret = dsif.bindData('get_status', 'pb_data_sensor_list', bindData, 'get_status_list')
                    if int(ret) == 1:
                        self._bindData = True
                        log.info('获取[%s]状态[bind data]成功' % self._task.name)
                    else:
                        self._bindData = False
                        log.error('获取[%s]状态[bind data]异常,原因:%s' % (self._task.name, ret))
                except Exception as e:
                    self._bindData = False
                    log.error('获取[%s]状态[bind data]异常,原因:%s' % (self._task.name, repr(e)))

                self._getData = pb_data_sensor_list.pb_data_sensor_list()
                try:
                    ret = dsif.getData('get_status', 'get_status_list', 'pb_data_sensor_list', self._getData)
                    if ret == 1 and len(self._getData.pb_data_sensors) > 0:
                        _status_value = int(self._getData.pb_data_sensors[0].value)
                        _good_status = True
                        log.debug('[%s]当前运行状态为:%s' % (self._task.name, _status_value))
                except Exception as e:
                    log.error('获取[%s]get data异常,原因:%s' % (self._task.name, repr(e)))

                if _good_status:
                    self._task.set_status(_status_value)
                    self._task.set_status_last_time(common.get_current_timespan())
                else:
                    self._task.set_status(0)
    #---------------------------------------------------------------------------
    
    run_tasks = []
    for tsk in tasks:
        if tsk.ip == '':
            log.error('初始化[%s]状态机失败,原因:%s' % (self.exe_path, '运行参数缺失'))
        else:
            ssts = _service_status(tsk)
            run_tasks.append(ssts)

    if len(run_tasks) > 0:
        while RUN_STATUS_MACHINE:
            for ssts in run_tasks:
                ssts.refresh_service_status()
                time.sleep(1)
            time.sleep(UPDATE_STATUS_CYCLE)

if __name__ == '__main__':
    import signal

    file_existed = False
    try:
        file = os.environ["richisland_home"] + '/run_config.cfg'
    except Exception as e:
        log.error('环境变量[%s]未定义,请检查...' % 'richisland_home')

    file_existed = common.check_file_existed(file)
    if not file_existed:
        log.error('启动配置文件[%s]不存在,请检查...' % file)
        sys.exit()

    count = init_tasks(file)

    if count > 0:
        log.info('任务管理程序初始化启动成功.')
        if len(tasks) > 0:
            try:
                signal.signal(signal.SIGINT, run_over)

                thread_do = threading.Thread(target = do)
                thread_do.setName('do')
                thread_do.setDaemon(True)
                thread_do.start()

                time.sleep(5)

                thread_status_machine = threading.Thread(target = status_machine)
                thread_status_machine.setName('status_machine')
                thread_status_machine.setDaemon(True)
                thread_status_machine.start()

                while True:
                    time.sleep(1)
            except Exception as e:
                raise e
        else:
            log.info('任务管理程序无可管理的任务.')
    else:
        log.info('任务管理程序初始化启动任务失败.')