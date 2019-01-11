# -*- coding: utf-8 -*-


# 2019/1/3 0003 下午 3:19     
# RollingBear

import os
import time
from tkinter.messagebox import showinfo

'''查询服务状态'''


def getServiceState(ServiceName):
    result = os.popen("sc query " + ServiceName).read()

    if "RUNNING" in result:
        return 1
    elif "START_PENDING" in result:
        return 1
    elif "STOPPED" in result:
        return 0
    elif "STOP_PENDING" in result:
        return 0
    elif "1060" in result:
        return -1


'''启动服务'''


def ServiceStart(ServiceName):
    result = os.popen("sc start " + ServiceName).read()

    if "1058" in result:
        createWindow("错误", "服务已被禁用")


'''停止服务'''


def ServiceStop(ServiceName):
    result = os.popen("sc stop " + ServiceName).read()

    if "1058" in result:
        createWindow("错误", "服务已被禁用")


'''重启服务'''


def ServiceReStart(ServiceName):
    ServiceStop(ServiceName)
    time.sleep(1)
    result = ServiceStart(ServiceName).read()

    if "1058" in result:
        createWindow("错误", "服务已被禁用")


'''打开、关闭开机自启'''


def ServiceSetStartAuto(ServiceName, State):
    os.popen("sc config " + ServiceName + " start=" + State)


'''打开记事本'''


def openNoteByName(LogAddress, ServiceName):
    os.system("notepad " + LogAddress + "\\" + ServiceName + ".log")


'''打开文件夹'''


def openFile(Address):
    os.popen("start " + os.path.abspath(Address))


'''弹窗'''


def createWindow(title, mes):
    showinfo(title, mes)
