# 提供窗口相关功能
class BluesWindow():
 
  def __init__(self,driver):
    self.driver = driver
  
  def shot(self,file=None):
    '''
    @description : shot screen as a file
    @param {str} file : File save address
    @returns {None} 
    '''
    file_path = file if file else self.__get_default_file()
    shot_status = self.driver.save_screenshot(file_path)
    return file_path if shot_status else ''

  def shot_base64(self):
    '''
    @description : shot screen as base64 string
    @returns {str} : base64 string
    '''
    return self.driver.get_screenshot_as_base64()

  def __get_default_file(self,prefix='screenshot'):
    timestamp = int(time.time()) 
    return './%s-%s.png' % (prefix,timestamp)

  def get_size(self):
    '''
    @descripton : get current window's size
    @returns {dict} : {'width': 1755, 'height': 946}
    '''
    return self.driver.get_window_size()

  def resize(self,size):
    '''
    @description 修改窗口尺寸
    @param {tuple|list} size (width,height)
    '''
    self.driver.set_window_size(*size)

  def maximize(self):
    '''
    @description : maximize
    '''
    self.driver.maximize_window()

  def minimize(self):
    '''
    @description : hide the chrome window
    '''
    self.driver.minimize_window()

  def fullscreen(self):
    '''
    @description : maximize and hide the tabs
    '''
    self.driver.fullscreen_window()

  def position(self,position):
    '''
    @description 修改窗口位置
    @param {tuple} position (x,y)
    '''
    self.driver.set_window_position(*position)
     
  def refresh(self):
    self.driver.refresh()
      
  def back(self):
    self.driver.back()
      
  def forward(self):
    self.driver.forward()
