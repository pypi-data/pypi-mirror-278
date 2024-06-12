# -*- coding: utf-8 -*-
"""
@Time : 2023/8/16 21:13 
@Author : skyoceanchen
@TEL: 18916403796
@项目：文件使用
@File : pdf_operation.by
@PRODUCT_NAME :PyCharm
"""
# https://pyfpdf.readthedocs.io/en/latest/reference/close/index.html
# https://pyfpdf.readthedocs.io/en/latest/reference/set_creator/index.html
# https://pyfpdf.readthedocs.io/en/latest/
from fpdf import FPDF  # pip install fpdf==1.7.2


# 页面在A4纵向和度量单位是毫米。它可以通过以下方式明确指定：
# pdf = FPDF('P', 'mm', 'A4')
# 它可以使用横向（L），其他页面的格式（如Letter和 Legal），测量单元（pt，cm，in）
# pdf = FPDF()
# pdf.add_page()  # 添加一页
# pdf.set_font('Arial', 'B', 16)  # 设置字体 Arial粗体16
# pdf.cell(40, 10, 'Hello World!')  # 设置位置，添加数据
# pdf.cell(40, 10, 'Hello World!', 1)
# pdf.cell(60, 10, 'Powered by FPDF.', 0, 1, 'C')
# pdf.output('tuto1.pdf', 'F')  # 保存文件
# pdf.close()  # 关闭
# pdf.footer()


# pdf.accept_page_break()
# pdf.set_auto_page_break()
class PDF(FPDF):
    def __init__(self, orientation, unit, format):
        super(PDF, self).__init__(orientation=orientation, unit=unit, format=format)

    # 获取当前页码
    def page_no(self):
        "获取当前页码"
        return self.page

    # 别名nb_页:为页面总数定义一个别名
    def alias_nb_pages(self, alias='{nb}'):
        return super().alias_nb_pages(alias=alias)

    # 错误信息。
    def error(self, msg=str):
        """
        如果发生致命错误，将自动调用此方法；它只需输出消息并停止执行。
        继承的类可能会重写它以自定义错误处理，但应该始终停止脚本，否则生成的文档可能无效。
        :param msg:错误信息。
        :return:
        """
        super().error(msg=msg)

    #   激活或取消页压缩
    def set_compression(self, compress: bool):
        """
        激活或取消页压缩。当激活时，每个页面的内部表示都会被压缩，这将导致结果文档的压缩比约为2。
        默认情况下，压缩是打开的。
        :param compress:布尔值，指示是否必须启用压缩。
        :return:
        """
        super().set_compression(compress=compress)

    def set_display_mode(self, zoom, layout='continuous'):
        """

        :param zoom:要用的变焦。它可以是以下字符串值之一：
                    fullpage：：在屏幕上显示整个页面
                    fullwidth使用窗口的最大宽度
                    real使用实际大小(相当于100%缩放)
                    default*使用查看器默认模式
                    或表示要使用的缩放因子的数字，作为百分比。
        :param layout:页面布局。可能的价值是：
                    single：：每次显示一页
                    continuous*连续显示页面
                    two*在两列中显示两页
                    default*使用查看器默认模式
                    默认值是continuous.
        :return:
        """
        # 描述
        """
        定义查看器显示文档的方式。
        可以设置缩放级别：页面可以完全显示在屏幕上，
        占据窗口的全部宽度，使用实际大小，通过特定的缩放因子缩放
        ，或者使用查看器默认设置(在AdobeReader的“首选项”菜单中配置)。
        也可以指定页面布局：一次单页、连续显示、两列或查看器默认设置。
        如果未调用此方法，则将缩放模式设置为全宽而布局设置为连续默认情况下。
        """
        super().set_display_mode(zoom=zoom, layout=layout)

    # 定义文档的作者
    def set_author(self, author: str):
        """
        :param author: 作者的名字
        :return:
        """
        super().set_author(author=author)

    #  创建者
    def set_creator(self, creator: str):
        """
        定义文档的创建者。这通常是生成PDF的应用程序的名称。
        :param creator:创建者
        :return:
        """
        super().set_creator(creator=creator)

    # 关键词:关键字与文档相关联，通常以“keyword 1 keyword 2.”形式出现。
    def set_keywords(self, keywords: str):
        """
        :param keywords:关键词：关键词列表。形式->"keyword 1 keyword 2."
        :return:
        """
        super().set_keywords(keywords=keywords)

    # 定义文档的主题。
    def set_subject(self, subject: str):
        """
        :param subject: 主题
        :return:
        """
        super().set_subject(subject=subject)
    #
    # # 定义文档的标题。
    # def set_title(self, title: str):
    #     """
    #     :param title:标题。
    #     :return:
    #     """
    #     super().set_title(title=title)


