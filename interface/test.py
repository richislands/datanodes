from functools import reduce

def filt(x):
    if x > 10:
        return True
    else:
        return False

list1 = [1,8,10,12,20]
print(list(filter(filt, list1)))

print(list(filter(lambda x: x > 10, list1)))

# def t():
#     for i in range(100, 1000):
#         if str(i)[0] == str(i)[-1]:
#             print(i)

# t()

print([x for x in range(100,1000) if str(x)[0]==str(x)[-1]])

def fit(max):
    a, b = 1, 1
    while a < max:
        yield a
        a, b = b, a+b

for n in fit(10):
    print(n)

m = fit(15)
print('first next:',next(m))
print('second next:',next(m))
print('third next:',next(m))

# t = ('hello', 'the', 'world')
# print(dir(t))

g,k,l = map(str,(1,2,3))
print(g,k,l)

# lst = list[,n for 1]

# import struct

v = "\000\000\211B"
# print(struct.unpack('!f', v)[0])
from struct import pack, unpack

float_value = 1.5
float_bytes = pack('f', float_value)
print(float_bytes)

int_value = unpack('L', float_bytes)[0]
print(int_value)

int_bytes = pack('L', int_value)
print(int_bytes)

# v_value = bytes(v,encoding='utf-8')
# print('v_value:',v_value)
# f_value = unpack('f', v_value)[0]
# print(f_value)

# eval("__import__('os').system('dir')")
from ctypes import * 
user32 = windll.LoadLibrary('user32.dll') 
user32.MessageBoxA(0, str.encode('Ctypes is so smart!'), str.encode('Ctypes'), 0)

import win32api
win32api.ShellExecute(0, 'open', 'notepad.exe', '', '', 0)           # 前台打开 

# parser = argparse.ArgumentParser(description='I print fibonacci sequence')
# parser.add_argument('-s', '--start', type=int, dest='start',
#                     help='Start of the sequence', required=True)
# parser.add_argument('-e', '--end', type=int, dest='end',
#                     help='End of the sequence', required=True)
# parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
#                     help='Enable debug info')