# -*- coding: utf-8 -*-


# 2019/1/3 0003 下午 3:19     
# RollingBear

from tkinter import *
import ServiceOpt
import configparser
import time
import _thread

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

SERVICE_NOT_INSTALL = "服务未安装"


BLANK_1 = " "
BLANK_2 = "  "
BLANK_3 = "   "
BLANK_4 = "    "

'''读取配置文件'''


def loadCONF():
    global LogListAddress, RedPicAddress, GreenPicAddress, YellowPicAddress, LogoPicAddress, ServiceNameList

    config = configparser.ConfigParser()
    config.read("config.ini")

    LogListAddress = config.get("address", "LogListAddress")
    RedPicAddress = config.get("address", "RedPicAddress")
    GreenPicAddress = config.get("address", "GreenPicAddress")
    YellowPicAddress = config.get("address", "YellowPicAddress")
    LogoPicAddress = config.get("address", "LogoPicAddress")

    file = open(config.get("address", "NameListAddress"), encoding="utf-8-sig")
    ServiceNameList = []
    result = file.readlines()
    for count in range(len(result)):
        result[count] = result[count].replace("\n", "")
        result_1 = result[count].split(",")
        ServiceNameList.append(result_1[0])
        ServiceNameList.append(result_1[1])


'''按钮'''


def printMenuButton(tk, text, mes, count, column):
    if ServiceOpt.getServiceState(mes) == -1:
        btn = Button(tk, text=text, anchor='w', height=1, relief=FLAT, activeforeground="blue")
        btn.bind("<Button-1>", lambda index=None, title="错误", mes="服务未安装": ServiceOpt.createWindow(title, mes))
        btn.bind("<Enter>", lambda event: event.widget.config(fg="blue"))
        btn.bind("<Leave>", lambda event: event.widget.config(fg="black"))
        btn.grid(row=count, column=column, sticky=W)
    else:
        btn = Menubutton(tk, text=text, anchor='w', height=1, relief=FLAT, activeforeground="blue")
        btn.grid(
            row=count, column=column, sticky=W)
        fileMenu = Menu(btn, tearoff=False)
        fileMenu.add_radiobutton(label=START, value=1, command=lambda: ServiceOpt.ServiceStart(mes))
        fileMenu.add_radiobutton(label=STOP, value=2, command=lambda: ServiceOpt.ServiceStop(mes))
        fileMenu.add_radiobutton(label=RE_START, value=3, command=lambda: ServiceOpt.ServiceReStart(mes))
        fileMenu.add_radiobutton(label=LOG_FILE, value=4,
                                 command=lambda: ServiceOpt.openNoteByName(LogListAddress, mes))
        fileMenu.add_radiobutton(label=SET_START_AUTO, value=5,
                                 command=lambda: ServiceOpt.ServiceSetStartAuto(mes, "auto"))
        fileMenu.add_radiobutton(label=SET_START_DEMAND, value=6,
                                 command=lambda: ServiceOpt.ServiceSetStartAuto(mes, "demand"))
        fileMenu.add_radiobutton(label=SET_START_DISABLED, value=7,
                                 command=lambda: ServiceOpt.ServiceSetStartAuto(mes, "disabled"))
        btn.config(menu=fileMenu)


def printButton(tk, text, mes, row, column, columnspan):
    if text == START_ALL:
        btn = Button(tk, text=text, width=8, height=1, activeforeground="blue",
                     command=lambda List=mes: ServiceAllStart(List))
    elif text == STOP_ALL:
        btn = Button(tk, text=text, width=8, height=1, activeforeground="blue",
                     command=lambda List=mes: ServiceAllStop(List))
    elif text == LOG_LIST:
        btn = Button(tk, text=text, width=8, height=1, activeforeground="blue",
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


def printLabel(tk, mes, row, column, columnspan, sticky=W):
    Label(tk, text=mes, anchor=NW).grid(row=row, column=column, columnspan=columnspan, sticky=sticky)


'''按钮服务'''


def ServiceAllStart(ServiceNameList):
    for count in range(int(len(ServiceNameList) / 2)):
        ServiceOpt.ServiceStart(ServiceNameList[int(count * 2)])
        ServiceState(count, 3, 1, ServiceNameList[int(count * 2)])


def ServiceAllStop(ServiceNameList):
    for count in range(int(len(ServiceNameList) / 2)):
        ServiceOpt.ServiceStop(ServiceNameList[int(count * 2)])
        ServiceState(count, 3, 1, ServiceNameList[int(count * 2)])


def ServiceLogList():
    ServiceOpt.openFile(LogListAddress)


'''加载服务状态'''


def ServiceState(tk, count, column, columnspan, ServiceName):
    FLAG = ServiceOpt.getServiceState(ServiceName)
    if FLAG == 1:
        printPNG(GREEN, count, column, columnspan)
        printLabel(tk, "已启动", count, column + 1, columnspan)
        return True
    elif FLAG == 0:
        printPNG(RED, count, column, columnspan)
        printLabel(tk, "未启动", count, column + 1, columnspan)
        return True
    elif FLAG == -1:
        printPNG(YELLOW, count, column, columnspan)
        printLabel(tk, "未安装", count, column + 1, columnspan)
        return False


'''状态刷新'''


def ReFreshThread(tk, ServiceNameList, delay):
    while True:
        for count in range(int(len(ServiceNameList) / 2)):
            ServiceState(tk, count, 3, 1, ServiceNameList[int(count * 2)])
        time.sleep(delay)


'''启动服务'''


def start():
    global myGui, ServiceNameList, GREEN, RED, YELLOW, LOGO
    myGui = Tk(className="服务管理")
    myGui.withdraw()
    myGui.resizable(width=False, height=False)

    GREEN = PhotoImage(file=GreenPicAddress)
    RED = PhotoImage(file=RedPicAddress)
    YELLOW = PhotoImage(file=YellowPicAddress)
    LOGO = PhotoImage(file=LogoPicAddress)

    for count in range(int(len(ServiceNameList) / 2)):
        printMenuButton(myGui, ServiceNameList[int(count * 2 + 1)], ServiceNameList[int(count * 2)], count, 1)
        ServiceState(myGui, count, 3, 1, ServiceNameList[int(count * 2)])

    printLabel(myGui, BLANK_4, int(len(ServiceNameList) / 2) + 1, 1, 1)

    printPNG(LOGO, int(len(ServiceNameList) / 2) + 2, 1, 1)
    printButton(myGui, START_ALL, ServiceNameList, int(len(ServiceNameList) / 2) + 2, 2, 1)
    printButton(myGui, STOP_ALL, ServiceNameList, int(len(ServiceNameList) / 2) + 2, 3, 1)
    printButton(myGui, LOG_LIST, None, int(len(ServiceNameList) / 2) + 2, 4, 1)

    try:
        _thread.start_new_thread(ReFreshThread, (myGui, ServiceNameList, 2))
    except:
        print('Thread start Error')

    myGui.update_idletasks()

    SetX = (myGui.winfo_screenwidth() - myGui.winfo_reqwidth()) / 2
    SetY = (myGui.winfo_screenheight() - myGui.winfo_reqheight()) / 2
    myGui.geometry("%dx%d+%d+%d" % (myGui.winfo_reqwidth() + 8, myGui.winfo_reqheight(), SetX, SetY))
    myGui.deiconify()
    myGui.mainloop()


if __name__ == '__main__':
    loadCONF()
    start()
