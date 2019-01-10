# -*- coding: utf-8 -*-


# 2019/1/10 0010 下午 4:38     
# RollingBear

import configparser

config = configparser.ConfigParser()
config.read("config.ini")

print(config.get("name", "ServiceName"))
print(config.get("name", "ServiceName").split(', '))