class MyPDF(PDF):
    def __init__(self, orientation='P', unit='mm', format='A4'):
        """这是类构造函数。它允许设置所有方法中使用的页面格式、方向和度量单位(字体大小除外)。"""
        """
        :param orientation:页面方向。可能的值是(不区分大小写的)：
                            P or Portrait-----P或肖像
                            L or Landscape-----L或景观
                            默认值是传递给构造函数的值。
        :param unit: 用户单位。可能的价值是：
                        pt: point————PT：点
                        mm: millimeter————毫米：毫米
                        cm: centimeter————厘米：厘米
                        in: inch————英寸
        :param format:用于页面的格式。它可以是下列值之一(不区分大小写)：
                        A3----A3
                        A4----A4
                        A5----A5
                        Letter----信件
                        Legal----合法
                        或包含宽度和高度的元组(以给定单位表示)。在纵向定位中，元组应按顺序排列(宽度, 高度)，
                        但在景观方向上，顺序应该是(高度, 宽度)。在任何一种情况下，第一个元组元素通常小于第二个元组元素。
                        默认值是传递给构造函数的值。
                        默认值是A4。 
        """
        super(PDF, self).__init__(orientation=orientation, unit=unit, format=format)
        """
        使用自定义的100x150毫米页格式的示例：
        pdf = FPDF('P', 'mm', (100, 150))
        """

    def open(self):
        """
        此方法开始生成PDF文档。没有必要显式地调用它，因为添加页自动完成。
注意：此方法不会创建任何页面。
        :return:
        """
        super().open()

    # 在您自己的继承类中实现的头文件
    def header(self):
        """
        此方法用于呈现页面标题。
        它自动被添加页而不应由应用程序直接调用。
        FPDF中的实现是空的，所以如果需要特定的处理，
        就必须对它进行子类化并重写该方法。
        :return:
        """
        # Select Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Framed title
        # self.cell(30, 10, 'Title', 1, 0, 'C')
        # Line break
        self.ln(20)

    # 页面页脚
    def footer(self):
        """
        此方法用于呈现页面页脚。它由add_page自动调用并关闭，并且不应由应用程序直接调用。
        FPDF中的实现为空，因此如果要进行特定处理，则必须对其进行子类化并重写该方法。
        :return:
        """
        # Do not print footer on first page
        # 不要在第一页打印页脚
        if self.page_no() != 1:
            # Go to 1.5 cm from bottom
            self.set_y(-15)
            # Select Arial italic 8
            self.set_font('Arial', 'I', 8)
            # Print centered page number
            self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

    # 添加页
    def add_page(self, orientation='', format='', same=False):
        """
        :param orientation:页面方向。可能的值是(不区分大小写的)：
                            P or Portrait-----P或肖像
                            L or Landscape-----L或景观
                            默认值是传递给构造函数的值。
        :param format:用于页面的格式。它可以是下列值之一(不区分大小写)：
                        A3----A3
                        A4----A4
                        A5----A5
                        Letter----信件
                        Legal----合法
                        或包含宽度和高度的元组(以给定单位表示)。在纵向定位中，元组应按顺序排列(宽度, 高度)，
                        但在景观方向上，顺序应该是(高度, 宽度)。在任何一种情况下，第一个元组元素通常小于第二个元组元素。
                        默认值是传递给构造函数的值。
        :param same:如果页面必须与前一页相同，则为true。在这种情况下，其他参数将被忽略。
        :return:
        """
        # 描述
        """向文档添加新页。如果页已经存在，则页脚方法首先被调用以输出页脚。
        然后添加页面，根据左上角和上边框将当前位置设置为左上角，以及标头调用以显示标题。
        调用前设置的字体将自动还原。
        没有必要打电话设置字体同样，如果要继续使用相同的字体。颜色和线宽也保留下来。
        坐标系的起源在左上角，增加的纵坐标向下移动。
        """

        super().add_page(orientation=orientation)

    # 是否接受自动换页
    def accept_page_break(self):
        # <editor-fold desc="是否接受自动换页">
        """
        每当满足分页中断条件时，将调用此方法，并根据返回的值发出或不发出该中断。
        默认实现根据所选择的模式返回一个值。设置自动分页。此方法是自动调用的，应用程序不应直接调用该方法。
        :return:
        """
        return self.auto_page_break
        # </editor-fold>

    # 设置自动换页模式和触发页边距
    def set_auto_page_break(self, auto: bool, margin=0.0):
        # <editor-fold desc="设置自动换页模式和触发页边距">

        """
        启用或禁用自动分页模式。启用时，第二个参数是与定义触发限制的页面底部的距离。默认情况下，模式是开的，边距是2cm。
        :param auto:布尔值，指示模式是打开还是关闭。
        :param margin:与页面底部的距离。
        :return:
        """
        "设置自动换页模式和触发页边距"
        self.auto_page_break = auto
        self.b_margin = margin
        self.page_break_trigger = self.h - margin

        # </editor-fold>

    # 添加TrueType或Type1字体
    def add_font(self, family: str, style='', fname='', uni=False):
        # <editor-fold desc="添加TrueType或Type1字体">
        """
        :param pdf:
        :param family:字体系列。用作set_font的参考，例如：'dejavu'。
        :param style:字体样式。不推荐使用，仅为了向后兼容而进行维护。
        :param fname:字体文件名（例如'DejaVuSansCondensed.ttf'）。您可以指定完整路径；否则，将在FPDF_FONTPATH或中搜索文件SYSTEM_TTFONTS。
        :param uni:TTF Unicode标志（如果设置为True，则将启用TrueType字体子集嵌入，并且utf8默认情况下将文本视为文本）。
        :return:
        你一定不能调用add_font为标准PDF的Latin-1字体（快递，黑体，时代，符号，ZAPFDINGBATS）; 在这种情况下，请直接使用set_font。
        """
        super().add_font(family, style=style, fname=fname, uni=uni)
        """
        # Add a Unicode free font
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        # Add a Unicode system font (using full path)
        pdf.add_font('sysfont', '', r"c:\WINDOWS\Fonts\arial.ttf", uni=True)
        描述
        导入TrueType，OpenType或Type1字体并使其可用。
        警告：对于Type1和旧字体，必须首先使用该MakeFont实用程序生成字体定义文件。目前不推荐使用此功能，而支持TrueType Unicode字体（使用随附的ttfonts.py实用程序会自动处理其字体）。
        注意：字体源文件必须可访问。将在以下位置连续搜索它们（如果定义了这些常量）：
        FPDF_FONTPATH（默认情况下，font位于fpdf软件包目录中的文件夹）
        SYSTEM_TTFONTS（例如C:\WINDOWS\FONTS）
        如果找不到与所请求字体相对应的文件，则会引发运行时异常“未找到TTF字体文件：...”。
        有关更多信息，请参见Unicode支持页面。
        应该在使用set_font方法之前调用此方法，并且该字体将可用于整个文档。
        注意：由于字体处理会占用大量时间，因此会缓存一些数据。
        默认情况下，缓存文件是在同一文件夹中创建的。可以通过设置FPDF_CACHE_MODE常量来更改：
        0-（默认情况下），将缓存存储在字体文件所在的文件夹中
        1-禁用所有缓存
        2-将高速缓存文件存储在FPDF_CACHE_DIR具有神秘名称的目录中
        """

        # </editor-fold>

    # 选择一个字体;以点数表示的尺寸
    def set_font(self, family, style='', size=0):
        # <editor-fold desc="选择一个字体;以点数表示的尺寸">
        """
        :param family:
                字体家族。它可以是由添加字体或其中一个标准家庭(不区分大小写)：
                信使(固定宽度) ————Courier (fixed-width)
                Helvetica或Arial(同义词；无衬线) ————Helvetica or Arial (synonymous; sans serif)
                时间(衬线) ————Times (serif)
                符号(符号) ————Symbol (symbolic)
                ZapfDingbat(象征性) ————ZapfDingbats (symbolic)
                还可以传递空字符串。在这种情况下，保留目前的字体。

        :param size:字体大小(以点为单位)。默认值是当前大小。如果自文档开始以来没有指定任何大小，则所取值为12。
        :param style:字体风格。可能的值是(不区分大小写的)：
                    空字符串：普通字符串
                    B：粗体
                    I：斜体
                    U：划线
                    或者任何组合。默认值是规则的。粗体和斜体风格不适用于符号和ZapfDingbat。

        :return:
        """
        # 描述
        """
        设置用于打印字符串的字体。在打印文本或结果文档无效之前，必须至少调用一次此方法。
        字体可以是标准字体，也可以是通过添加字体方法。
        未指定默认编码，但所有文本写入方法只接受外部字体的Unicode和标准的一个字节编码。
        标准字体使用Latin-1默认情况下编码，但Windows编码cp1252(西欧)可与SET_doc选项(“core_fonts_coding”，编码)。
        可以在创建第一页之前调用该方法，并在页与页之间保留字体。
        如果您只想更改当前的字体大小，那么调用它就更简单了。设定字体大小.
        注字体度量文件必须是可访问的。他们先后在下列地点被搜查：
        由FPDF_FONTPATH常量定义的目录(如果定义了此常量)
        位于包含fpdf.py的目录中的字体目录(如果存在的话)
        通过include()示例访问的目录定义FPDF_FONTPATH(注意强制尾随斜杠)：Defined(“FPDF_FONTPATH”，“/HOME/www/字体/”)；Required(“fpdf.php”)；如果找不到与请求字体相对应的文件，则发出错误“无法包含字体度量文件”。
        """
        super().set_font(family=family, style=style, size=size)

        # </editor-fold>

    # 以点为单位设置字体大小
    def set_font_size(self, size):
        """
        定义当前字体的大小。
        :param size: 大小(以点数为单位)。
        :return:
        """
        super().set_font_size(size=size)

    # 创建一个新的内部链接
    def add_link(self):
        # <editor-fold desc="创建一个新的内部链接">
        """
        创建一个新的内部链接并返回其标识符。
        内部链接是指向文档中另一个位置的可点击区域。
        然后，可以将标识符传递给细胞, 写, 影象或链接。目标定义为设定链.
        :return:
        """
        return super().add_link()

        # </editor-fold>

    # 写入一个文本cell
    def cell(self, w, h=0, txt='', border=0, ln=0, align='', fill=False, link=''):
        # <editor-fold desc="写入一个文本cell">
        """
        打印带有可选边框、背景色和字符串的单元格(矩形区域)。单元格的左上角对应于当前位置.文本可以对齐或居中。
        调用后，当前位置移动到右侧或下一行。在文本上放一个链接是可能的。
        如果启用了自动分页，并且单元格超出了限制，则在输出之前会执行分页操作。
        :param w:宽度。如果为0，则该单元格扩展到右侧边缘。
        :param h:高度。默认值：0。
        :param txt:字符串。默认值：空字符串。
        :param border:指示是否必须在单元格周围绘制边框。该值可以是一个数字：
                        0：无边界
                        1：框架
                        或包含以下部分或全部字符的字符串(按任何顺序排列)：
                        L*左
                        T*顶部
                        R*对
                        B*底部
                        默认值：0。
        :param ln:指示调用后当前位置应移至何处。可能的价值是：
                    0：右边
                    1：到下一行的开头
                    2：下文
                    输入1等于将0放入并调用林就在这之后。默认值：0。
        :param align:允许对中或对齐文本。可能的价值是：
                        L或空字符串：左对齐(默认值)
                        C*中心
                        R*右对齐
        :param fill:指示是否必须绘制单元格背景(True)或透明(False)。默认值：false。
        :param link:返回的URL或标识符加链.add_link() 方法返回值
        :return:
        """
        super().cell(w=w, h=h, txt=txt, border=border, ln=ln, align=align, fill=fill, link=link)

        # </editor-fold>

    def multi_cell(self, w: float, h: float, txt: str = '', border=0, align: str = 'J', fill=0, split_only=False):
        """
        :param w:宽度。如果为0，则将其扩展到页的右边距。
        :param h:高度。
        :param txt:字符串
        :param border:指示是否必须围绕单元格块绘制边框。该值可以是一个数字：
                        0：无边界
                        1：框架
                        或包含以下部分或全部字符的字符串(按任何顺序排列)：
                        L*左
                        T*顶部
                        R*对
                        B*底部
                        默认值：0。
        :param align:设置文本对齐。可能的价值是：
            L*左对齐
            C*中心
            R*对齐
            J*理由(默认值)
        :param fill:指示是否必须绘制单元格背景(True)或透明(False)。默认值：false。
        :param split_only:
        :return:
        """
        # 描述
        """
        此方法允许打印带有换行符的文本。它们可以是自动的(当文本到达单元格的右边框时)或显式(通过\n)。
        输出尽可能多的单元格，其中一个在另一个下面。文本可以对齐、居中或对齐。该单元可以被框和背景油漆。
        """
        super().multi_cell(w=w, h=h, txt=txt, border=border, align=align, fill=fill, split_only=split_only)

    # 以流动模式输出文本
    def write(self, h: float, txt: str = '', link=''):
        # <editor-fold desc="以流动模式输出文本">
        """
        此方法从当前位置打印文本。当到达右边距(或满足\n字符)时，将发生行中断，文本从左侧边距继续。
        在方法退出时，当前位置就留在文本的末尾。在文本上放一个链接是可能的。
        :param h:线高。
        :param txt:字符串
        :param link:返回的URL或标识符加链. add_link() 方法返回值
        :return:
        """
        super().write(h=h, txt=txt, link=link)

        # </editor-fold>

    # 在页面上放一幅图片
    def image(self, name, x=None, y=None, w=0, h=0, type='', link=''):
        # <editor-fold desc="在页面上放一幅图片">
        """
        :param name:图像的路径或URL。
        :param x:左上角的横坐标。如果未指定或等于无，则使用当前的横坐标(版本1.7.1及以上).
        :param y:左上角的纵坐标。如果未指定或等于无，则使用当前纵坐标；此外，如果有必要，首先触发分页(在启用自动分页的情况下)，并且在调用之后，当前纵坐标被移动到图像的底部(版本1.7.1及以上).
        :param w:页面中图像的宽度。如果未指定或等于零，则自动计算。
        :param h:页面中图像的高度。如果未指定或等于零，则自动计算。
        :param type:图像格式可能的值是(不区分大小写的)：jpg、JPEG、PNG和GIF。如果未指定，则从文件扩展名推断类型。
        :param link:返回的URL或标识符加链. add_link() 方法返回值
        :return:
        """
        # 描述
        """
        放个图像。它将在页面上显示的大小可以通过不同的方式指定：
        显式宽度和高度(以用户单位表示)
        一个显式维数，另一个维数是自动计算的，以保持原来的比例。
        没有显式的维数，在这种情况下，图像被放置在72 dpi。
        支持的格式有JPEG、PNG和GIF。
        对于JPEG，所有口味都是允许的：
        灰阶
        真彩(24位)
        CMYK(32位)
        对于PNG，允许这样做：
        灰度等级最多为8位(256级)
        索引颜色
        真彩(24位)
        阿尔法通道(1.7及以上版本)
        但这一点没有得到支持：
        隔行
        对于GIF：在动画GIF的情况下，只使用第一个框架。
        如果定义了透明的颜色，就会考虑到它。
        可以从文件扩展名中显式指定或推断格式。
        可以在图像上添加链接。
        """
        super().image(name, x=x, y=y, w=w, h=h, type=type, link=link)

        # </editor-fold>

    # 在页面上放一个链接
    def link(self, x: float, y: float, w: float, h: float, link):
        # <editor-fold desc="在页面上放一个链接">
        """

        :param x:矩形左上角的横坐标。
        :param y:矩形左上角的纵坐标。
        :param w:矩形的宽度。
        :param h:矩形的高度。
        :param link:返回的URL或标识符加链. add_link() 方法返回值
        :return:
        """
        # 描述
        "将链接放到页面的矩形区域。文本或图像链接通常通过细胞, 写或影象，但是这个方法对于定义图像中的可点击区域很有用。"
        super().link(x=x, y=y, w=w, h=h, link=link)

        # </editor-fold>

    # 设置内部链路的目的地址
    def set_link(self, link, y=0.0, page=-1):
        # <editor-fold desc="设置内部链路的目的地址">
        """

        :param link:返回的URL或标识符加链. add_link() 方法返回值
        :param y:目标位置的纵坐标；-1表示当前位置。默认值为0(页面顶部)。
        :param page:目标页数；-1表示当前页，这是默认值。
        :return:
        """
        # 描述
        "定义链接指向的页面和位置。"
        super().set_link(link, y=y, page=page)

    # 虚线
    def dashed_line(self, x1, y1, x2, y2, dash_length=1, space_length=1):
        """
        :param x1:第一点横坐标
        :param y1:第一点纵坐标
        :param x2:第二点横坐标
        :param y2:第二点纵坐标
        :param dash_length:短跑长度
        :param space_length:破折号之间空格的长度
        :return:
        """
        # 描述
        """
        在两点之间画一条虚线。同界面线除了这两个参数，破折号和空格长度。
        """
        self._set_dash(dash_length, space_length)
        self.line(x1, y1, x2, y2)
        self._set_dash()
        """
        添加从点(10，30)开始的虚线，以点(110，30)结尾的#结束，其#破折号长度为1，空格长度为10。
        pdf.dashed_line(10, 30, 110, 30, 1, 10)
        """

    # 设定线宽
    def set_line_width(self, width: float):
        """
        定义线宽。默认情况下，该值等于0.2毫米。可以在创建第一个页面之前调用该方法，并在每个页面之间保留该值。
        :param width:宽度。
        :return:
        """
        super().set_line_width(width=width)

    # 线
    def line(self, x1, y1, x2, y2):
        """在两点之间划一条线。
        :param x1:第一点横坐标
        :param y1:第一点纵坐标
        :param x2:第二点横坐标
        :param y2:第二点纵坐标
        :return:
        添加从点(10,30)开始到点(110,30)结束的一行。
        pdf.line(10, 30, 110, 30)
        """
        super().line(x1=x1, y1=y1, x2=x2, y2=y2)

    # 画一个椭圆和圆形
    def ellipse(self, x: float, y: float, w: float, h: float, style=''):
        """
        输出椭圆。它可以绘制(仅限边界)、填充(无边界)或两者兼而有之。
        与PHP版本不同，此函数使用椭圆的左上角位置、宽度和高度，如下所示直角而不是中心点和半径。
        :param x:左上角边框的横坐标。
        :param y:左上角边框的纵坐标。
        :param w:宽度。
        :param h:高度。
        :param style:渲染风格。可能的价值是：
                    D或者是空字符串：抽签。这是默认值。
                    F*填补
                    DF或FD*绘制和填充
        :return:
        """
        super().ellipse(x=x, y=y, w=w, h=h, style=style)

    # 矩形
    def rect(self, x: float, y: float, w: float, h: float, style=''):
        """
        输出矩形。它可以绘制(仅限边界)、填充(无边界)或两者兼而有之。
        :param x:左上角的横坐标。
        :param y:左上角的纵坐标。
        :param w:宽度。
        :param h:高度。
        :param style:渲染风格。可能的价值是：
                    D或者是空字符串：抽签。这是默认值。
                    F*填补
                    DF或FD*绘制和填充
        :return:
        """
        super().rect(x=x, y=y, w=w, h=h, style=style)

    # 获取当前字体中字符串的宽度
    def get_string_width(self, s: str):
        """
        返回用户单元中字符串的长度。必须选择字体。
        该值是用拉伸和间距计算的。
        :param s:要计算长度的字符串。
        :return:
        """
        return super().get_string_width(s=s)

    # 定画颜色:所有绘图操作(线条、矩形和单元格边框)
    def set_draw_color(self, r: int, g: int = -1, b: int = -1):
        """

        :param r:如果g和b如果没有，则表示灰色级别。值介于0到255之间。
        :param g:绿色组件(介于0到255之间)。
        :param b:蓝色组件(介于0到255之间)。
        :return:
        """
        # 描述
        """
        定义用于所有绘图操作(线条、矩形和单元格边框)的颜色。
        它可以用RGB组件表示，也可以用灰度表示。可以在创建第一个页面之前调用该方法，并在每个页面之间保留该值。
        """
        super().set_draw_color(r=r, g=g, b=b)

    # 设置填充颜色:填充操作(填充矩形和单元格背景)的颜色
    def set_fill_color(self, r, g=-1, b=-1):
        """
        定义用于所有填充操作(填充矩形和单元格背景)的颜色。
        它可以用RGB组件表示，也可以用灰度表示。
        可以在创建第一个页面之前调用该方法，并在每个页面之间保留该值。
        :param r:
        :param g:
        :param b:
        :return:
        """
        super().set_fill_color(r=r, g=g, b=b)

    # 用于文本的颜色
    def set_text_color(self, r, g=-1, b=-1):
        """
        定义用于文本的颜色。
        它可以用RGB组件表示，也可以用灰度表示。
        可以在创建第一个页面之前调用该方法，并在每个页面之间保留该值。
        :param r:
        :param g:
        :param b:
        :return:
        """
        super().set_text_color(r=r, g=g, b=b)

    def text(self, x: float, y: float, txt: str = ''):
        """

        :param x:原点的横坐标。
        :param y:原点的纵坐标。
        :param txt:字符串
        :return:
        """
        # 描述
        """
        打印字符串。原点在第一个字符的左边，在基线上。
        此方法允许在页面上精确放置字符串，但通常更容易使用。细胞, 多室或写，这是打印文本的标准方法。
        """
        super().text(x=x, y=y, txt=txt)

    # 返回当前职位的横坐标。
    def get_x(self):
        return super().get_x()

    # 返回当前位置的纵坐标。
    def get_y(self):
        return super().get_y()

    # 设置纵坐标
    def set_x(self, x):
        "定义当前职位的横坐标。如果传递的值为负值，则相对于页的右侧。"
        super().set_x(x=x)

    # 设置纵坐标
    def set_y(self, y):
        "将当前的横坐标移回左侧边距，并设置纵坐标。如果传递的值为负值，则相对于页面底部。"
        super().set_y(y=y)

    # 设置纵坐标 设置纵坐标
    def set_xy(self, x, y):
        """

        :param x:横坐标的值
        :param y:纵坐标的值。
        :return:
        """
        # 定义当前位置的横坐标和纵坐标。如果传递的值为负值，则它们分别相对于页的右侧和底部。
        super().set_xy(x=x, y=y)

    def ln(self, h=''):
        """
        :param h: 休息的高度。默认情况下，该值等于上次打印单元格的高度。
        :return:
        """
        # 执行换行操作。当前的横坐标返回到左边的边距，纵坐标通过参数中传递的数量增加。

        super().ln(h=h)

    # 定义左、上和右边距。
    def set_margins(self, left: float, top: float, right: float = -1):
        # 定义左、上和右边距。默认情况下，它们等于1厘米。调用此方法来更改它们。
        super().set_margins(left=left, top=top, right=right)

    #  设上边距
    def set_top_margin(self, margin: float):
        """
        定义上边距。可以在创建第一页之前调用该方法。
        :param margin:边距
        :return:
        """
        super().set_top_margin(margin=margin)

    # 设定右边距
    def set_right_margin(self, margin: float):
        """
        定义正确的页边距。可以在创建第一页之前调用该方法。
        :param margin:边距
        :return:
        """
        super().set_right_margin(margin=margin)

    # 设定左边距
    def set_left_margin(self, margin: float):
        """
        定义左边框。可以在创建第一页之前调用该方法。如果当前的横坐标离开页面，它将返回到边距。
        :param margin:边距
        :return:
        """
        super().set_left_margin(margin=margin)

    # 保存文件
    def output(self, name='', dest=''):
        """
        :param name:文件的名称。仅在写入文件时使用。
        :param dest:发送文档的目的地。它可以采用下列值之一：
        I或D*将文件写入Sys.stdout。如果没有给出文件名，这是默认的。
        F：：保存到具有给定名称的本地文件(可能包括路径)。如果给出了文件名，这是默认的。
        S：：以字节字符串的形式返回文档。
        :return:
        """
        # 描述
        """
        将文档发送到某个目标：标准输出、文件或字节字符串。
        方法首先调用关必要时终止文档。
        注意事项：在Python中，字符串是原始数据，但在Python 3中，字符串现在默认为Unicode。
        如果您正在使用Python3.x，则必须使用pdf.output(dest='S').encode('latin-1')为了获得输出，
        如果不这样做，生成的PDF将是无效的，取决于查看器要么根本不打开，要么显示为一些空白页。
        """
        super().output(name=name,
                       dest='S'
                       ).encode('latin-1')

    # 关闭
    def close(self):
        """
        终止PDF文档。不需要显式调用此方法，因为输出量自动完成。
        如果文档不包含页面，添加页调用以防止获取无效文档。
        :return:
        """
        super().close()

    # 设定拉伸
    # def set_stretching(self,stretching: float):
    #     super().set_str


