from .BluesElement import BluesElement

# 提供frame相关功能
class BluesFrame():
 
  def __init__(self,driver):
    self.driver = driver
    self.element_action = BluesElement(driver)

  '''
  @description frame 窗口切换
  @param {str} frame_selector : iframe selector
  '''
  def switch_to(self,frame_selector):
    locator = self.element_action.wait(frame_selector)
    self.driver.switch_to.frame(locator)
      
  def quit(self):
    '''
    @description : back to the default partent window
    '''
    self.driver.switch_to.default_content()

  def wrap(self,frame_selector,callback):
    '''
    @description : switch to iframe, execute the callback, then back to main window
    @param {str} frame_selector : iframe's css selector
    @param {function} callback : ececute in the iframe window
    '''
    self.switch_to(frame_selector)
    callback()
    self.quit()
      
  



