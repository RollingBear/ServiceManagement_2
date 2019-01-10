# -*- coding: utf-8 -*-


# 2019/1/3 0003 下午 3:19     
# dell

from tkinter import *
from tkinter import ttk

import tkinter
import ServiceOpt

'''文件地址'''
ServiceNameListAddress = "ServiceNameList.txt"
ConfigAddress = "config.txt"
RedPicAddress = "pic\RED.png"
GreenPicAddress = "pic\GREEN.png"
YellowAddress = "pic\YELLOW.png"
LogoPicAddress = "pic\LOGO.png"

'''名称'''
START = "启动"
START_ALL = "全部启动"
STOP = "停止"
STOP_ALL = "全部停止"
RE_START = "重启"
SET_START_AUTO = "打开自启"
SET_START_ALL_AUTO = "打开全部自启"
SET_START_DEMAND = "关闭自启"
SET_START_ALL_DEMAND = "关闭全部自启"
SET_START_DISABLED = "禁用服务"
SET_START_ALL_DISABLED = "禁用全部服务"
LOG_FILE = "日志"
LOG_LIST = "日志目录"

RE_FRESH_STATE = "刷新状态"

MESSAGE_TEXT = ""
SERVICE_NOT_INSTALL = "服务未安装"

BLANK_1 = " "
BLANK_2 = "  "
BLANK_3 = "   "
BLANK_4 = "    "

'''读文件'''


def readFromFile(address, type):
    File = open(address)
    if type == 1:
        result = File.read()
        File.close()
        return result
    elif type == 0:
        result = File.readlines()
        File.close()
        for count in range(len(result)):
            result[count] = result[count].replace("\n", "")
        File.close()
        return result


'''按钮'''


def printMenuButton(tk, mes, count, column):
    if ServiceOpt.getServiceState(mes) == -1:
        btn = Button(tk, text=mes, anchor='w', height=1, relief=FLAT, activeforeground="blue")
        btn.bind("<Button-1>", lambda index=None, title="错误", mes="服务未安装": ServiceOpt.createWindow(title, mes))
        btn.bind("<Enter>", lambda event: event.widget.config(fg="blue"))
        btn.bind("<Leave>", lambda event: event.widget.config(fg="black"))
        btn.grid(row=count, column=column, sticky=W)
    else:
        btn = Menubutton(tk, text=mes, anchor='w', height=1, relief=FLAT, activeforeground="blue")
        btn.grid(
            row=count, column=column, sticky=W)
        fileMenu = Menu(btn, tearoff=False)
        fileMenu.add_radiobutton(label=START, value=1, command=lambda: ServiceOpt.ServiceStart(mes))
        fileMenu.add_radiobutton(label=STOP, value=2, command=lambda: ServiceOpt.ServiceStop(mes))
        fileMenu.add_radiobutton(label=RE_START, value=3, command=lambda: ServiceOpt.ServiceReStart(mes))
        fileMenu.add_radiobutton(label=LOG_FILE, value=4,
                                 command=lambda: ServiceOpt.openNoteByName(LogFileAddress, mes))
        fileMenu.add_radiobutton(label=SET_START_AUTO, value=5,
                                 command=lambda: ServiceOpt.ServiceSetStartAuto(mes, "auto"))
        fileMenu.add_radiobutton(label=SET_START_DEMAND, value=6,
                                 command=lambda: ServiceOpt.ServiceSetStartAuto(mes, "demand"))
        fileMenu.add_radiobutton(label=SET_START_DISABLED, value=7,
                                 command=lambda: ServiceOpt.ServiceSetStartAuto(mes, "disabled"))
        btn.config(menu=fileMenu)


def printButton(tk, text, mes, row, column, columnspan):
    if text == START_ALL:
        btn = Button(tk, text=text, width=8, height=1, relief=FLAT, activeforeground="blue",
                     command=lambda List=mes: ServiceAllStart(List))
    elif text == STOP_ALL:
        btn = Button(tk, text=text, width=8, height=1, relief=FLAT, activeforeground="blue",
                     command=lambda List=mes: ServiceAllStop(List))
    elif text == LOG_LIST:
        btn = Button(tk, text=text, width=8, height=1, relief=FLAT, activeforeground="blue",
                     command=lambda: ServiceLogList())
    btn.grid(row=row, column=column, columnspan=columnspan)
    btn.bind("<Enter>", lambda event: event.widget.config(fg="blue"))
    btn.bind("<Leave>", lambda event: event.widget.config(fg="black"))


'''图片'''


def printPNG(photo, row, column, columnspan):
    label = Label(image=photo)
    label.image = photo
    label.grid_forget()
    label.grid(row=row, column=column, columnspan=columnspan)


'''标签'''


def printLabel(tk, mes, row, column, columnspan):
    Label(tk, text=mes, anchor=NW).grid(row=row, column=column, columnspan=columnspan, sticky=W)


'''按钮服务'''


def ServiceAllStart(ServiceNameList):
    for count in range(len(ServiceNameList)):
        ServiceOpt.ServiceStart(ServiceNameList[count])


def ServiceAllStop(ServiceNameList):
    for count in range(len(ServiceNameList)):
        ServiceOpt.ServiceStop(ServiceNameList[count])


def ServiceLogList():
    ServiceOpt.openFile(LogFileAddress)


'''加载服务状态'''


def ServiceState(count, column, columnspan, ServiceName):
    FLAG = ServiceOpt.getServiceState(ServiceName)
    if FLAG == 1:
        printPNG(GREEN, count, column, columnspan)
        return True
    elif FLAG == 0:
        printPNG(RED, count, column, columnspan)
        return True
    elif FLAG == -1:
        printPNG(YELLOW, count, column, columnspan)
        return False


'''状态刷新'''


def ServiceStateReFresh():
    for count in range(len(ServiceNameList)):
        ServiceState(count, 3, 1, ServiceNameList[count])
    myGui.after(800, ServiceStateReFresh)


if __name__ == '__main__':

    myGui = Tk(className="服务管理")
    myGui.resizable(width=False, height=False)

    LogFileAddress = readFromFile(ConfigAddress, 1)
    ServiceNameList = readFromFile(ServiceNameListAddress, 0)

    GREEN = PhotoImage(file=GreenPicAddress)
    RED = PhotoImage(file=RedPicAddress)
    YELLOW = PhotoImage(file=YellowAddress)
    LOGO = PhotoImage(file=LogoPicAddress)

    for count in range(len(ServiceNameList)):
        printMenuButton(myGui, ServiceNameList[count], count, 1)
        printLabel(myGui, BLANK_4, count, 2, 1)
        ServiceState(count, 3, 1, ServiceNameList[count])
        printLabel(myGui, BLANK_4 * 3, count, 4, 1)

    printLabel(myGui, BLANK_4, len(ServiceNameList) + 1, 1, 1)

    printPNG(LOGO, len(ServiceNameList) + 2, 1, 1)
    printButton(myGui, START_ALL, ServiceNameList, len(ServiceNameList) + 2, 2, 1)
    printButton(myGui, STOP_ALL, ServiceNameList, len(ServiceNameList) + 2, 3, 1)
    printButton(myGui, LOG_LIST, None, len(ServiceNameList) + 2, 4, 1)

    ServiceStateReFresh()
    myGui.mainloop()
