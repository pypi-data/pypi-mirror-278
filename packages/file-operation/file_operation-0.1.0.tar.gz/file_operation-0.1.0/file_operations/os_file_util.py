#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:skyoceanchen
# project_name:chengduairport
# py_name :processing_txt
# software: PyCharm
# datetime:2021/3/3 13:45
"""文件类工具"""
import datetime as dt
import glob
import linecache
import math
import os
import platform
import time
from pathlib import Path
from shutil import copy2, rmtree

import pandas as pd
from basic_type_operations.date_operation import DateOperation
from pywintypes import Time  # 可以忽视这个 Time 报错（运行程序还是没问题的）
from win32file import CreateFile, SetFileTime, CloseHandle
from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING


class FileBasicOperation(object):
    # <editor-fold desc="删除文件或者文件夹">
    def remove_path(self, path):
        """
        :param path: 文件或者文件夹路径,文件架空不空都强删
        :return:
         os.remove#删除文件
        os.rmdir#删除文件夹（只能删除空文件夹）
        os.removedirs#移除目录(必须是空目录)
        shutil.rmtree#删除文件夹
        """
        if os.path.isfile(path):
            os.remove(path)
        else:
            rmtree(path)

    def delete(self, path):
        FileBasicOperation().remove_path(path)

    # </editor-fold>
    # <editor-fold desc="创建文件夹">
    def makedirs(self, path):
        path_obj = Path(path)
        if not path_obj.suffix and not path_obj.exists():
            path_obj.absolute().mkdir(parents=True)
        elif path_obj.suffix and not path_obj.absolute().parent.exists():
            path_obj.absolute().parent.mkdir(parents=True)
        return path_obj.absolute()

    # </editor-fold>
    # <editor-fold desc="获取桌面路径">
    # 这样做的好处是可以把数据放在桌面上，在不同的电脑上都能调用代码对数据进行处理。
    # 如果是在一条电脑上把桌面路径固定在字符串中，则换一台电脑就必须修改桌面路径。
    def get_desktop_path(self, ):
        return os.path.join(os.path.expanduser("~"), 'Desktop')

    # </editor-fold>
    # <editor-fold desc="获取文件的大小,结果保留两位小数，单位为MB">
    @staticmethod
    def file_size(file):
        fsize = os.path.getsize(file)
        fsize = fsize / float(1024 * 1024)
        return round(fsize, 2)

    # </editor-fold>
    # <editor-fold desc="获取文件的访问时间">
    @staticmethod
    def file_access_time(file):
        t = os.path.getatime(file)
        return DateOperation.TimeStampToTime(t)

    # </editor-fold>
    # <editor-fold desc="获取文件的创建时间">
    @staticmethod
    def file_create_time(file):
        t = os.path.getctime(file)
        return DateOperation.TimeStampToTime(t)

    # </editor-fold>
    # <editor-fold desc="获取文件的修改时间">
    @staticmethod
    def file_modify_time(file):
        t = os.path.getmtime(file)
        return DateOperation.TimeStampToTime(t)

    # </editor-fold>
    # <editor-fold desc="获取文件时间">
    def get_file_time(self, file):
        from win32file import CreateFile, GetFileTime, CloseHandle
        from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
        fh = CreateFile(file, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
        createTimes, accessTimes, modifyTimes = GetFileTime(fh)
        CloseHandle(fh)
        return createTimes, accessTimes, modifyTimes

    # </editor-fold>
    # <editor-fold desc="修改文件时间">
    def modify_file_time(self, file, create_time=None, modify_time=None, access_time=None, offset=(0, 0, 0),
                         format="%Y-%m-%d %H:%M:%S"):

        if not create_time:
            create_time = FileBasicOperation.file_create_time(file)
        if not modify_time:
            modify_time = FileBasicOperation.file_modify_time(file)
        if not access_time:
            access_time = FileBasicOperation.file_access_time(file)
        fh = CreateFile(file, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
        createTimes = Time(time.mktime(DateOperation().timeOffsetAndStruct(create_time, format, offset[0])))
        modifyTimes = Time(time.mktime(DateOperation().timeOffsetAndStruct(modify_time, format, offset[1])))
        accessTimes = Time(time.mktime(DateOperation().timeOffsetAndStruct(access_time, format, offset[2])))
        SetFileTime(fh, createTimes, accessTimes, modifyTimes)
        CloseHandle(fh)

    # </editor-fold>
    # <editor-fold desc="获取文件某一行/文件内容">
    @staticmethod
    def getlines(file, line=None):
        """
        :param file: 目标文件
        :param line: 行
        :return:
        """
        if not line:
            return linecache.getline(file, line)
        else:
            return linecache.getlines(file)

    # </editor-fold>
    # <editor-fold desc="读取文件最后n行">
    @staticmethod
    def get_last_lines(file, n):
        blk_size_max = 4096
        n_lines = []
        with open(file, 'rb') as fp:
            fp.seek(0, os.SEEK_END)
            cur_pos = fp.tell()
            while cur_pos > 0 and len(n_lines) < n:
                blk_size = min(blk_size_max, cur_pos)
                fp.seek(cur_pos - blk_size, os.SEEK_SET)
                blk_data = fp.read(blk_size)
                assert len(blk_data) == blk_size
                lines = blk_data.decode().split('\r\n')
                # adjust cur_pos
                if len(lines) > 1 and len(lines[0]) > 0:
                    n_lines[0:0] = lines[1:]
                    cur_pos -= (blk_size - len(lines[0]))
                else:
                    n_lines[0:0] = lines
                    cur_pos -= blk_size
                fp.seek(cur_pos, os.SEEK_SET)
        if len(n_lines) > 0 and len(n_lines[-1]) == 0:
            del n_lines[-1]
        return n_lines[-n:]

    # </editor-fold>
    # <editor-fold desc="扫描输出所有的子目录（子文件夹）">
    # 扫描输出所有的子目录（子文件夹）
    # 使用os.walk输出某个目录下的所有文件   er
    @staticmethod
    def dir_son_names(dir_path):
        """
        :param dir_path: 目标文件夹
        :return:
        """
        lis = list()
        for curDir, dirs, files in os.walk(dir_path):
            """
            print("现在的目录：", curDir)
            print("该目录下包含的子目录：", str(dirs))
            print("该目录下包含的文件：", str(files))
            """
            for _dir in dirs:
                lis.append(os.path.join(curDir, _dir))
        return lis

    # </editor-fold>
    # <editor-fold desc="输出所有文件">
    # 扫描输出所有文件的路径
    @staticmethod
    def file_paths(dir_path):
        """

        :param dir_path: 目标文件夹
        :return:
        """
        lis = list()
        for curDir, dirs, files in os.walk(dir_path):
            for file in files:
                lis.append(os.path.join(curDir, file))
        return lis

    # </editor-fold>
    # <editor-fold desc="输出指定类型文件">
    @staticmethod
    def file_endswith_path(dir_path, endswith):
        """

        :param dir_path:目录地址
        :param endswith: 文件结尾
        :return:
        """
        lis = list()
        for curDir, dirs, files in os.walk(dir_path):
            lis.append([os.path.join(curDir, file) for file in files if file.endswith(endswith)])
        res = (x for j in lis for x in j)
        return list(res)

    # </editor-fold>
    # <editor-fold desc="文件去重-相同日期文件">
    @staticmethod
    def file_qch_date(dir_path):
        wj_names = os.listdir(dir_path)
        wj_list = []
        num = 0
        for wj in wj_names:
            new_wj = wj[:-11]
            if new_wj not in wj_list:
                wj_list.append(new_wj)
            else:
                os.remove(dir_path + "\\" + wj)
                num += 1
        return num

    # </editor-fold>
    # <editor-fold desc="找指定时间段条件的文件">
    @staticmethod
    def file_move(dir_path, start_date, end_date):
        # 本文件移动至对应新建文件夹，非本月文件直接删除
        """
        :param file_dir_path: 目标文件夹
        :return:
        """
        # # 日期格式：xxxx-xx eg:2020-07-01
        # # 生成日期区间-字符串类型
        date_xl_str = [str(i)[:10] for i in pd.date_range(start_date, end_date, freq='D')]
        # # # 创建指定文件夹
        _new_dir_path = os.getcwd() + '\\' + start_date + "~" + end_date
        try:
            os.mkdir(_new_dir_path)
        except:
            pass
        # time_data = []
        for curDir, dirs, files in os.walk(dir_path):
            for file in files:
                old_dir_path = os.path.join(curDir, file)
                # time_data.append(str(time.strftime("%Y-%m-%d", time.localtime(os.path.getctime(old_dir_path)))))
                new_dir_path = os.path.join(_new_dir_path, file)
                # file_date = file.split("_")[-1][:10]
                # 文件创建时间
                file_date = str(time.strftime("%Y-%m-%d", time.localtime(os.path.getctime(old_dir_path))))
                # print(old_dir_path, '*******', new_dir_path, '*******', file_date)
                try:
                    # os.rename(old_dir_path, new_dir_path) if file_date in date_xl_str else os.remove(old_dir_path)
                    if file_date in date_xl_str:
                        # os.rename(old_dir_path, new_dir_path)  # 把文件移动到另外一个文件夹
                        copy2(old_dir_path, new_dir_path)
                except Exception as e:
                    # os.remove(old_dir_path)
                    pass

    # </editor-fold>
    # <editor-fold desc="文件或者文件夹-重新命名">
    @staticmethod
    def path_renames(old_path_name, new_path_name):
        # os.rename(old_file_path, new_file_path)# 只能对相应的文件进行重命名, 不能重命名文件的上级目录名.
        try:
            # 是os.rename的升级版, 既可以重命名文件, 也可以重命名文件的上级目录名
            os.renames(old_path_name, new_path_name)
            return True
        except Exception as e:
            return False

    # </editor-fold>
    # <editor-fold desc="创建具有顺序的文件夹或者文件">
    @staticmethod
    def file_number(cap_num, path_name_end=None, to_dir=None):
        """
        :param cap_num:创建个数
        :param path_name_end: 文件的后缀名 如txt, 不传创建文件夹
        :param to_dir: 存储路径
        :return:
        """
        try:
            cap_num_t = cap_num
            cap_count = 0
            while cap_num:
                cap_count = cap_count + 1
                cap_num = math.floor(cap_num / 10)
            fix = '%0' + str(cap_count) + 'd'  # 得到图片保存的前缀，比如001.png，0001.png
            cap_cnt = 1
            if not os.path.exists(to_dir):
                os.makedirs(to_dir)
            while cap_num_t:
                if path_name_end:
                    if to_dir:
                        path = os.path.join(to_dir, str(fix % cap_cnt) + '.' + path_name_end)
                    else:
                        path = str(fix % cap_cnt) + '.' + path_name_end
                    with open(path, mode="w", encoding="utf-8") as f:  # 写文件,当文件不存在时,就直接创建此文件
                        pass
                else:
                    if to_dir:
                        path = os.path.join(to_dir, str(fix % cap_cnt))
                    else:
                        path = str(fix % cap_cnt)
                    os.makedirs(path)
                cap_cnt = cap_cnt + 1
                cap_num_t -= 1
            return True
        except Exception as e:
            return False

    # </editor-fold>
    # <editor-fold desc="生成以时间戳和文件名称命名的文件或文件夹">
    @staticmethod
    def file_datetime(name_start=None, to_Dir=None):
        """
        :param name_start: 文件名或者文件名称 a.txt a
        :param rootDir: 存储路径
        :return:
        """
        name_end = None
        if '.' in name_start:
            name_end = name_start.split('.')[1]
            name_start = name_start.split('.')[0]
        date = dt.datetime.now().strftime('%Y%m%d%H%M%S%f')
        if name_end:
            if to_Dir:
                path = os.path.join(to_Dir, str(name_start) + str(date) + '.' + name_end)
            else:
                path = str(name_start) + str(date) + '.' + name_end
            f = open(path, 'w')
            f.close()
        else:
            if name_start:
                if to_Dir:
                    path = os.path.join(to_Dir, str(name_start) + str(date))
                else:
                    path = str(name_start) + str(date)
            else:
                if to_Dir:
                    path = os.path.join(to_Dir, str(date))
                else:
                    path = str(date)
            os.mkdir(path)
        return path

    # </editor-fold>
    # <editor-fold desc="过滤指定文件">
    @staticmethod
    def filter_files(file_list, endswith):
        def is_index(n):
            if n.endswith(endswith):
                return n

        file_list = list(filter(is_index, file_list))
        return file_list

    # </editor-fold>
    # <editor-fold desc="文件排序">
    @staticmethod
    def file_sort_absolute(dir_path, endswith):
        """
        :param path:文件位置
        :param endswith: 文件以什么结尾比如py，xls,word,txt等
        :param absolute: True是返回绝对路径，Flase是返回相对路径
        :return: 列表内都是文件的绝对路径
        """
        file_list = os.listdir(dir_path)
        length = len(endswith) + 1
        file_list = FileBasicOperation.filter_files(file_list, endswith)
        file_list.sort(key=lambda x: int(x[:-length]) if x.endswith(endswith) else False)
        file_list = [os.path.join(dir_path, i) for i in file_list]
        return file_list

    # </editor-fold>
    # <editor-fold desc="不全是num的文件数字排序">
    @staticmethod
    def file_other_sort(dir_path, endswith, split=None, location=None):
        """
        :param path:文件位置
        :param endswith: 文件以什么结尾比如py，xls,word,txt等
        :param split: split 右边是数字
        :param location:
        需要配合 split进行使用
        right 右边是数字 left 左边是数字
        1 拆分后索引1的位置是数字，2 拆分后索引2的位置是数字 .。。
        ‘create’ 按照文件创建时间进行排序
        ‘modify’ 按照文件修改时间进行排序
        ‘access’ 按照文件访问时间进行排序
        None 默认排序
        :param absolute: True是返回绝对路径，Flase是返回相对路径
        :return: 列表内都是文件的绝对路径
        """
        file_list = os.listdir(dir_path)
        file_list = FileBasicOperation.filter_files(file_list, endswith)
        length = len(endswith) + 1
        if split:
            if location not in ['right', "left", "create", "modify", "access", None] and not isinstance(location, int):
                raise ValueError(f"location not value {location}")
            if location == None:
                location = "create"
            if location in ["create", "modify", "access", ]:
                file_list = [os.path.join(dir_path, i) for i in file_list]
                if location == "create":
                    file_list.sort(
                        key=lambda x: FileBasicOperation.file_create_time(x) if x.endswith(endswith) else False)
                elif location == "modify":
                    file_list.sort(
                        key=lambda x: FileBasicOperation.file_modify_time(x) if x.endswith(endswith) else False)
                elif location == "access":
                    file_list.sort(
                        key=lambda x: FileBasicOperation.file_modify_time(x) if x.endswith(endswith) else False)
                return file_list
            elif location == "right":
                file_list.sort(key=lambda x: int(x[:-length].split(split)[-1]) if x.endswith(endswith) else False)
            elif location == "left":
                file_list.sort(key=lambda x: int(x[:-length].split(split)[0]) if x.endswith(endswith) else False)
            elif isinstance(location, int):
                file_list.sort(key=lambda x: int(x[:-length].split(split)[location]) if x.endswith(endswith) else False)
        else:
            file_list.sort(key=lambda x: x if x.endswith(endswith) else False)
        file_list = [os.path.join(dir_path, i) for i in file_list]
        return file_list

    # </editor-fold>
    # <editor-fold desc="文件夹数字排序">
    @staticmethod
    def dir_num_sort(dir_path, absolute=True):
        """

        :param dir_path: 文件位置
        :param absolute: 返回绝对位置
        :return:
        """
        rootpath = os.listdir(dir_path)
        rootpath = [dir_path for dir_path in rootpath if '.' not in dir_path]
        rootpath.sort(key=lambda x: int(x))
        if absolute:
            rootpath = [dir_path + '\\' + i for i in rootpath]
        return rootpath

    # </editor-fold>
    # <editor-fold desc="文件移动到另外一个问价夹内">
    @staticmethod
    def files_move(file, to_dir):
        """
        :param path:文件地址
        :param to_dir: 存储文件夹
        :return:
        """
        try:
            copy2(file, to_dir)
            # 将目标文件移动到目标文件夹里，
            # shutil.move(r'.\practice.txt', r'.\文件夹1/')
            # 将目标文件移动到目标文件夹里的同时，能够对其进行重命名
            # shutil.move(r'.\practice.txt', r'.\文件夹1/new.txt')
            # 如果我们需要移动某个或某些文件到新的文件夹，并且需重命名文件，
            # 则我们并不需要用 os.rename 先命名文件再用
            # shutil.move 将其移动的指定文件夹，而是可以用 shutil.move 一步到位
            return True
        except Exception as e:
            return False

    # </editor-fold>
    # <editor-fold desc="文件批量改名">
    @staticmethod
    def file_many_rename(dir_path, endswith):
        """

        :param dir_path:目录地址
        :param endswith: 文件结尾
        :return:
        """
        lis = list()
        for curDir, dirs, files in os.walk(dir_path):
            lis.append([os.path.join(curDir, file) for file in files if
                        file.endswith(endswith)
                        ]
                       )
        res = (x for j in lis for x in j)
        lisdir = list(res)
        fileNum = len(str(len(lisdir)))
        formatting_new = '%0' + str(fileNum) + 'd'
        for index, i in enumerate(lisdir):
            to_pa = i
            new = formatting_new % (index + 1)
            path = '\\'.join(i.split('\\')[:-1])
            file_name: str = i.split('\\')[-1]
            file_before = file_name.split('.')[0]
            if file_before.strip('0').isdigit():
                new_i = new + '.' + endswith
                new_path = os.path.join(path, new_i)
            elif file_before[:fileNum].strip('0').isdigit():
                new_path = new + file_before[fileNum:] + '.' + endswith
            else:
                new_path = new + file_before + '.' + endswith
            os.renames(to_pa, new_path)

    # </editor-fold>
    # <editor-fold desc="文件匹配">
    def glob(self, re_, root_dir, dir_fd=None, recursive=False):
        """

        :param endswith:
        :param root_dir:
        :param dir_fd:
        :param recursive:
        :return:
        glob 函数支持三种格式的语法：
* 匹配单个或多个字符
? 匹配任意单个字符
[] 匹配指定范围内的字符，如：[0-9]匹配数字。
        """
        # glob.glob("*.ipynb")
        # glob.glob("../09*/*.ipynb")
        # glob.glob("../[0-9]*")#匹配数字开头的文件夹名：
        # glob.glob("*.ipynb")
        return glob.glob(re_, root_dir=root_dir, dir_fd=dir_fd, recursive=recursive)

    # </editor-fold>
    def environment(self):
        """ 判断什么环境下
        windows 1
        linux 2
        mac 3
        """
        # 查看系统类型
        platform_ = platform.system()
        platformenv = 1  # 默认0 如果读不到,默认是在windows 环境下
        if platform_ == "Windows":
            platformenv = 1  # windows 1
        elif platform_ == "Linux":
            platformenv = 2  # linux 2
        elif platform_ == "Mac":
            platformenv = 3  # mac 3
        return platformenv

    def path(self, folderPath):
        env = self.environment()
        if folderPath is None:
            raise self.ConstCaseError("请传入文件夹路径,  项目/xxx文件夹  ")
        if (env == 1):
            folderPath = folderPath.replace("/", "\\")
            # print(pathUtil+folderPath)
            isok, msg = self.makedirs(folderPath)
            if not isok and msg != "":
                print("创建文件夹失败,请检查是否有此文件夹  ===>", folderPath)
            return folderPath
        if (env == 2):
            folderPath = folderPath.replace("/", "/")
            isok, msg = self.makedirs(folderPath)
            if not isok and msg != "":
                print("创建文件夹失败,请检查是否有此文件夹  ===>", folderPath)
            return folderPath
        if (env == 3):
            folderPath = folderPath.replace("/", "/")
            isok, msg = self.makedirs(folderPath)
            if not isok and msg != "":
                print("创建文件夹失败,请检查是否有此文件夹  ===>", folderPath)
            return folderPath
        self.makedirs(folderPath)
        return folderPath

    # <editor-fold desc="当前位置找到多层之后的父级">
    def path_layer(self, n, current_path=None):
        if not current_path:
            current_path = os.getcwd()
        for i in range(n):
            current_path = os.path.dirname(current_path)
        return current_path
    # </editor-fold>
