import time
from .BluesElement import BluesElement

# 提供窗口相关功能
class BluesDocument():
 
  def __init__(self,driver):
    self.driver = driver
    self.element = BluesElement(driver)
  
  def shot(self,selector,file=None):
    '''
    @description 指定元素截图,不支持base64格式
    @param {str} selector : css selector 
    @param {str} file 保存位置
    @returns {str} file_path
    '''
    file_path = file if file else self.__get_default_file('elementshot')
    locator = self.element.wait(selector)
    shot_status = locator.screenshot(file_path)
    return file_path if shot_status else ''

  def __get_default_file(self,prefix='elementshot'):
    timestamp = int(time.time()) 
    return './%s-%s.png' % (prefix,timestamp)

  def get_attr(self,key):
    '''
    @descripton : get current document's info
    @param {str} key 
      - current_url
      - title
      - name
      - page_source
    '''
    return getattr(self.driver,key,'')


  