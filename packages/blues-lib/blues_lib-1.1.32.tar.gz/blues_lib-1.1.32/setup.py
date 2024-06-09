from setuptools import setup,find_packages

setup(
  name="blues_lib", # package name
  version="1.1.32", # package version
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  packages=find_packages(), # package module
  # add from requirement.txt,本地测试注释所有包，不能从镜像立即安装
  install_requires=[
    #'Pillow>=10.3.0',
    #'Requests>=2.31.0',
    #'selenium>=4.20.0',
    #'selenium_wire>=5.1.0',
    #'setuptools>=47.1.0',
    #'webdriver_manager>=4.0.0',
  ] # package dependency
)