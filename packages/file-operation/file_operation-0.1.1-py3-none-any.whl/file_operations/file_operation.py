#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:skyoceanchen
# project_name:chengduairport
# py_name :processing_txt
# software: PyCharm
# datetime:2021/3/3 13:45
"""文件类工具"""
import datetime as dt
import imghdr
import os
import uuid

import filetype
from PIL import Image
from basic_type_operations.str_operation import StringOperation
from django.conf import settings
from django.http import StreamingHttpResponse
from django.utils.encoding import escape_uri_path  # 用于解决中文命名文件乱码问题

PassExPrentFile = ["png", "jpg", "doc", "pdf", "xlsx", 'docx', 'xls', 'zip', 'mp4']
passFile = ['.doc', '.docx']
picEx = ["png", "jpg"]


class FileOperation(object):
    @staticmethod
    def save_destination(dest, reqfile):
        if not os.path.exists(dest):
            if not isinstance(reqfile, bytes):
                with open(dest, "wb") as destination:
                    for chunk in reqfile.chunks():
                        destination.write(chunk)
            else:
                with open(dest, "wb") as destination:
                    destination.write(reqfile)

    @staticmethod
    def upload(FILES, file_type: str, **kwargs):
        """
            上传文件
        :return:
        """
        reqfile = FILES
        if kwargs:
            filename = kwargs['file_name']
            filename_old = kwargs['file_name']
        else:
            filename = reqfile.name
            filename_old = reqfile.name
        if str(filename).find('.') == -1:
            filename = filename + '.jpg'
            suffix = '.jpg'
        else:
            suffix = filename[filename.rfind('.'):]
        filename_old = filename
        if StringOperation.check_contain_zh_cn(filename) and imghdr.what(reqfile):
            filename_old = filename
            filename = str(uuid.uuid1()) + suffix

        current_time = dt.datetime.now().strftime("%Y%m%d%H%M%S")
        current_time_str = dt.datetime.now().strftime("%Y%m%d %H:%M:%S")

        pathdir = os.path.join(settings.MEDIA_ROOT, file_type, current_time).replace('\\', '/')
        pathRela = os.path.join(file_type, current_time, filename).replace('\\', '/')
        dest = os.path.join(settings.MEDIA_ROOT, file_type, current_time, filename).replace('\\', '/')

        if not os.path.exists(pathdir):
            os.makedirs(pathdir)
        thumb_flag = False
        if not isinstance(reqfile, bytes):
            if imghdr.what(reqfile):  # 是图片类型
                thumb_flag = True
                img_ = Image.open(reqfile).convert('RGB')
                width, height = img_.size
                size = (480, 480)
                img_.thumbnail(size, Image.ANTIALIAS)
                thumb_path = os.path.join(settings.MEDIA_ROOT, 'thumb', file_type, current_time).replace('\\', '/')
                if not os.path.exists(thumb_path):
                    os.makedirs(thumb_path)
                # print(thumb_path)
                # 保存
                img_.save(thumb_path + '/' + filename, quality=70)
        FileOperation.save_destination(dest, reqfile)
        res = {
            'original': settings.HTTP_HEAD + '/media/' + pathRela,
            'short_url': pathRela
        }
        if thumb_flag:
            res['thumb'] = settings.HTTP_HEAD + '/media/thumb/' + pathRela
        return res

    @staticmethod
    def file_upload(FILES, file_type: str, **kwargs):
        """
            上传文件
        :return:
        """
        try:
            reqfile = FILES
            filename = reqfile.name
            suffix = filename[filename.rfind('.'):]
            kind = filetype.guess(reqfile)
            if kind is None and suffix not in passFile:
                raise Exception('未知混乱或无效的文件')
            if kind and kind.extension not in PassExPrentFile:
                raise Exception('不允许的文件类型')
            current_time = dt.datetime.now().strftime("%Y%m%d%H%M%S")
            if StringOperation.check_contain_zh_cn(filename):
                filename = str(uuid.uuid1()) + suffix

            pathdir = os.path.join(settings.MEDIA_ROOT, file_type, current_time).replace('\\', '/')
            pathRela = os.path.join(file_type, current_time, filename).replace('\\', '/')
            dest = os.path.join(settings.MEDIA_ROOT, file_type, current_time, filename).replace('\\', '/')
            if not os.path.exists(pathdir):
                os.makedirs(pathdir)
            FileOperation.save_destination(dest, reqfile)
            res = {
                'original': settings.HTTP_HEAD + '/media/' + pathRela,
                'short_url': pathRela
            }
            return res
        except Exception as e:
            raise Exception('文件传输过程中发生异常，或者您上传了不允许的文件')

    @staticmethod
    def file_iterator(file_name):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read()
                if c:
                    yield c
                else:
                    break

    @staticmethod
    def download(request, file_name, file_path):
        response = StreamingHttpResponse(FileOperation.file_iterator(file_path))
        file_end = file_path.split('.')[-1]
        agent = request.META.get('HTTP_USER_AGENT')
        if agent.upper().find("MSIE") != -1:
            response['Content-Disposition'] = "attachment; filename={0}".format(file_name + f'.{file_end}').encode(
                'gbk').decode('latin-1')
        elif agent.upper().find("EDGE") != -1:
            response['Content-Disposition'] = "attachment; filename={0}".format(file_name + f'.{file_end}').encode(
                'gb2312')
        elif agent.upper().find("TRIDENT") != -1:
            response['Content-Disposition'] = "attachment; filename={0}".format(file_name + f'.{file_end}').encode(
                'gb2312')
        else:
            response['Content-Disposition'] = 'attachment; filename={}'.format(
                escape_uri_path(file_name + f'.{file_end}'))
        response["Access-Control-Expose-Headers"] = "Content-Disposition"  # 为了使前端获取到Content-Disposition属性
        if file_end == "pdf":
            response["Content-type"] = "application/pdf"
        elif file_end == "zip":
            response["Content-type"] = "application/zip"
        elif file_end == "doc":
            response["Content-type"] = "application/msword"
        elif file_end == "xls":
            response["Content-type"] = "application/vnd.ms-excel"
        elif file_end == "xlsx":
            response["Content-type"] = "application/vnd.ms-excel"
        elif file_end == "docx":
            response["Content-type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        elif file_end == "doc":
            response["Content-type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        elif file_end == "ppt":
            response["Content-type"] = "application/vnd.ms-powerpoint"
        elif file_end == "pptx":
            response["Content-type"] = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        else:
            response['Content-Type'] = 'application/octet-stream'
        return response
