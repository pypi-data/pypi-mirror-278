from setuptools import setup, find_packages

version = '0.1.0'  # Any format you want
DESCRIPTION = 'Easily cut the basic type by file_operation'
AUTHOR = "SkyOceanChen"  # 留下大名
AUTHOR_EMAIL = "skyoceanchen@foxmail.com"  # 留下邮箱
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    # 要显示的唯一标识（用于pip install xxx）
    name='file_operation',
    # py_modules=['pgzero_template'],#上传单个文件的时候可以使用这个 是库名，在里面填写你的库文件名即可。
    # 使用find_packages()自动发现项目中的所有包,如果不想使用所有的包，那么可以手动指定例如：packages=[‘package1’, ‘package2’, ‘package3’]
    packages=find_packages(),

    include_package_data=True,  # 打包包含静态文件标识！！上传静态数据时有用
    version=version,  # 版本号
    description='Short description',  # '包的简介描述'
    long_description_content_type="text/markdown",  # 包的详细介绍(一般通过加载README.md)
    long_description=long_description,  ## 长描述设置为README.md的内容
    author=AUTHOR,  # 作者
    author_email=AUTHOR_EMAIL,  # 作者的电子邮件
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    url='https://gitee.com/SkyOceanchen/file_operations.git',  # 项目开源地址
    keywords=['basic_type', 'python', ],
    # 许可协议
    license='MIT',
    # PLATFORMS=["all", ],  # 支的乎台，如所有乎台超支，可以葵 aLLall'
    # 要安装的依赖包 ['py-L>=0.12.0', 'ter==3.1.0'],  # 指定了当前软件包所依赖的其他python类库。这些指定的python类库将会在本package被安装的时候一并被安装
    install_requires=[
        "pdfkit==1.0.0",
        "pyyaml",
        "xlwt==1.3.0",
        "basic_type_operations",
        "pandas==2.0.2",
        "openpyxl==3.1.2",
        "patool==1.12",
        "filetype==1.2.0",
        "pillow==9.5.0",
        "qrcode==7.4.2",
        "django==4.2.3",
        "docx2pdf==0.1.8",
        "reportlab==4.1.0",
        # All external pip packages you are importing
    ],
    classifiers=[  # 关于包的其他元数据(metadata)
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',  # 与操作系统无关
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # 根据MIT许可证开源
        'Programming Language :: Python :: 3.6',  # 该软件包仅与Python3兼容
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='~=3.3'  # 大于等于3.3，但是不能超过4
)
"""
setup.py中的python_requires='>=3' 为要求python版本>=3，如果有更细致的要求写法：
# 大于等于3
python_requires='>=3'
# 大于等于3.3，但是不能超过4
python_requires='~=3.3'
# 不能用3.1,3.2
python_requires='!=3.1.*, !=3.2.*'

"""
"""
python setup.py bdist_wheel sdist
twine upload dist/*
SkyOceanChen/CHENziqing527#
"""
"""
[pypi]
  username = __token__
  password = 
pypi-AgEIcHlwaS5vcmcCJGVkZTQwNTU1LWY5NzQtNDgzZS04OGY2LTUxMDM0YmVlZDBhZgACKlszLCI5MzI5N2UxMi04MjZhLTQ1MzMtOWZkYi0yZjA3N2E5ZTc5YzIiXQAABiAVpjcCBcICbQrRME30zbngnWE8apTLKrTFwni953wzlw
"""