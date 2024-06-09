from selenium.webdriver.support.select import Select
from .BluesElement import BluesElement

# 提供下拉选择相关功能
class BluesSelecter():
 
  def __init__(self,driver):
    self.driver = driver
    self.element_action = BluesElement(driver)
  
  def get_options(self,selector):
    '''
    @description 获取select选项/选中对象list
    @param {str} selector
    @returns {list}
    '''
    locator = self.element_action.wait(selector)
    options = Select(locator).options
    if options:
      return self.__get_option_items(options)
    else:
      return None
      
  def get_selected_options(self,selector):
    locator = self.element_action.wait(selector)
    options = Select(locator).all_selected_options
    if options:
      return self.__get_option_items(options)
    else:
      return None

  def get_frist_selected_option(self,selector):
    locator = self.element_action.wait(selector)
    option = Select(locator).first_selected_option # return WebElement
    if option:
      return self.__get_option_items([option])[0]
    else:
      return None

  def __get_option_items(self,option_elements):
    items = []
    for option in option_elements:
      items.append({
        'value':option.get_attribute('value'),
        'text':option.text,
      })
    return items

  def select_by_index(self,selector,index=0):
    '''
    @descrition : set a value as the selected value
    @param {int} index 
    '''
    locator = self.element_action.wait(selector)
    return Select(locator).select_by_index(index)
  
  def select_by_value(self,selector,value=''):
    locator = self.element_action.wait(selector)
    return Select(locator).select_by_value(value)

  def select_by_text(self,selector,text=''):
    locator = self.element_action.wait(selector)
    return Select(locator).select_by_visible_text(text)

  def deselect_all(self,selector):
    locator = self.element_action.wait(selector)
    return Select(locator).deselect_all()
    
  def deselect_by_index(self,selector,index=0):
    '''
    @descrition : Change the status to unselected
    @param {int} index 
    '''
    locator = self.element_action.wait(selector)
    return Select(locator).deselect_by_index(index)
  
  def deselect_by_value(self,selector,value=''):
    locator = self.element_action.wait(selector)
    return Select(locator).deselect_by_value(value)

  def deselect_by_text(self,selector,text=''):
    locator = self.element_action.wait(selector)
    return Select(locator).deselect_by_visible_text(text)


