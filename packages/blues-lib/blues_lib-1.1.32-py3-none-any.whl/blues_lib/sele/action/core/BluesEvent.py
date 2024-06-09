
from selenium.webdriver import ActionChains
from .BluesElement import BluesElement
from .BluesShortcut import BluesShortcut 

class BluesEvent():
  def __init__(self,driver):
    self.driver = driver
    self.element_action = BluesElement(driver)
    self.shortcut = BluesShortcut(driver)
    self.chains = ActionChains(driver)

  def click(self,selector):
    '''
    @description 单击
    @param {str} selector
    '''
    locator = self.element_action.wait(selector)
    self.chains.click(locator).perform()
  
  def hold(self,selector):
    '''
    @description 点击按住不放
    @param {str} selector
    '''
    locator = self.element_action.wait(selector)
    self.chains.click_and_hold(locator).perform()

  def release(self,selector):
    '''
    @description 释放按下的鼠标
    @param {str} selector
    '''
    locator = self.element_action.wait(selector)
    self.chains.release(locator).perform()

  def right_click(self,selector):
    '''
    @description 右击
    @param {str} selector
    '''
    locator = self.element_action.wait(selector)
    self.chains.context_click(locator).perform()

  # 测试无效，无法触发菜单选项
  def right_click_menu(self,selector,index=0):
    '''
    @description : right click and select a menu to enter
    @param {str} selector : the element where right click
    @param {int} index : the selected menu index
    '''
    self.right_click(selector)
    self.shortcut.arrow_down(index+1)
    self.shortcut.enter('body')

  def double_click(self,selector):
    '''
    @description 双击
    @param {str} selector
    '''
    locator = self.element_action.wait(selector)
    self.chains.double_click(locator).perform()

  def hover(self,selector):
    '''
    @description 鼠标移入元素，悬浮上方
    @param {str} selector
    '''
    locator = self.element_action.wait(selector)
    self.chains.move_to_element(locator).perform()

