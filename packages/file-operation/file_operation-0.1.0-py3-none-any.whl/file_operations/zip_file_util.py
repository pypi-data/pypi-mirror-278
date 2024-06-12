#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:skyoceanchen
# project_name:chengduairport
# py_name :processing_txt
# software: PyCharm
# datetime:2021/3/3 13:45
"""文件类工具"""

import os
import shutil
import tarfile
import urllib
import zipfile

import patoolib  # pip install patool
import requests

PassExPrentFile = ["png", "jpg", "doc", "pdf", "xlsx", 'docx', 'xls', 'zip', 'mp4']
passFile = ['.doc', '.docx']
picEx = ["png", "jpg"]
from .os_file_util import FileBasicOperation


class FileZIPOperation(object):
    # <editor-fold desc="zip下载器">
    def zip_download(self, urllist, namelist):
        count = 0
        dir = os.path.abspath('.')
        for item in urllist:
            if os.path.exists(os.path.join(dir, namelist[count] + '.zip')):
                count = count + 1
            else:
                try:
                    # print('正在下载' + namelist[count])
                    work_path = os.path.join(dir, namelist[count] + '.zip')
                    urllib.request.urlretrieve(item, work_path)
                    count = count + 1
                except:
                    continue

    # </editor-fold>
    # <editor-fold desc="# zip的压缩和解密">
    # 打包目录为zip文件（未压缩）
    def zip_make(self, source_dir, output_filename):
        """
        make_zip(r'F:\jiyiproj\mysqlbackup\jiekouback\image\copyimage', "copyimage.zip")
        :param source_dir:
        :param output_filename:
        :return:
        """
        zipf = zipfile.ZipFile(output_filename, 'w')
        pre_len = len(os.path.dirname(source_dir))
        for parent, dirnames, filenames in os.walk(source_dir):
            for filename in filenames:
                pathfile = os.path.join(parent, filename)
                arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
                zipf.write(pathfile, arcname)
        zipf.close()

    # zip解压缩
    def zip_unpack(self, zip_path, dst_dir, ):
        # dst_dir = os.getcwd() + '/extract'  # 解压目录
        # zip_path = os.getcwd() + '/tk_mysql_dump_Release_20200717.zip'  # 压缩包路径
        os.makedirs(dst_dir)
        FileBasicOperation().makedirs(dst_dir)
        try:
            shutil.unpack_archive(zip_path, dst_dir, zip_path.split(".")[-1])
        except:
            with zipfile.ZipFile(zip_path, 'r') as f:
                f.extractall(dst_dir)

    # zip解加密压缩包
    def zip_extract(self, zip_path, dst_dir, pwd):
        """
        p = 'di201805'
    path = r'F:\python学习资料\新建文件夹\解压后'
        :param mypath:
        :return:
        """
        # zfile = zipfile.ZipFile(r"F:\jiyiproj\automaticoffice\002common\文件以及文件夹\extract\C语言编程精粹.PDF.zip")
        zfile = zipfile.ZipFile(zip_path)
        zfile.extractall(path=dst_dir, pwd=str(pwd).encode('utf-8'))

    # </editor-fold>
    # <editor-fold desc="tar.gz 打包 压缩">
    # 打包目录为zip文件（未压缩）
    # 一次性打包整个根目录。空子目录会被打包。
    # 如果只打包不压缩，将"w:gz"参数改为"w:"或"w"即可。
    def tar_gz_make(self, source_dir, output_filename, ):
        """
        tar_gz_make("copyimage.tar.gz", r'F:\jiyiproj\mysqlbackup\jiekouback\image\copyimage')
        :param output_filename:
        :param source_dir:
        :return:
        """
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))

    # 逐个添加文件打包，未打包空子目录。可过滤文件。
    # 如果只打包不压缩，将"w:gz"参数改为"w:"或"w"即可。
    # 多个不同目录下的文件打包成一个tar
    def tar_gz_files_make(self, source_dir, output_filename, ):
        """
        make_targz_one_by_one("copyimage.tar.gz", r'F:\jiyiproj\mysqlbackup\jiekouback\image\copyimage')
        :param output_filename:
        :param source_dir:
        :return:
        """
        tar = tarfile.open(output_filename, "w:gz")
        for root, dir, files in os.walk(source_dir):
            for file in files:
                pathfile = os.path.join(root, file)
                tar.add(pathfile)
        tar.close()

    # 多个不同目录下的文件打包成一个tar
    def tar_gz_any_files_make(self, output_filename, source_dir_lis):
        """
        # make_targz_many('/home/zlp/zlp.tar.gz', ['/home/zlp/result', '/home/zlp/Desktop/teston2'])
        :param output_filename:
        :param source_dir:
        :return:
        """
        with tarfile.open(output_filename, "w:gz") as tar:
            for dir in source_dir_lis:
                tar.add(dir, arcname=os.path.basename(dir))

    def tar_gz_unpack(self, tar_gz_path, dst_dir):
        with tarfile.open(tar_gz_path, 'r:gz') as tar:
            tar.extractall(dst_dir)

    # </editor-fold>
    # <editor-fold desc="rar压缩和解压缩">
    def rar_unpack(self, rar_path, dst_dir):
        patoolib.extract_archive(rar_path, outdir=dst_dir)

    # </editor-fold>
    def get_archive_formats(self, ):
        return shutil.get_archive_formats()

    def make_archive(self, base_name, format, root_dir=None, base_dir=None):
        """
        Create an archive file (eg. zip or tar).
        :param base_name: 是要创建的文件的名称，减去任何特定于格式的扩展名;
        :param format:“格式”是存档格式：“zip”，“tar”，“gztar”，“bztar”或“xztar”之一。或任何其他注册格式。
        :param root_dir: 是一个目录，将成为存档的根目录
        :param base_dir: “base_dir”是我们开始存档的目录
       “root_dir”和“base_dir”都默认为当前目录。返回存档文件的名称。
        :return:
            print(FileZIPOperation().make_archive("dirs/dirs111", "bztar", root_dir="dirs",
                                          base_dir="dirs"))
                                          生成
        # print(FileZIPOperation().make_archive("dirs", "gztar"))
        # print(FileZIPOperation().make_archive("dirs", "tar"))
        # print(FileZIPOperation().make_archive("dirs", "xztar"))
        # print(FileZIPOperation().make_archive("dirs", "zip"))
        """
        shutil.make_archive(base_name, format, root_dir=root_dir, base_dir=base_dir, )

    def send_zip(self, url, zip_path, headers=None):
        files = {'app_filename': (zip_path, open(zip_path, 'rb'), 'application/x-zip-compressed')}
        # files ={'app_filename':open('portal-1.0-SNAPSHOT-fat.jar.zip','rb')} 和上面的功能一样
        if not headers:
            headers = {
                'Authorization': '6bae7b70-8dae-4f74-9631-680b9501b52',
                'cookie': "_ga=GA1.3.733851079.1534745675; Hm_lvt_dde6ba2851f3db0ddc415ce0f895822e=1537859803; _ga=GA1.3.733851079.1534745675; Hm_lvt_dde6ba2851f3db0ddc415ce0f895822e=1537859803",
            }
        res = requests.post(url, files=files, headers=headers)
        return res.json()
