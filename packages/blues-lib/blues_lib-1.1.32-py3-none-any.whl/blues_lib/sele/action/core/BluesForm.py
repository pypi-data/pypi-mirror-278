import time
from selenium.webdriver.common.keys import Keys
from .BluesElement import BluesElement

class BluesForm():

  def __init__(self,driver):
    self.driver = driver
    self.element_action = BluesElement(driver)
   
  def __input(self,selector,texts,clear=False):
    '''
    @description : type text
    @param {str} selector : css selector
    @param {str|tuple|list} texts
    '''
    web_element = self.element_action.wait(selector)
    if clear:
      web_element.clear()
    input_texts = (texts,) if type(texts)==str else texts 
    web_element.send_keys(*input_texts)

  def write(self,selector,texts):
    '''
    @description : type text
    @param {str} selector : css selector
    @param {str|tuple|list} texts
    '''
    self.__input(selector,texts,True)

  def write_after(self,selector,texts):
    self.__input(selector,texts)
  
  def write_file(self,selector,texts):
    self.__input(selector,texts)

  def clear(self,selector):
    web_element = self.element_action.wait(selector)
    web_element.clear()
