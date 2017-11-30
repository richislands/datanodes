#!/usr/bin/env python  
# -*- coding:utf-8 -*-  

import time  
from datetime import date, datetime, timedelta  
import platform  
import os  
import win32ui,win32api,win32con,win32gui  
import subprocess  


def install():  
    print("install psutil...")  
    sysstr = platform.system()  
    if(sysstr =="Windows"):  
        print ("Call Windows tasks")  
        bit,type=platform.architecture()  
        print ("os bit: %s "  % bit)  
        #print ("os type: %s "  % type)  
        if(bit == "64bit"):  
            fileName="psutil-3.3.0.win-amd64-py3.6.exe"
        else:  
            fileName="psutil-3.3.0.win32-py3.6.exe"
        print("will install the file [%s]" % fileName)
        
        #启动程序--4种方法
        #subprocess.Popen(fileName); #非阻塞
        #subprocess.Popen(fileName).wati(); #阻塞
        #os.system(fileName); #阻塞
        #win32api.ShellExecute(0, 'open', fileName, '','',0)
        
        label = 'Setup' #此处假设主窗口名为tt  
        hld = win32gui.FindWindow(None, label)          
        count=0  
        while (hld == 0 and count<20):  
            print("the setup is no running,will run it...")  
            count += 1  
            win32api.ShellExecute(0, 'open', fileName, '','',0)              
            print("sleep 1 seconds...")  
            time.sleep(0.5)  
            #wnd = win32ui.GetForegroundWindow()  
            #print wnd.GetWindowText()  
            hld = win32gui.FindWindow(None, label)  
            print("hld is %s" % hld)  
          
        pwin=win32ui.FindWindow(None,label)          
        print("pwin is %s" % pwin)  
        print(pwin.GetWindowText())
        print("click...")  
        button2=win32ui.FindWindowEx(pwin,None,None,'下一步(&N) >') #找到按钮   
        button2.SendMessage(win32con.BM_CLICK, 0,-1)  
        button2=win32ui.FindWindowEx(pwin,None,None,'下一步(&N) >') #找到按钮   
        button2.SendMessage(win32con.BM_CLICK, 0,-1)  
        button2=win32ui.FindWindowEx(pwin,None,None,'下一步(&N) >') #找到按钮   
        button2.SendMessage(win32con.BM_CLICK, 0,-1)  
        button2=win32ui.FindWindowEx(pwin,None,None,'完成') #找到按钮   
        button2.SendMessage(win32con.BM_CLICK, 0,-1)  
        print("install done...")  
  

        # 鼠标点击  
        #print("click...")  
        #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)   
        #time.sleep(0.1)  
        #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)  
        #time.sleep(1)  
        #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)   
        #time.sleep(0.1)  
        #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)  
        #time.sleep(1)  
        #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)   
        #time.sleep(0.1)  
        #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)  
        #time.sleep(1)  
        #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)   
        #time.sleep(0.1)  
        #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)  
          
    elif(sysstr == "Linux"):  
        print ("Call Linux tasks")  
    else:  
        print ("Other System tasks")  
          
try:  
    print("import psutil...")  
    import psutil     
except Exception as e:
    print(Exception,":",e)
    install()  
    import psutil  
  
  
    
def get_proc_by_id(pid):  
    return psutil.Process(pid)  
  
  
def get_proc_by_name(pname):  
    """ get process by name 
     
    return the first process if there are more than one 
    """  
    for proc in psutil.process_iter():  
        try:  
            if proc.name().lower() == pname.lower(): 
                return proc
        except psutil.AccessDenied:  
            pass  
        except psutil.NoSuchProcess:  
            pass  
    return None  
  
  
  
  
def getProcess(pname, day=0, hour=0, min=0, second=0):     
    # Init time  
    now = datetime.now()  
    strnow = now.strftime('%Y-%m-%d %H:%M:%S')  
    print("now:",strnow)
    # First next run time  
    period = timedelta(days=day, hours=hour, minutes=min, seconds=second)  
    next_time = now + period  
    strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')  
    print("next run time:",strnext_time)  
    while True:  
        # Get system current time  
        iter_now = datetime.now()  
        iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')        
        if str(iter_now_time) == str(strnext_time):  
            next_time = iter_now + period  
            strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')  
            print("next run time:",strnext_time)  
              
            try:  
                Process=get_proc_by_name(pname)  
            except Exception as e:  
              print(Exception,":",e)  
            if Process != None :  
                print("-------Found the process : %s" % Process.name()) 
                print("pid is (%s)" % Process.pid);  
                Cpu_usage = Process.cpu_percent(interval=1)  
                print("cpu percent is (%s)" % Cpu_usage);  
                if (100-Cpu_usage) < 0.1 :  
                    print("cpu percent larger 60,now will terminate this process !")
                    Process.terminate();  
                    Process.wait(timeout=3);  
                    continue  
                RAM_percent = Process.memory_percent()  
                print("memory percent is (%s)" % RAM_percent)
                if (60-RAM_percent) < 0.1 :  
                    print("memory percent larger 60,now will terminate this process !")
                    Process.terminate()
                    Process.wait(timeout=3)
                    continue          
                all_files = list(Process.open_files())
                print("open files size is (%d)" % len(all_files))
                if (len(all_files)>300) : 
                    print("open files size larger 300,now will terminate this process !")
                    Process.terminate()
                    Process.wait(timeout=3)
                    continue  
                Threads_Num=Process.num_threads()  
                print("threads number is (%s)" % Threads_Num) 
                if (Threads_Num>200) :  
                    print("threads number larger 200,now will terminate this process !" )
                    Process.terminate()
                    Process.wait(timeout=3)  
                    continue  
            else :  
                print ("-------No found the process : %s" % pname)
              
            continue  
  
  
  
if __name__ == '__main__':  
    print("main....")  
    getProcess("QQ.exe",second=5)  
