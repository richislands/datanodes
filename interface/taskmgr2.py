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
import time

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
    def __init__(self, context):
        '''
        task对象构造方法
        args:
            task_context: path, ip, port, name格式的字符串
        returns:
        raises:
        '''
        self.is_running = False
        self.handle, self.exe_path, self.status, self.status_last_time = None, context.strip('\n'), 0, 0
        self.name = self.exe_path.split(' ')[-1].strip('\n') if len(self.exe_path.split(' ')) > 0 else None

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
        return self.handle.pid if self.handle else 0

    def update_status_time(self, time_span):
        '''
        设置任务对象状态更新时间
        args:
            time_span: 时间戳
        returns:
        raises
        '''
        self.status_last_time = time_span

    def get_status_time(self):
        '''
        获取状态更新时间戳
        args:
        returns:
            状态更新时间戳
        raises
        '''
        return self.status_last_time

    def task_is_running(self):
        if self.handle is not None:
            n = 0
            while n < 2:
                p_poll = self.handle.poll()
                n += 1
                time.sleep(0.5)
            if p_poll is None:
                return True
        return False

    def __run_exe(self, exe, file_out, file_error):
        try:
            fdout = open(file_out, 'w')
            fderr = open(file_error, 'w')
            p = subprocess.Popen(exe, stdout=fdout, stderr=fderr, shell=False)
            return p
        except Exception as e:
            raise e

    def start_task(self):
        '''
        启动任务管理进程
        args:
        returns:
        raises
        '''
        try:
            file_out = 'taskmgr_out.txt'
            file_err = 'taskmgr_err.txt'
            self.handle = self.__run_exe(self.exe_path, file_out, file_err)            
            return 1
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
                print('---------------------------stop-------------------------')
                return 1
            else:
                return None
        except Exception as e:
            raise custom_exception(exception_dict['custom'], '%s' % repr(e))
        
    def dispose(self):
        if self.handle is not None:
            self.handle.terminate()

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
RUN_TASK_CYCLE = 5
DO_TIME = 10

tasks = []

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
                # 判断内容是否为空
                if line is None or line.strip() == '':
                    continue

                # 判断是否为重复启动程序
                if line in lines:
                    log.error('[%s]启动失败,原因:该启动程序重复,请检查...' % line)
                    break

                try:
                    # 创建任务对象
                    tk = task(line)
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
    if task_list is not None:
        for tsk in task_list:
            try:
                log.info('程序[%s]正在启动...' % tsk.name)
                flag = tsk.start_task()
                time.sleep(2)
                if flag == 1 and tsk.task_is_running():
                    log.info('程序[%s]启动成功, 进程号:[%s]' % (tsk.name,tsk.get_pid()))
                    tsk.is_running = True
                else:
                    log.error('程序[%s]启动失败' % tsk.name)
                    tsk.is_running = False
            except custom_exception as ce:
                log.error('程序[%s]启动失败,原因:%s' % (tsk.name, ce.message))
            except Exception as e:
                log.error('程序[%s]启动失败,原因:%s' % (tsk.name, e.message))

