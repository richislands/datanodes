
f = open('c:/ttt1.txt')
# lines = [line for line in file]
# print(lines)

# while True:
#     l = file.readline()
#     print(l)
#     if not l:
#         break

# for line in file:
#     print(line)

# a = [l for l in file]
# print(a)
# for l in file:
#     print(len(l.split(',')))

# lines = list(filter(lambda x: len(x.split(','))>0, [l for l in file]))
# print(lines)
# file.close()
# for line in lines:
#     print(line)

lines = [''.join(line).strip('\n').split(',') for line in f if len(line.split(',')) == 4]

print(lines)
# exe, *_ = next(f)
# print(exe)
# exe, *_ = next(f)
# print(exe)
# exe, *_ = next(f)
# print(exe)
# exe, *_ = next(f)
# print(exe)

import time
import datetime
t = int(time.time())
print(time.time())
print(t)
print(time.mktime(datetime.datetime.now().timetuple()))

a = '1'
b = '2'
c = ' '.join([a,b])
print(c)
d = None
if not d:
    print(d)




def cf(l):
    l = l if isinstance(l, list) else [l]
    for i in l:
        print('%s * %s = %s' % (l[0], i, l[0] * i))
    if len(l) > 1:
        cf(l[1:])
cf([i for i in range(1,10)])


# import pb_data_sensor

# tags = []
# tag1 = pb_data_sensor.pb_data_sensor()
# tag1.name = 'FIX.F_1000.F_CV'
# tag1.size = 5
# tags.append(tag1)
# tag2 = pb_data_sensor.pb_data_sensor()
# tag2.name = 'FIX.F_981.F_CV'
# tag2.size = 1
# tags.append(tag2)
# tag3 = pb_data_sensor.pb_data_sensor()
# tag3.name = 'FIX.F_110.F_CV'
# tag3.size = 50
# tags.append(tag3)
# tag4 = pb_data_sensor.pb_data_sensor()
# tag4.name = 'FIX.F_101.F_CV'
# tag4.size = 10
# tags.append(tag4)
# tag6 = pb_data_sensor.pb_data_sensor()
# tag6.name = 'FIX.S999.A_CV'
# tag6.size = 53
# tags.append(tag6)
# tag5 = pb_data_sensor.pb_data_sensor()
# tag5.name = 'FIX.B53.F_CV'
# tag5.size = 13
# tags.append(tag5)

# print([v.name for v in tags])
# print('=' * 50)
# from operator import attrgetter
# tags2 = sorted(tags, key=attrgetter('name'))
# print(tags2)
b = 'aaa'
c = str(b)
a = str(0x02010302)
print(int(a,16))

def OnlyCharNum(s,oth=''):
    s2 = s.lower();
    fomart = 'abcdefghijklmnopqrstuvwxyz0123456789'
    for c in s2:
        if not c in fomart:
            s = s.replace(c,'');
    return s;

from enum import Enum

EXCEPT_HEAD = '0x0201'

SERVICE_STATUS = Enum('SERVICE_STATUS', ('NONE','CONFIG','RUN','ERROR'))

FUNCTIONS = Enum('FUNCTIONS', ('BIND_SERVICE','BIND_CONFIG','START','BIND_DATA',\
    'GET_DATA', 'SET_DATA', 'STOP', 'DISPOSE'))

EXCEPTIONS = Enum('EXCEPTIONS', ('INPUT_PARAMS_ERROR','NET_COMM_ERROR','GET_STATUS_ERROR','NOT_BIND_CONFIG',\
    'HAVE_BIND_CONFIG', 'NOT_START', 'HAVE_START', 'APP_ERROR', 'RTN_ERROR'))

EXCEPTIONS_REMARK = {
EXCEPTIONS.INPUT_PARAMS_ERROR:'输入参数异常',\
EXCEPTIONS.NET_COMM_ERROR:'网络通信异常',\
EXCEPTIONS.GET_STATUS_ERROR:'获取状态异常',\
EXCEPTIONS.NOT_BIND_CONFIG:'节点未配置',\
EXCEPTIONS.HAVE_BIND_CONFIG:'节点已配置',\
EXCEPTIONS.NOT_START:'节点未运行',\
EXCEPTIONS.HAVE_START:'节点正在运行',\
EXCEPTIONS.APP_ERROR:'节点状态异常',\
EXCEPTIONS.RTN_ERROR:'节点返回异常',\
}

