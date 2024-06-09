import sys,os,re,subprocess,time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesPowerShell import BluesPowerShell 
from sele.action.BluesAction import BluesAction  
from sele.script.BluesScript import BluesScript 
from sele.parser.BluesParser import BluesParser  

class BluesChrome():

  CONFIG = {
    'url':'https://www.baidu.com', # default open web page
    'jquerization':False, # 是否默认引入jquery
  }

  # https://peter.sh/experiments/chromium-command-line-switches/
  ARGUMENTS = {
    #'--headless':'', # headless mode
    '--start-maximized':'',
    '--no-default-browser-check':'',
    '--disable-notifications':'',
    #'--disable-web-security':'', # 禁用此项，会导致debug模式下也无法存储登录信息
    #'--ignore-certificate-errors':'',
    '--disable-infobars':'',
    '--hide-crash-restore-bubble':'', # 是否打开崩溃前的页面
    '--disable-popup-blocking':'',
    '--disable-extensions-api':'', 
    '--disable-application-install-prompt':'',
    '--no-first-run':'', 
    '--disable-first-run-ui':'',
  }

  EXPERIMENTAL_OPTIONS = {
    'detach':True,
    'prefs' : {
      # 0 - Default, 1 - Allow, 2 - Block
      "profile.default_content_setting_values.notification": 2,
      # Removing the webdriver property from the navigator object,so the browser could not distinguish whether for robots
      "Page.addScriptToEvaluateOnNewDocument":{
        "source": """
          Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
          })
        """
      }
    }
  }

  def __init__(self,config={},arguments={},experimental_options={}):
    '''
    @description : Get a Chrome Driver instance
    @param {dict} config
    '''
    self.before_created(config,arguments,experimental_options)
    self.created()
    self.after_created()

  def before_created(self,config,arguments,experimental_options):
    self.driver = None
    self.action = None
    self.config = {**self.CONFIG,**config}
    self.arguments = {**self.ARGUMENTS,**arguments} 
    # connect to a exist chrome, can't set detach and prefs options
    if experimental_options.get('debuggerAddress'):
      self.experimental_options = experimental_options
    else:
      self.experimental_options = {**self.EXPERIMENTAL_OPTIONS,**experimental_options}
    self.chrome_driver_exe = BluesPowerShell.get_env_value('CHROME_DRIVER_EXE')

  def created(self):
    '''
    @description : create the driver and action instance
    '''
    chrome_service = self.__get_service()
    chrome_options = self.__get_options()
    web_driver = self.get_driver_creator()
    self.driver = web_driver.Chrome( service = chrome_service, options = chrome_options)
    # 页面加载超时时间, by default is 0 : no time limit
    self.driver.set_page_load_timeout(60*5)
    # js脚本执行超时时间，just for execute_async_script，If the callback is not called within the time limit, it will result in a timeout exception
    self.driver.set_script_timeout(60*5)
    self.action = BluesAction(self.driver)  
    self.script = BluesScript(self.driver)  
    self.parser = BluesParser(self.driver)  

  def after_created(self):
    '''
    @description : do some settings after the driver was created
     provide a hook to make subclass to insert private logic
    '''
    url = self.config.get('url')
    if url:
      self.driver.get(url)
  
  def quit(self):
    self.__close_alert()
    # must close alert first ,then cant determine weather the current_url is exists
    if not self.has_quitted():
      self.driver.quit()

  def has_quitted(self):
    try:
      self.driver.current_url
      return False
    except Exception as e:
      return True

  def close(self):
    self.__close_alert()
    if not self.has_quitted():
      self.driver.close()

  def __close_alert(self):
    '''
    @description : if the alert is  presence, quit and close can't quit the browser,just close the alert
    '''
    if self.action.waiter.alert_to_be_presence():
      self.action.alert.accept()

  def get_driver_creator(self):
    '''
    @description : get the webdirver isntance, it will be cover by subclass BluesProxyChrome
    '''
    return webdriver

  def __get_options(self):
    chrome_options = ChromeOptions()
    
    for key,value in self.arguments.items():
      arg_value = '%s=%s' % (key,value) if value else key
      chrome_options.add_argument(arg_value)

    for key,value in self.experimental_options.items(): 
      chrome_options.add_experimental_option(key,value)

    return chrome_options

  def __get_service(self):
    executable_path=self.chrome_driver_exe if self.chrome_driver_exe else ChromeDriverManager().install()
    return ChromeService(executable_path) 



