import sys,os,re,time

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesType import BluesType 
from sele.script.BluesJavaScript import BluesJavaScript 

# 提供窗口相关功能
class BluesTab():
 
  def __init__(self,driver):
    self.driver = driver
    self.js_action = BluesJavaScript(driver)
  
  def get_handle(self):
    '''
    @description : get current active tab's handle id
    @returns {str} handle id, such as : 3D31BF6D96E5671253E70BCF33DC7F39
    '''
    return self.driver.current_window_handle

  # 所有窗口句柄 list
  def get_handles(self):
    '''
    @description : get all tab's handle id
    @returns {list} handle id, such as : ['3D31BF6D96E5671253E70BCF33DC7F39']
    '''
    return self.driver.window_handles

  def get_new_handle(self):
    '''
    @description : get the new opened tab
    '''
    return self.get_handles()[-1]

  def switch_to(self,handle):
    '''
    @description window窗口切换（切换浏览器tab页签）
    @param {string} handle 窗口句柄
    '''
    self.driver.switch_to.window(handle)

  def switch_to_latest(self):
    '''
    @description : switch window to the latest opened tab
    '''
    self.switch_to(self.get_new_handle())
  
  def switch_to_prev(self):
    '''
    @description : switch window to the prev tab
    '''
    handles = self.get_handles()
    current_handle_index = BluesType.last_index(handles,self.get_handle())
    if current_handle_index>0:
      prev_handle = handles[current_handle_index-1]
      self.switch_to(prev_handle)

  def switch_to_next(self):
    '''
    @description : switch window to the prev tab
    '''
    handles = self.get_handles()
    current_handle_index = BluesType.last_index(handles,self.get_handle())
    if current_handle_index<len(handles)-1:
      next_handle = handles[current_handle_index+1]
      self.switch_to(next_handle)

  def open_tab(self,url,name=''):
    self.js_action.open(url,name)
    self.switch_to_latest()