def stop_tasks(task_list):
    '''
    停止任务
    args:
    returns:
        停止任务成功个数
    raises
    '''
    if task_list is not None:
        for tsk in task_list:
            try:
                log.info('程序[%s]正在停止...' % tsk.name)
                flag = tsk.stop_task()
                time.sleep(2)
                if flag == 1 and (not tsk.task_is_running()):
                    tsk.dispose()
                    log.info('程序[%s]停止成功' % tsk.name)
                else:
                    log.error('程序[%s]停止失败' % tsk.name)                    
            except custom_exception as ce:
                log.error('程序[%s]停止失败,原因:%s' % (tsk.name, repr(ce)))
            except Exception as e:
                log.error('程序[%s]停止失败,原因:%s' % (tsk.name, repr(e)))

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
        current_time = int(time.time())
        for tsk in tasks:
            # 当前任务运行状态为非正常(不等于1),且大于等于设定的有效时间，则重启该任务
            if (current_time - tsk.get_status_time() >= DO_TIME) and tsk.get_status() != 1:
                # 停止任务
                if tsk.task_is_running(): 
                    stop_tasks([tsk])
                
                # 启动任务
                if not tsk.task_is_running():
                    start_tasks([tsk])

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
            self._bindData = False
            self._serviceName = '%s_get_status' % task_obj.name
            self._ip = task_obj.exe_path.split(' ')[-3] if len(task_obj.exe_path.split(' ')) > 2 else None
            self._port = task_obj.exe_path.split(' ')[-2] if len(task_obj.exe_path.split(' ')) > 1 else None

        def refresh_service_status(self):
            if not self._task.is_running:
                self._bindData = False
                self._task.set_status(0)
            else:
                _good_status = False
                _status_value = None

                if not self._bindService:
                    ret = dsif.bindService(self._ip, self._port, self._task.name, self._serviceName)
                    if int(ret) == 1:
                        self._bindService = True
                        log.info('获取[%s]状态bind service成功' % self._task.name)
                    else:
                        self._bindService = False
                        log.error('获取[%s]状态bind service异常,原因:%s' % (self._task.name, ret))

                if not self._bindData:
                    # 状态数据对象
                    bindData = pb_data_sensor_list.pb_data_sensor_list()
                    bindData.list_id = 1
                    status_tag = bindData.pb_data_sensors.add()

                    status_tag.name = '%s_status' % self._task.name
                    log.debug('准备[%s]状态数据bind data...' % self._task.name)
                    try:
                        ret = dsif.bindData(self._serviceName, 'pb_data_sensor_list', bindData, 'get_status_list')
                        if int(ret) == 1:
                            self._bindData = True
                            log.info('获取[%s]状态[bind data]成功' % self._task.name)
                        else:
                            self._bindData = False
                            log.error('获取[%s]状态[bind data]失败,原因:%s' % (self._task.name, ret))
                    except Exception as e:
                        self._bindData = False
                        log.error('获取[%s]状态[bind data]异常,原因:%s' % (self._task.name, repr(e)))                

                if self._bindData:
                    self._getData = pb_data_sensor_list.pb_data_sensor_list()
                    try:
                        log.debug('准备[%s]状态数据get data...' % self._task.name)
                        ret = dsif.getData(self._serviceName, 'get_status_list', 'pb_data_sensor_list', self._getData)
                        if ret == 1 and len(self._getData.pb_data_sensors) > 0:
                            _status_value = int(self._getData.pb_data_sensors[0].value)
                            _good_status = True
                            log.debug('[%s]当前运行状态为:%s' % (self._task.name, _status_value))
                        else:
                            log.error('获取[%s]状态[get data]失败,原因:%s' % (self._task.name, ret))
                    except Exception as e:
                        log.error('获取[%s]get data异常,原因:%s' % (self._task.name, repr(e)))

                if _good_status:
                    self._task.set_status(_status_value)
                    self._task.update_status_time(int(time.time()))
                else:
                    self._bindData = False
                    self._task.set_status(0)

    #---------------------------------------------------------------------------

    if len(tasks) > 0:
        run_tasks = []
        for tsk in tasks:
            ssts = _service_status(tsk)
            run_tasks.append(ssts)

        if len(run_tasks) > 0:
            while RUN_STATUS_MACHINE:
                for rt in run_tasks:
                    rt.refresh_service_status()
                    time.sleep(0.5)
                time.sleep(UPDATE_STATUS_CYCLE)

if __name__ == '__main__':
    import signal

    file_existed = False
    try:
        file = os.environ["richisland_home"] + '/run_config.cfg'
    except Exception as e:
        log.error('环境变量[%s]未定义,请检查...' % 'richisland_home')

    file_existed = os.path.exists(file)
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