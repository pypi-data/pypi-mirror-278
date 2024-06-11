import hashlib
import random
import json
from datetime import datetime, timedelta
import uuid
from dateutil.relativedelta import relativedelta
import os


def randomxx(a, b):
    return random.uniform(a, b)


def writeText(path, dataList):
    file = open(path, "w")
    for s in dataList:
        file.write(s + '\n')
    file.close()


def writePfText(path, dataList):
    file = open(path, "w")
    for s in dataList:
        req = json.loads(s['req'])
        file.write(req[0] + '\n')
    file.close()


def writePfTextOne(path, text):
    file = open(path, "a")
    file.write(text + '\n')
    file.close()


def writeLog(text):
    print(text)
    # 检查文件是否存在
    file_path = f"D:/logs/python/python-log{get_now_time('%Y%m%d')}.log"
    if os.path.exists(file_path):
        file = open(file_path, "a")
        file.write(text + '\n')
        file.close()


def readText(path):
    data = []
    with open(path, 'r') as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            # print(line)
            if index != 0:
                data.append(line.replace('\n', ''))
    return data


def isEmpty(s):
    if s is None:
        return True
    elif not s:
        return True
    elif s.strip() == "":
        return True
    else:
        return False


def isEmptyObject(s):
    if s is None:
        return True
    else:
        return False


def md5_hash(input_string):
    # 创建一个md5对象
    hash_object = hashlib.md5(input_string.encode())
    # 获取md5哈希的16进制字符串表示
    hex_dig = hash_object.hexdigest()
    return hex_dig


def get_now_time(format='%Y-%m-%d %H:%M:%S'):
    if format == '' or format == None:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        return datetime.now().strftime(format)


def bu_zero(s, num):
    return str(s).zfill(num)


def get_timestamp():
    return int(datetime.datetime.now().timestamp())


def get_time_by_day(format, day=0):
    if day == '' or day == None:
        day = 0
    # 当前日期
    current_date = datetime.now()
    # 计算前day天的日期
    five_days_ago = current_date + timedelta(days=day)
    if format == '' or format == None:
        return five_days_ago.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return five_days_ago.strftime(format)

def get_time_by_month(format, month=0):
    if month == '' or month == None:
        month = 0
    # 当前日期
    current_date = datetime.now()
    # 计算前day天的日期
    five_days_ago = current_date + relativedelta(months=month)
    if format == '' or format == None:
        return five_days_ago.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return five_days_ago.strftime(format)

def uuid4(replace=""):
    return str(uuid.uuid4()).replace("-", replace)
