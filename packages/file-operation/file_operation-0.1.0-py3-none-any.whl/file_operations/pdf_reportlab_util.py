# -*- coding: utf-8 -*-
"""
@Time : 2024/3/1 16:31 
@项目：文件使用
@File : reportlab制作pdf.by
@PRODUCT_NAME :PyCharm
"""
import datetime

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.units import inch
# 注册中文字体  下载自己需要的.ttf字体，例如STSONG.ttf
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageTemplate
from reportlab.platypus import Paragraph, Table
from reportlab.platypus.doctemplate import BaseDocTemplate, Frame

# youyuan_ttf = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "../..")), r'media\ttf\youyuan.TTF')
youyuan_ttf = r'F:\ContentPro\PythonPro\automaticoffice\字体\youyuan.TTF'
fontName = 'youyuan'

pdfmetrics.registerFont(TTFont(
    fontName,  # 命名
    youyuan_ttf,  # 字体位置
))
registerFontFamily(fontName, )


class MyReportlab():
    def footer(self, canvas, doc):
        Style = getSampleStyleSheet()
        normalStyle = Style['Normal']
        normalStyle.wordWrap = 'CJK'
        normalStyle.fontName = fontName  # 使用的字体
        """
        设置页脚
        :param canvas:Canvas类型  pdf画布
        :param doc:doc类型   整个pdf文件
        """
        canvas.saveState()  # 先保存当前的画布状态
        # pageNumber = ("%s/%s页" % (canvas.getPageNumber(), 1))  # 获取当前的页码
        pageNumber = ("%s页" % (canvas.getPageNumber(),))  # 获取当前的页码
        # pageNumber = ("%s/%s页" % (canvas.getPageNumber(), doc.pages))  # 获取当前的页码
        p = Paragraph(pageNumber, normalStyle)
        w, h = p.wrap(4 * cm, 1 * cm)  # 申请一块1cm大小的空间，返回值是实际使用的空间
        p.drawOn(canvas, (doc.width - len(pageNumber)) / 2, 10)  # 将页码放在指示坐标处
        canvas.restoreState()

    def header(self, canvas, doc):
        """
        设置页眉
        :param canvas:Canvas类型  pdf画布
        :param doc:doc类型     整个pdf文件
        """
        Style = getSampleStyleSheet()
        normalStyle = Style['Normal']
        normalStyle.wordWrap = 'CJK'
        normalStyle.fontName = fontName  # 使用的字体
        canvas.saveState()
        # p = Paragraph("<img src='%s' width='%d' height='%d'/>" % ('img_address', 11, 12),
        #               normalStyle)  # 使用一个Paragraph Flowable存放图片
        p = Paragraph("11111111111sdasdsada",
                      normalStyle)  # 使用一个Paragraph Flowable存放图片
        w, h = p.wrap(doc.width, doc.bottomMargin)
        p.drawOn(canvas, doc.leftMargin, doc.topMargin + doc.height - 0.5 * cm)  # 放置图片
        # p = Paragraph("<font size=10 face='STSong-Light'>报告</font>", normalStyle)
        # w, h = p.wrap(doc.width, doc.bottomMargin)
        # p.drawOn(canvas, doc.leftMargin + doc.width - 2.2 * cm, doc.topMargin + doc.height - 0.3 * cm)  # 放置报告这句话
        canvas.line(doc.leftMargin, doc.bottomMargin + doc.height + 0.5 * cm, doc.leftMargin + doc.width,
                    doc.bottomMargin + doc.height + 0.5 * cm)  # 画一条横线
        canvas.restoreState()

    def table_model_all(self, data):
        width = 10  # 总宽度
        colWidths = (width / len(data[0])) * inch  # 每列的宽度
        dis_list = []
        for x in data:
            # dis_list.append(map(lambda i: Paragraph('%s' % i, cn), x))
            dis_list.append(x)
        style = [
            ('FONTNAME', (0, 0), (-1, -1), fontName),  # 字体
            ('FONTSIZE', (0, 0), (-1, -1), 9.1),  # 字体大小
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 水平居中对齐
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 垂直居中
            ('hAlign', (0, 0), (-1, -1), 'CENTER'),  # 对齐
            # ('BOX', (0, 0), (-1, -1), 1, colors.black),  # 外边框
            # ('INNERGRID', (2, 0), (2, -1), 0, colors.white),  # 内边框
            # ('LEADING', (2, 0), (2, -1),24),  # 行距
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # 设置表格框线为grey色，线宽为0.5
            # ('SPAN', (2, 0), (2, -1)),  # 合并 （'SPAN',(第一个方格的左上角坐标)，(第二个方格的左上角坐标))，合并后的值为靠上一行的值，按照长方形合并
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # 设置表格内文字颜色
            # ('BACKGROUND', (0, 0), (-1, 0), HexColor('#d5dae6')),  # 设置第一行背景颜色
            # ('BACKGROUND', (0, 1), (-1, 1), HexColor('#d5dae6')),  # 设置第二行背景颜色
            # ('LINEBEFORE', (0, 0), (0, -1), 1, colors.grey),  # 设置表格边左边线颜色为灰色，线宽为0.1
            # ('LINEBELOW', (0, -1), (-1, -1), 2, colors.red),  # 设置表格边下边线颜色为灰色，线宽为0.1
            # ('LINEABOVE', (0, 0), (-1, 0), 2, colors.green),#设置表格上边线颜色为灰色，线宽为0.1
            # ('LINEABOVE', (0, 1), (-1, -1), 0.25, colors.red),#设置表格下边线颜色为灰色，线宽为0.1
            # ('NOSPLIT', (1, 0), (3, 18)),#间隔
            #
        ]

        component_table = Table(dis_list,
                                colWidths=[2.5 * inch, 2.5 * inch, 50, 2.5 * inch, 2.5 * inch, ],
                                style=style,
                                # vAlign="LEFT",
                                # hAlign="LEFT"
                                )

        return component_table

    def font_create(self, font_style="Normal", fontName="youyuan", wordWrap='CJK', firstLineIndent=32, leading=None,
                    fontSize=None, alignment=0, textColor=colors.black
                    ):
        Style = getSampleStyleSheet()
        font = Style[font_style]  # 字体的样式
        font.fontName = fontName  # 使用的字体
        font.wordWrap = wordWrap  # 该属性支持自动换行，'CJK'是中文模式换行，用于英文中会截断单词造成阅读困难，可改为'Normal'
        if firstLineIndent:
            font.firstLineIndent = firstLineIndent  # 该属性支持第一行开头空格
        if leading:
            font.leading = leading  # 该属性是设置行距
        if fontSize:
            font.fontSize = fontSize
        if alignment or alignment == 0:
            font.alignment = alignment  # 居中
        if textColor:
            font.textColor = colors.black  # 颜色
        return font

    def table_normal(self):
        table_style = [
            ('SPAN', (0, 0), (-1, 0)),
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#d5dae6')),
            ('FONTNAME', (0, 0), (-1, -1), fontName),  # 字体
            ('FONTSIZE', (0, 0), (-1, -1), 9.1),  # 字体大小
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 水平居中对齐
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 垂直居中
            ('hAlign', (0, 0), (-1, -1), 'CENTER'),  # 对齐
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # 设置表格框线为grey色，线宽为0.5
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # 设置表格内文字颜色

        ]
        return table_style


