from .browser.BluesChrome import BluesChrome 
from .browser.BluesDebugChrome import BluesDebugChrome
from .browser.BluesProxyChrome import BluesProxyChrome
from .browser.BluesCookieChrome import BluesCookieChrome 

class BluesBrowser():

  @classmethod
  def chrome(cls,config={},arguments={},experimental_options={}):
    return BluesChrome(config,arguments,experimental_options)
  
  @classmethod
  def debug_chrome(cls,config={},arguments={},experimental_options={}):
    return BluesDebugChrome(config,arguments,experimental_options)
  
  @classmethod
  def proxy_chrome(cls,config={},arguments={},experimental_options={}):
    return BluesProxyChrome(config,arguments,experimental_options)

  @classmethod
  def cookie_chrome(cls,config={},arguments={},experimental_options={}):
    return BluesCookieChrome(config,arguments,experimental_options)