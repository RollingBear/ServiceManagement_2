# -*- coding: utf-8 -*-


# 2019/1/10 0010 下午 4:38     
# RollingBear

import configparser
import os
import sys

# config = configparser.ConfigParser()
# config.read("config.ini")
#
# print(config.get("name", "ServiceName"))
# print(config.get("name", "ServiceName").split(', '))

Address = "Done\pack\pack"
test = "..\..\..\pack"
test2 = "..\..\pack"
test3 = "..\pack"

# now = os.getcwd()
# print(now)
# father = os.path.abspath(os.path.dirname(now)+os.path.sep+".")
# print(father)
# grand = os.path.abspath(os.path.dirname(now)+os.path.sep+"..")
# print(grand)
# os.popen("start " + os.path.abspath(os.path.dirname(now)+os.path.sep+"..") + Address)

print(test.count("..\\"))
print(test2.count("..\\"))
print(test3.count("..\\"))
print(test.replace("..\\", ""))
print("~" * test.count("..\\") + test.replace("..\\", ""))
Address_test = "..\..\Done\pack\pack"

# os.popen("start " + os.path.abspath(
#     os.path.dirname(os.getcwd()) + os.path.sep + ("." * Address_test.count("..\\"))) + "\\" + Address_test.replace("..\\",
#                                                                                                                  ""))

os.popen("start " + os.path.abspath(Address_test))