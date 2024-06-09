import sys,os,re
from .BluesJavaScript import BluesJavaScript
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.action.core.BluesWaiter import BluesWaiter  

class BluesJQuery():

  JQUERY_CDN = 'https://libs.baidu.com/jquery/2.0.0/jquery.min.js'

  def __init__(self,driver):
    self.driver = driver
    self.waiter = BluesWaiter(driver)
    self.javascript = BluesJavaScript(driver)

  def is_loaded(self):
    js_script = 'return window.jQuery!=null;'
    return self.javascript.execute(js_script)

  def wait_to_load(self):
    # the wait func must receive the driver param
    def wait_func(driver):
      js_script = 'return window.jQuery!=null;'
      return self.driver.execute_script(js_script)
    return self.waiter.wait_for(wait_func)
  
  def load(self,jquery_url=''):
    url = jquery_url if jquery_url else self.JQUERY_CDN
    self.javascript.load(url)
