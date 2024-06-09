import sys,os,re,time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions 
from .BluesWaiter import BluesWaiter   

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesConsole import BluesConsole  

# 提供元素选择功能
class BluesElement():

  def __init__(self,driver):
    self.driver = driver
    self.wait_action = BluesWaiter(driver) 

  # === part 1:  find element === #
  def wait(self,selector,is_visible_required=False,timeout=5):
    '''
    @description : wait and return a WebElement
    @param {str}  selector : css selector
    @param {bool} is_visible_required : Whether the element is required to be visible
    @param {int} timeout : Maximum waiting time (s)
    @returns {WebElement} 
    '''
    if is_visible_required:
      return self.wait_action.to_be_visible(selector,timeout)
    else:
      return self.wait_action.to_be_presence(selector,timeout)

  def wait_all(self,selector,timeout=5):
    '''
    @desction : wait and return all of the matched elements
    @returns {Array<WebElement>}
    '''
    return self.wait_action.all_to_be_presence(selector,timeout)

  def find(self,selector,parent=None):
    '''
    @description : get the first WebElement, if none exists, an exception is thrown - dont't wait 1 second
    @param {str} selector : css selector
    @param {WebElement} parent : find element from where (default is driver)
    @returns {WebElement}
    '''
    parent = parent if parent else self.driver
    return parent.find_element(By.CSS_SELECTOR,selector)

  def find_all(self,selector,parent=None):
    '''
    @description : get the first WebElement, if none exists, return empty list - dont't wait 1 second
    @param {str} selector : css selector
    @returns {WebElement[] | []}
    '''
    parent = parent if parent else self.driver
    return parent.find_elements(By.CSS_SELECTOR,selector)

  # === part 2:  get element info === #
  def get_attr(self,selector,key):
    '''
    @description : get element's attribute
    @param {str} selector : css selector
    @param {str} key : attribute name, all HTML DOM attributes can be accessed
      - innerHTML
      - innerText
    @returns {str}
    '''
    web_element = self.wait(selector)
    return web_element.get_attribute(key)

  def get_text(self,selector):
    web_element = self.wait(selector)
    return web_element.text

  def get_css(self,selector,key):
    '''
    @description : get a element's css property value
    '''
    web_element = self.wait(selector)
    return web_element.value_of_css_property(key)
  
  # === part 3:  get element by link text === #
  def find_link(self,link_text,is_partial=True):
    '''
    @description : 根据 a元素的内容查找元素
     - 不受隐藏在在屏外限制
     - 如果不在屏内，会自动滚动到屏内
    @param {str} link_text ：链接内可视文本
    '''
    if is_partial:
      return self.driver.find_element(By.PARTIAL_LINK_TEXT,link_text)
    else:
      return self.driver.find_element(By.LINK_TEXT,link_text)
    
  # === part 4: get element's status, don't wiat === #
  def is_displayed(self,selector):
    web_element = self.find(selector)
    return web_element.is_displayed()

  def is_enabled(self,selector):
    # weather a input can't be input
    web_element = self.find(selector)
    return web_element.is_enabled()

  def is_selected(self,selector):
    # only used to radio and checkbox
    web_element = self.find(selector)
    return web_element.is_selected()

  def is_displayed(self,selector):
    web_element = self.find(selector)
    return web_element.is_displayed()