pdf = FPDF()
pdf.add_font('youyuan22', '', r'F:\ContentPro\PythonPro\automaticoffice\字体\youyuan - 副本.TTF', True)
pdf.add_page()
pdf.set_font('youyuan22', size=12)
pdf.cell(40, 10, 'Hello www我!踩踩踩踩踩踩踩踩踩踩踩踩踩踩')
pdf.output('example1.pdf', dest='F'
           )
# pdf = MyPDF(orientation='P', unit='mm', format='A4')
# pdf.add_font('youyuan', '', r'F:\ContentPro\PythonPro\automaticoffice\字体\youyuan.TTF', True)
# pdf.add_page()
# pdf.set_font("youyuan", size=12)
#
# print(pdf.w)
# print(pdf.h)
# # pdf.multi_cell(pdf.w, pdf.h,
# pdf.cell(0, 6, "ddddddddddddddddddd")
# # pdf.cell(0, 6, "华沙")
# # pdf.set_title('好好学习')
# #
# # pdf.cell(0, 6, "two", 0, ln=0, align="R")
# # pdf.cell(0, 6, "three", 0,ln=0, align="L")
# # pdf.cell(0, 6, "four", 0,ln=1, align="R")
# pdf.write(h=1000, txt='我是的是的')
# # pdf.footer()
# print(1111111111)
# pdf.output("simple_demo.pdf")
# pdf.close()
# pdf = MyPDF(orientation='P', unit='mm', format='A4')
# # author = '陈子晴'.encode('latin-1')
# # print(author)
# # pdf.set_author(author=author)
# pdf.set_creator(creator="chen")
# pdf.set_keywords('sky ocean chen ')
# pdf.set_title('dfadfasdfasd')
# pdf.output('as.pdf', 'F')  # 保存文件
# pdf.close()  # 关闭