class MyBaseDocTemplate(MyReportlab):
    def __init__(self, report_addresses):
        self.doc = BaseDocTemplate(report_addresses,
                                   pagesize=A4,
                                   # pagesize=landscape(letter),
                                   rightMargin=10,
                                   leftMargin=10,
                                   topMargin=50,
                                   bottomMargin=20
                                   )
        self.font1 = self.font_create(alignment=1, fontSize=20)
        self.font2 = self.font_create(alignment=0, firstLineIndent=32)


# 案例
class HwdReport(MyBaseDocTemplate):
    def __init__(self, report_addresses):
        super().__init__(report_addresses)

    def get_fwd_build(self, date=datetime.datetime.now().strftime('%Y年%m月%d日'),
                      area="同济大学嘉定校区通达馆副楼外",
                      creator="佚名",
                      creator_sign="",
                      test_by="同科",
                      brand="熙赢测控",
                      version="SHN-HWD-S",
                      number="SHN-HWD-S（无）",
                      operators="匿名"):
        build_lis = [
            Paragraph('HWD标定报告', self.font1),
            Paragraph(f'<br/><br/><br/>', self.font2),
            Paragraph(f'\t标定日期:{"&emsp;" * 4}{date}', self.font2),
            Paragraph(f'\t标定场地:{"&emsp;" * 4}{area}', self.font2),
            Paragraph(f'\t标定人员:{"&emsp;" * 4}{creator}', self.font2),
            Paragraph(f'\t标定人员签名:_________________', self.font2),
            Paragraph(f'<br/><br/><br/>', self.font2),

            Paragraph(f'\tHWD测试方:{"&emsp;" * 4}{test_by}', self.font2),
            Paragraph(f'\tHWD品牌:{"&emsp;" * 5}{brand}', self.font2),
            Paragraph(f'\tHWD型号:{"&emsp;" * 5}{version}', self.font2),
            Paragraph(f'\tHWD编号:{"&emsp;" * 5}{number}', self.font2),
            Paragraph(f'\tHWD操作人员:{"&emsp;" * 3}{operators}', self.font2),
            Paragraph(f'<br/><br/><br/>', self.font2),
            Paragraph(f'\tHWD随机误差', self.font_create(alignment=0, firstLineIndent=32)),

        ]
        table1_content = [
            [
                ['HWD荷载随机误差判定#1', ],
                ['判定阈值', ''],
                ['误差大小', '002'],
                ['判定结果', '003'],
                ['误差来源', '003\n005']
            ],
            [
                ['HWD Geophone随机误差判定#1', ''],
                ['判定阈值', ''],
                ['误差大小', 'Geophone随机误差判定Geophone随机误差判定Geophone随机误差判定\nGeophone随机误差判定'],
                ['判定结果', '003'],
                ['误差来源', '003\n005']
            ]]
        for table_data in table1_content:
            build_lis.append(Paragraph(f'<br/><br/><br/>', self.font2), )
            build_lis.append(
                Table(table_data,
                      colWidths=[2.5 * inch, 5 * inch],
                      style=self.table_normal(),
                      # vAlign="LEFT",
                      # hAlign="LEFT"
                      )
            )
        build_lis.append(Paragraph(f'<br/><br/><br/>', self.font2), )
        build_lis.append(
            Paragraph(f'\t标定模型', self.font_create(alignment=0, firstLineIndent=32)),
        )
        table2_content = [
            [
                ['Geophone #1', 'Geophone #1'],
                ['距离承载板', ''],
                ['标定方程', '002'],
                ['决定系数（R2）', '003'],
                ['误差来源', '003\n005']
            ],
            [
                ['Geophone #2', 'Geophone #2'],
                ['距离承载板', ''],
                ['标定方程', '002'],
                ['决定系数（R2）', '003'],
                ['误差来源', '003\n005']
            ],
            [
                ['Geophone #3', 'Geophone #3'],
                ['距离承载板', ''],
                ['标定方程', '002'],
                ['决定系数（R2）', '003'],
                ['误差来源', '003\n005']
            ],
            [
                ['Geophone #4', 'Geophone #4'],
                ['距离承载板', ''],
                ['标定方程', '002'],
                ['决定系数（R2）', '003'],
                ['误差来源', '003\n005']
            ],
            [
                ['Geophone #5', 'Geophone #5'],
                ['距离承载板', ''],
                ['标定方程', '002'],
                ['决定系数（R2）', '003'],
                ['误差来源', '003\n005']
            ],
            [
                ['Geophone #6', 'Geophone #6'],
                ['距离承载板', ''],
                ['标定方程', '002'],
                ['决定系数（R2）', '003'],
                ['误差来源', '003\n005']
            ],
        ]
        for table_data in table2_content:
            build_lis.append(Paragraph(f'<br/><br/><br/>', self.font2), )
            build_lis.append(
                Table(table_data,
                      colWidths=[2.5 * inch, 5 * inch, ],
                      style=self.table_normal(),
                      # vAlign="LEFT",
                      # hAlign="LEFT"
                      )
            )
        build_lis.append(Paragraph(f'<br/><br/><br/>', self.font2), )

        build_lis.append(Paragraph(f'标定结论', self.font2), )
        build_lis.append(
            Paragraph(f'测试方 {test_by}  来标定的HWD品牌为 {brand} ，型号为 {number}，接受机场道面适航安全测试设备标定管理平台的标定', self.font2),
        )
        build_lis.append(
            Paragraph(f'标定结论和依据如下：', self.font2),
        )
        lis = ["""（1）标定中 通过 荷载随机误差判定（误差 < 1%）""",
               """（2）标定中 通过 Geophone随机误差判定（误差 < 2%）""",
               """（3）标定中 通过 系统标定，且标定方程的拟合优度良好（各决定系数 > 0.9, 决定系数均值 > 0.95）""",
               """（4）标定结论为HWD设备 通过 本次标定。""",
               ]
        for li in lis:
            build_lis.append(
                Paragraph(li, self.font2),
            )
        build_lis.append(
            Paragraph(f'根据标定数据和结果给出以下建议：', self.font2),
        )
        lis2 = [
            """（1） 标定的Geophone#3需要进行检查或组件标定，考虑替换此传感器或支架。""",
            """（2） 标定的Geophone#5需要进行检查，同时需检查本段支架。""",
            """（3） 标定的Geophone#6需要进行检查，同时需检查本段支架。  """
        ]
        for li in lis2:
            build_lis.append(
                Paragraph(li, self.font2),
            )

        return build_lis

    def get_report(self, build_data):
        frame_footer = Frame(self.doc.leftMargin, self.doc.bottomMargin, self.doc.width, self.doc.height,
                             id='normal')  # 声明一块Frame，存放页码
        template = PageTemplate(id='test', frames=frame_footer,
                                # onPage=self.header,
                                onPageEnd=self.footer)  # 设置页面模板，在加载页面时先运行herder函数，在加载完页面后运行footer函数
        self.doc.addPageTemplates([template])
        self.doc.build(build_data)


if __name__ == '__main__':
    pdf_obj = HwdReport(f"LoaderReport.pdf")
    pdf_obj.get_report(pdf_obj.get_fwd_build())
