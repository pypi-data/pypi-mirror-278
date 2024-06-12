# -*- coding: utf-8 -*-
"""
@Time : 2023/12/16 22:09 
@项目：爬虫使用
@File : xml_parse.by
@PRODUCT_NAME :PyCharm
"""
import xmltodict
import json

"""
案例
import requests
import xmltodict
headers = {
}
url = "https://boyyongxin.github.io/atom.xml"
response = requests.get(url, headers=headers,verify=False)
xml_str = response.text
new_dict_obj = xmltodict.parse(xml_str)
print(new_dict_obj)
"""
xml_str = '''
<bookstore>
  <book category="COOKING">
      <title lang="en">Everyday Italian</title>
      <author>Giada De Laurentiis</author>
      <year>2005</year>
      <price>30.00</price>
  </book>
  <book category="CHILDREN">
      <title lang="en">Harry Potter</title>
      <author>J K. Rowling</author>
      <year>2005</year>
      <price>29.99</price>
  </book>
  <book category="WEB">
      <title lang="en">Learning XML</title>
      <author>Erik T. Ray</author>
      <year>2003</year>
      <price>39.95</price>
  </book>
</bookstore>
'''


class XmlParse(object):
    def __init__(self, data):
        self.data = data

    def xml_to_dict(self):
        new_dict_obj = xmltodict.parse(self.data)  # 返回一个OrderedDict类型的对象
        json_str = json.dumps(new_dict_obj)  # 使用内置的json模块转换成json
        return json_str

    def dict_to_xml(self):
        new_xml = xmltodict.unparse(self.data)  # 这里直接放dict对象
        print(new_xml)
