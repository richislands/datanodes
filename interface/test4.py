__version__ = '1.0.0'
# import sys

# def add(a, b):
#     return a + b

# def sub(a, b):
#     return a - b

# import time

# t1 = int(time.time())
# print('t1:',t1)
# time.sleep(5)
# t2 = int(time.time())
# print('t2:',t2)
# print('t2-t1:',t2-t1)

# if __name__ == '__main__':
#     for arg in sys.argv:
#         print(arg)

# import os
# import subprocess
# import win32process
# import time
# import win32api

# try:
#     #检查要启动的程序路径有效性
#     exe_path = 'F:\\aqwg\\s_rtds\\s_rtds.exe'
#     exe_params = '127.0.0.1 8888 s_rtds'

#     # os.system(command)
#     # win32api.ShellExecute(0, 'open', exe_path, exe_params, '', 1)

#     # p = subprocess.Popen([exe_path,exe_params])
#     # print(p.args)
#     # time.sleep(100)
#     # p.terminate()
#     # print('over')
    

#     # import subprocess
#     # plistexes=['start apps.exe -a','start  apps.exe -b','start  apps.exe -c']
#     # processes=[subprocess.Popen(exe,shell=True) for exe in plistexes]
#     p = subprocess.Popen(args)


# except Exception as e:
#     print('run exception: ', repr(e))

# var = 1
# def fun():
#   print(var)
#   var = 200

# fun(2)
# # print(a)

import sys
import time

sys.stdout.write('hello'+'\n') 

__console__= sys.stdout
f_handler = open('t1.txt', 'w')
sys.stdout = f_handler
print('hello world.')
sys.stdout=__console__


def test(x,y):
    a = 4
    print(locals())
    z = 3
    print(locals())

test(1,2)

globals()['__version__'] = '0.1'
print(globals()['__version__'])

import test4
# print(dir(test4))
print(globals())


print('%(age)s %(name)s' % {'name':'cw','age':38})
print('%(name)s am a hero, %()s' % {'name': 'i', '':'Yes', 'a':'bb'})

import binascii  
import struct  
  
  
def example(express, result=None):  
    if result == None:  
        result = eval(express)  
    print(express, ' ==> ', result) 

print("10进制转16进制", end=': ');example("hex(16)")
print('字节串转16进制表示,固定两个字符表示', end=": ");example(r"str(binascii.b2a_hex(b'\x01\x0212'))[2:-1]")
print('字节码解码为字符串', end=": ")
example(r"bytes(b'\x31\x32\x61\x62').decode('ascii')")
print('\n===================\n') 

for i in range(10):
    print(i, end='')

import six
print(six.int2byte(196))

import logger2
import os

path = os.path.abspath(os.curdir)
print(path)
log = logger2.logger2(logger="业务接口", log_path=path).getlog()
log.info('bacd')

import pb_data_sensor_list
s_list = pb_data_sensor_list.pb_data_sensor_list()
print(type(s_list))
print(isinstance(s_list, pb_data_sensor_list.pb_data_sensor_list))
print(True if 'pb_data_sensor_list1' in str(type(s_list)) else False)
a = 'pb_data_sensor_list'
b = str(type(s_list))
print(b)
print(str(type(s_list)).split('.')[-1][:-2])
print(True if a == str(type(s_list)).split('.')[-1][:-2] else False)

c = {'abcd':1}
print(c.__contains__('abc'))

x = '0x10102020'
print(x)
print(repr(x))
y = 1
xx = eval(str(x))
print(xx)
print(isinstance(xx,str))
# z = eval(xx)
zz = int(xx)
print(zz)

path = os.environ.get("richisland_home")
path2 = 'cba\\abc.doc'
a_path = os.path.join(path,path2)
print(a_path)