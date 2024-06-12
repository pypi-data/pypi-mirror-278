from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

VERSION = '0.0.10'
DESCRIPTION = 'scAGDE Python package'

# 配置
setup(
       # 名称必须匹配文件名 'verysimplemodule'
        name="scAGDE",
        version=VERSION,
        author="Gaoyang Hao",
        author_email="<haogy22@mails.jlu.edu.cn>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        packages=find_packages(),
        url="https://github.com/Hgy1014/scAGDE",
        install_requires=[], # add any additional packages that 
        # 需要和你的包一起安装，例如：'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)