fun_err_dict = {
    FUNCTIONS.BIND_SERVICE:[EXCEPTIONS.INPUT_PARAMS_ERROR],
    ########################################################
    FUNCTIONS.BIND_CONFIG:[EXCEPTIONS.INPUT_PARAMS_ERROR, EXCEPTIONS.NET_COMM_ERROR, 
    EXCEPTIONS.GET_STATUS_ERROR, EXCEPTIONS.HAVE_BIND_CONFIG, EXCEPTIONS.HAVE_START,
    EXCEPTIONS.APP_ERROR, EXCEPTIONS.RTN_ERROR],
    ########################################################
    FUNCTIONS.START:[EXCEPTIONS.INPUT_PARAMS_ERROR, EXCEPTIONS.NET_COMM_ERROR,
    EXCEPTIONS.GET_STATUS_ERROR, EXCEPTIONS.NOT_BIND_CONFIG, EXCEPTIONS.HAVE_START,
    EXCEPTIONS.APP_ERROR, EXCEPTIONS.RTN_ERROR],
    ########################################################
    FUNCTIONS.STOP:[EXCEPTIONS.INPUT_PARAMS_ERROR, EXCEPTIONS.NET_COMM_ERROR,
    EXCEPTIONS.GET_STATUS_ERROR, EXCEPTIONS.NOT_START, EXCEPTIONS.APP_ERROR, EXCEPTIONS.RTN_ERROR],
    ########################################################
    FUNCTIONS.DISPOSE:[EXCEPTIONS.INPUT_PARAMS_ERROR, EXCEPTIONS.NET_COMM_ERROR,
    EXCEPTIONS.GET_STATUS_ERROR, EXCEPTIONS.HAVE_START, EXCEPTIONS.APP_ERROR, EXCEPTIONS.RTN_ERROR],
    ########################################################
    FUNCTIONS.BIND_DATA:[EXCEPTIONS.INPUT_PARAMS_ERROR, EXCEPTIONS.NET_COMM_ERROR,
    EXCEPTIONS.GET_STATUS_ERROR, EXCEPTIONS.NOT_BIND_CONFIG, EXCEPTIONS.APP_ERROR, EXCEPTIONS.RTN_ERROR],
    ########################################################
    FUNCTIONS.GET_DATA:[EXCEPTIONS.INPUT_PARAMS_ERROR, EXCEPTIONS.NET_COMM_ERROR,
    EXCEPTIONS.GET_STATUS_ERROR, EXCEPTIONS.NOT_BIND_CONFIG, EXCEPTIONS.NOT_START, EXCEPTIONS.APP_ERROR, EXCEPTIONS.RTN_ERROR],
    ########################################################
    FUNCTIONS.SET_DATA:[EXCEPTIONS.INPUT_PARAMS_ERROR, EXCEPTIONS.NET_COMM_ERROR,
    EXCEPTIONS.GET_STATUS_ERROR, EXCEPTIONS.NOT_BIND_CONFIG, EXCEPTIONS.NOT_START, EXCEPTIONS.APP_ERROR, EXCEPTIONS.RTN_ERROR],
}

import operator
from struct import pack, unpack
import binascii  

except_dict = {}

# sorted(fun_err_dict.items(), key=lambda x:x.member)
for (key, value) in fun_err_dict.items():
    list_name = {int('%s%s%s' % (EXCEPT_HEAD, '%02d' % key.value, '%02d' % func.value),16): '%s异常,原因:%s'%(key.name,EXCEPTIONS_REMARK[func]) for func in value }
    for (k,v) in list_name.items():
        except_dict[k] = v

list_names = [key for key in except_dict]
print(list_names)
print('---------------------')
print(list(map(lambda x:pack('L', x), sorted(except_dict.keys()))))
print(list(map(lambda x:'0x%s' % str(binascii.b2a_hex(pack('>L', x)))[2:-1], sorted(except_dict.keys()))))
print('---------------------')
# print(sorted(except_dict.items()))
print('---------------------')
# print(['%s -------- %s' % (hex(item[0]),item[1]) for item in sorted(except_dict.items())])
print('---------------------')
# sorted(except_dict.items(),key = lambda x:x[0], reverse = False)
# print(except_dict)


# for name, member in EXCEPTIONS.__members__.items():
#     print(name, '=>', member, ',', member.value)

# file = 'c:/exception_dict.txt'
# with open(file,'w') as f:
#     f.writelines(['%s -------- %s\n' % (hex(item[0]),item[1]) for item in sorted(except_dict.items())])

import data_service_interface as dsif

ip = '192.168.28.42'
port = 41009

ret = dsif.bindService(ip, port, 's_rtds', 'rtds')
print('bindService return:',ret)

# ret = dsif.getStatusTest('rtds')
# print(int(ret))

# dsif.createExceptionDictory('c:/inteface_exception.txt')
a = '000001'
b = int(a)
print(b)

import os
print(os.path.abspath(os.curdir))

# import test4
# print(dir(test4))



