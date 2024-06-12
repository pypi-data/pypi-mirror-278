# -*- coding: utf-8 -*-
"""
@Time : 2023/8/10 14:54 
@Author : skyoceanchen
@TEL: 18916403796
@项目：文件使用
@File : file_transform.by
@PRODUCT_NAME :PyCharm
"""
import os
import subprocess

import docx
import pdfkit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


# <editor-fold desc="HTML-转PDF">
class PdfKitOperation(object):
    def __init__(self, wkhtmltopdf_path):
        """
        下载：https://wkhtmltopdf.org/
        https://wkhtmltopdf.org/downloads.html
        :param wkhtmltopdf_path:wkhtmltopdf.exe的绝对路径
        """
        self.config = pdfkit.configuration(
            wkhtmltopdf=wkhtmltopdf_path)
        self.set_options()

    def set_options(self, orientation='Landscape'):
        """
        options = {
                # 'header-html': 'http://localhost:8080/static/data/pdfHeader.html',
                # # 设置页眉数据，作为页眉的html页面必须有<!DOCTYPE html>
                # 'header-spacing': '3',  # 设置页眉与正文之间的距离，单位是毫米
                # 'header-right': 'Quality Report',  # 设置页眉右侧数据
                # 'header-font-size': 10,  # 设置页眉字体大小
                # 'footer-font-size': 10,  # 设置页脚字体大小
                'footer-center': '[page]/[topage]页',  # 设置页码
                # 'margin-top': '0.75in',
                # 'margin-right': '0.75in',
                # 'margin-bottom': '0.5in',
                # 'margin-left': '0.75in',
                # 'encoding': "UTF-8",
                # # 'no-outline': None, #为None时表示确定，则不生成目录
                # 'header-line': None,  # 为None时表示确定，生成页眉下的线
                'orientation': 'Landscape',  # 横向
                "enable-local-file-access": True  # 打开本地文件访问权限
            }
        :param options:
        :return:
        """
        options = {}
        options['page-size'] = 'A4'
        options['footer-center'] = '[page]/[topage]页'
        if orientation:
            options['orientation'] = 'Landscape'
        options['enable-local-file-access'] = True
        self.options = {}

    def from_file(self, input_path, output_path):
        pdfkit.from_file(input_path, output_path, configuration=self.config, options=self.options)

    def from_url(self, url, output_path):

        pdfkit.from_url(url, output_path, configuration=self.config, options=self.options)

    def form_string(self, data, output_path):
        pdfkit.from_string(data, output_path, configuration=self.config, options=self.options)

    # 变化
    def water_report(self, output_path, templates_path, dic={}):
        with open(templates_path, 'r', encoding='utf-8') as f:
            data = f.read()
        # lis = ['provide_people', "tel", 'airport_code', 'assessment_datetime', 'track_code', 'status_code', 'degree',
        #        'degree_deep', 'pavement_status', ]
        # lis_checkd = ['control_tower', 'control_tower_other']
        for i in dic.keys():
            data = data.replace(i, dic.get(i, ''))
        # control_tower = dic.get('control_tower', False)
        # control_tower_other = dic.get('control_tower_other', False)
        # if control_tower:
        #     data = data.replace(
        #         """<input class="input_agreement_protocol control_tower"  type="checkbox"/>""",
        #         """<input class="input_agreement_protocol control_tower" checked type="checkbox"/>""")
        # if control_tower_other:
        #     data = data.replace(
        #         """<input class="input_agreement_protocol control_tower_other" type="checkbox"/>""",
        #         """<input class="input_agreement_protocol control_tower_other" checked type="checkbox"/>""")
        self.form_string(data, output_path)


# </editor-fold>
class PandocOperations(object):
    def __init__(self, pandoc_path):
        """
        下载： https://www.pandoc.org/installing.html
        :param pandoc_path: pandoc.exe 绝对路径
        """
        self.pandoc_path = pandoc_path

    def md_pdf(self, md_path, pdf_path):
        system = f'{self.pandoc_path}  {md_path} -o {pdf_path}'
        print(system)
        os.system(system)

    def md_doc(self, md_path, pdf_path):
        system = f'{self.pandoc_path}  {md_path} -o {pdf_path}'
        print(system)
        os.system(system)

    def convert_docx_to_pdf(self, docx_file, pdf_file):
        command = f"{self.pandoc_path} {docx_file} -o {pdf_file} --pdf-engine=xelatex"
        subprocess.run(command, shell=True)


from docx2pdf import convert


class DocxToPDFOperations(object):
    def docx_to_pdf(self, input_path, output_path):
        """
        :param input_path: test.docx
        :param output_path: test.pdf
        :return:
        """
        convert("D:\Program\Anaconda3\envs\激光断面仪标定报告.docx", "D:\Program\Anaconda3\envs\激光断面仪标定报告.pdf")
        convert(input_path, output_path)


def convert_docx_to_pdf_2(docx_file, pdf_file, ttf_path):
    """

    :param docx_file:
    :param pdf_file:
    :param ttf_path: r'F:\ContentPro\PythonPro\automaticoffice\字体\youyuan.TTF'
    :return:
    """
    doc = docx.Document(docx_file)
    pdf = canvas.Canvas(pdf_file)
    # 加载字体
    pdfmetrics.registerFont(TTFont('Arial', ttf_path))
    for para in doc.paragraphs:
        pdf.setFont("Arial", 12)
        pdf.drawString(100, 700, para.text)
        pdf.showPage()

    pdf.save()

# 用法示例
# convert_docx_to_pdf(md_path, pdf_path)
