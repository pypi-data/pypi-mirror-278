import time
from .BluesWaiter import BluesWaiter

# Provides methods for handling three pop-ups
class BluesAlert():
 
  def __init__(self,driver):
    self.driver = driver
    self.wait = BluesWaiter(driver)

  '''
  @description frame 切换到alert，不区分三种弹框类型
  @returns {WebElement} alert对象
  '''
  def switch_to(self):
    if self.wait.alert_to_be_presence():
      return self.driver.switch_to.alert
    else:
      return None

  '''
  @description 接受-并关闭弹框,the driver will back to main window automatically
  @param {string} text prompt框输入文本
  '''
  def accept(self,text=None):
    alert = self.switch_to()
    if not alert:
      return
    if text!=None:
      alert.send_keys(text)
    alert.accept()
      
  '''
  @description 取消-并关闭弹框
  @param {string} text prompt框输入文本
  '''
  def dismiss(self,text=None):
    alert = self.switch_to()
    if not alert:
      return
    if text!=None:
      alert.send_keys(text)
    alert.dismiss()



