import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from .BluesElement import BluesElement

# 提供元素拖拽功能
class BluesMover():
  def __init__(self,driver):
    self.driver = driver
    self.element_action = BluesElement(driver)
    self.chains = ActionChains(driver)

  
  def move_to(self,selector):
    '''
    @description : move the mouse to the element, it will scroll the page if needed
      the mouse pointer is invisible on browser page
    '''
    locator = self.element_action.wait(selector)
    self.chains.move_to_element(locator).perform()

  def move_offset(self,x,y):
    '''
    @description : move by offset 
    @param {tuple} offset : (x,y)
    '''
    self.chains.move_by_offset(x,y).perform()

  '''
  @description 按坐标(左上角)移动
  @param {str} selector driver元素
  @params {tuple} position (x,y) 左上角的坐标
  '''
  def position(self,selector,position):
    locator = self.element_action.wait(selector)
    args = (locator ,position[0],position[1])
    self.chains.drag_and_drop_by_offset(*args).perform()

  '''
  @description 按指定偏移量移动
  @param {str} selector driver元素
  @params {tuple} offset (offset_x,offset_y) 移动的尺寸（注意不是坐标），负数是向左/上移动
  '''
  def offset(self,selector,offset):
    coordinate = self.get_coordinate(selector)
    position = (coordinate[0]+offset[0],coordinate[1]+offset[1])
    self.position(selector,position)

  '''
  @description 滑块移动到容器右侧
  @param {str} target : the target container element's css selector
  @param {str} slider : css selector
  '''
  def slide(self,target,slider,direction='right'):
    # 获取容器右侧坐标
    target_coordinate = self.get_coordinate(target)
    slider_coordinate = self.get_coordinate(slider)
    x = slider_coordinate['left'] # init x-axis position
    y = slider_coordinate['top'] # init y-axis position

    if direction == 'left' or direction == 'right':
      x = target_coordinate[direction] 
    elif direction == 'top' or direction == 'bottom':
      y = target_coordinate[direction] 

    self.position(slider,(x,y))

  def center(self,target,slider):
    '''
    @description 滑块移动到容器内(默认到容器中间)
    @param {str} target : the target container element's css selector
    @param {str} slider : css selector
    '''
    target_locator = self.element_action.wait(target)
    slider_locator = self.element_action.wait(slider)
    # the first arg is the slided element
    self.chains.drag_and_drop(slider_locator,target_locator).perform()

  def get_coordinate(self,selector):
    '''
    @description : get element's position and size, the positon is base on window
    @param {str} selector : css selector
    @returns {dict}
    '''
    coordinate = {}
    locator = self.element_action.wait(selector)
    coordinate['left'] = locator.location.get('x')
    coordinate['top'] = locator.location.get('y')
    coordinate['width'] = locator.size.get('width')
    coordinate['height'] = locator.size.get('height')
    coordinate['right'] = coordinate['left']+coordinate['width']
    coordinate['bottom'] = coordinate['top']+coordinate['height']
    return coordinate


