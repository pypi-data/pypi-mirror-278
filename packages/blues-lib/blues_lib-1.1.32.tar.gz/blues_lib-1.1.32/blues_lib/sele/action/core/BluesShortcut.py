import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from .BluesElement import BluesElement
from .BluesForm import BluesForm 

class BluesShortcut():

  SHORTCUTS={
    'select':Keys.CONTROL+"A",
    'copy':Keys.CONTROL+"C",
    'paste':Keys.CONTROL+"V",
    'cut':Keys.CONTROL+"X", # 拼接为同时使用
    'clear':Keys.DELETE, # 元组元素为依次使用
    'enter':Keys.ENTER,
    'f12':Keys.F12,
    'arrow_down':Keys.ARROW_DOWN,
    'arrow_up':Keys.ARROW_UP,
    'page_down':Keys.PAGE_DOWN,
    'page_up':Keys.PAGE_UP,
  }

  def __init__(self,driver):
    self.driver = driver
    self.element_action = BluesElement(driver)
    self.form_action = BluesForm(driver)
    self.chains = ActionChains(driver)

  # 测试无效
  def control(self,key=''):
    self.chains.key_down(self.SHORTCUTS['control']).send_keys(key).key_up(self.SHORTCUTS['control']).perform()

  def select(self,selector):
    self.form_action.write_after(selector,self.SHORTCUTS['select'])

  def deselect(self,selector):
    web_element = self.element_action.wait(selector)
    web_element.click()

  # Instructions must be entered multiple times
  def copy(self,selector):
    self.select(selector)
    self.form_action.write_after(selector,self.SHORTCUTS['copy'])

  def cut(self,selector):
    self.select(selector)
    self.form_action.write_after(selector,self.SHORTCUTS['cut'])

  def paste(self,selector):
    self.form_action.write_after(selector,self.SHORTCUTS['paste'])
  
  def paste_after(self,selector):
    self.deselect(selector)
    self.paste(selector)

  def clear(self,selector):
    self.select(selector)
    self.form_action.write_after(selector,self.SHORTCUTS['clear'])

  def enter(self,selector):
    # must set a selector or enter envent is noneffective
    self.form_action.write_after(selector,self.SHORTCUTS['enter'])
  
  def f12(self,selector):
    self.form_action.write_after(selector,self.SHORTCUTS['f12'])
    #self.chains.send_keys(self.SHORTCUTS['f12']).perform()
  
  def arrow_up(self,count=1,interval=1):
    '''
    @description : press arrow up
    @param {int} count : how many times to move
    @param {init} interval : The interval time between moves
    '''
    for i in range(count):
      if interval:
        time.sleep(interval)
      self.chains.send_keys(self.SHORTCUTS['arrow_up']).perform()

  def arrow_down(self,count=1,interval=1):
    for i in range(count):
      if interval:
        time.sleep(interval)
      self.chains.send_keys(self.SHORTCUTS['arrow_down']).perform()
  
  def page_up(self,count=1,interval=1):
    for i in range(count):
      if interval:
        time.sleep(interval)
      self.chains.send_keys(self.SHORTCUTS['page_up']).perform()

  def page_down(self,count=1,interval=1):
    for i in range(count):
      if interval:
        time.sleep(interval)
      self.chains.send_keys(self.SHORTCUTS['page_down']).perform()

  def select_asso_option(self,selector,text,index=0):
    # input text to show associative options
    self.form_action.write(selector,text)
    time.sleep(1)
    self.arrow_down(index+1)
    self.enter(selector)