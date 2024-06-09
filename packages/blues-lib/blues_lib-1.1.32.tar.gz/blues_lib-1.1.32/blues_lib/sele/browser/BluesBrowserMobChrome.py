import sys,os,re,json
from seleniumwire import webdriver
from seleniumwire.utils import decode
from .BluesChrome import BluesChrome
from .http.BluesHTTP import BluesHTTP 

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesFiler import BluesFiler  
from util.BluesURL import BluesURL   
from util.BluesConsole import BluesConsole    

# browsermob is a http proxy
class BluesBrowserMobChrome(BluesChrome):
  # https://pypi.org/project/selenium-wire/
  def __init__(self,config={},arguments={},experimental_options={}):
    super().__init__(config,arguments,experimental_options)
    self.http = BluesHTTP(self.driver)

  def after_created(self):
    self.__set_wire()
    super().after_created()

  def __set_wire(self):
    wire = self.config.get('wire')
    if not wire:
      return
    for key,value in wire.items():
      setattr(self.driver,key,value)

  def get_driver_creator(self):
    '''
    @description : get the webdirver isntance
    '''
    return webdriver

  def get_messages(self,config={}):
    '''
    @description : get all request and response messges
    '''
    config['request_only']=False
    return self.http.get_messages(config)
  
  def save_messages(self,config,file=''):
    '''
    @description : save all request and response messges
    '''
    messages = self.get_messages(config)
    return self.http.save_to_json(messages,file)
    
  def get_requests(self,config={}):
    '''
    @description : get all http messages without response' body
    '''
    config['request_only']=True
    return self.http.get_messages(config)

  def save_requests(self,config,file=''):
    requests = self.get_requests(config)
    return self.http.save_to_json(requests,file)

  def get_cookie_requests(self,config={}):
    '''
    @description : get all requests filter by cookie
    '''
    config['request_only']=True
    return self.http.get_cookie_requests(config)

  def save_cookie_requests(self,config,file=''):
    requests = self.get_cookie_requests(config)
    return self.http.save_to_json(requests,file)

  def get_cookie(self,config={}):
    config['max_count']=1
    requests = self.get_cookie_requests(config)
    if not requests:
      return None
    return requests[0].get('cookie')
  
  def save_cookie(self,config={},file=''):
    cookie = self.get_cookie(config)
    return self.http.save_to_txt(cookie,file)

