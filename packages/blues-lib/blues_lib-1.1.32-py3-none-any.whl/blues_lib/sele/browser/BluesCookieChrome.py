
import sys,os,re,time
from .BluesChrome import BluesChrome

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesFiler import BluesFiler  
from util.BluesURL import BluesURL   
from util.BluesConsole import BluesConsole   
from util.BluesPowerShell import BluesPowerShell    
from util.BluesDateTime import BluesDateTime     
from config.BluesConfig import BluesConfig    

class BluesCookieChrome(BluesChrome):

  def __init__(self,config={},arguments={},experimental_options={}):
    self.loginer_executor = BluesPowerShell.get_env_value('LOGINER_EXECUTOR')
    self.relogin_time = 0
    super().__init__(config,arguments,experimental_options)

    
  def after_created(self):
    self.config['url'] = self.config.get('login_url') # 使用superclass访问 url属性逻辑
    super().after_created()
    # open home page with cookie
    self.add_cookie_file_and_browse()

  '''
  @description : support to login by default cookie
  '''
  def add_cookie_and_browse(self,login_ur,loggedin_url,cookies=''):
    '''
    @description : get a page afater add cookies
    @param {dict|str} cookies
    '''
    self.driver.get(login_ur)
    time.sleep(1)
    if cookies:
      self.action.cookie.add_cookies(cookies) 

    time.sleep(1)
    self.driver.get(loggedin_url)

  def add_cookie_file_and_browse(self):
    login_url = self.config.get('login_url')
    loggedin_url = self.config.get('loggedin_url')
    cookie_file = self.config.get('cookie_file')
    login_selector = self.config.get('login_selector')

    default_file = BluesConfig.get_download_http_domain_file(self.driver.current_url,'txt')
    file_path = cookie_file if cookie_file else default_file
    if file_path:
      cookies = BluesFiler.read(file_path)
    else:
      cookies = ''
    
    BluesConsole.info(cookies,'Login by cookies')
    self.add_cookie_and_browse(login_url,loggedin_url,cookies)
    
    is_login = self.is_login(login_selector)
    if is_login:
      BluesConsole.success('The cookie in file %s is still valid. Logged in %s successfully' % (file_path,loggedin_url))
      return 
    BluesConsole.info('The cookie in file %s is invalid. Relogin %s now' % (file_path,login_url))
    
    # 使用cookie，必须重新启动一个客户端（有些网站-dayu有校验）
    self.quit() # close the browser

    if not self.loginer_executor:
      BluesConsole.error('The env variable LOGINER_EXECUTOR is missing!')   
      return 

    if self.relogin_time>0:
      BluesConsole.warn('Relogin failure, and you can only re-log in once')
      return

    # The current program will wait for the login program to complete
    result = self.relogin()
    if result['code'] == 200 and result['output'].find('500')==-1:
      BluesConsole.success('Relogin is complete, try using the latest cookie to access the loggedin url')
      # reopen the page
      self.created()
      # 之后需要从 current_url解析 domain
      self.driver.get(self.config.get('url'))
      self.add_cookie_file_and_browse() 
    else:
      BluesConsole.error('The site (%s) relogin failure: %s ; PS output: %s' % (login_url,result['message'],result['output']))
      self.quit()

  def is_login(self,login_selector,wait_time=3):
    '''
    @description : is login or not
    @param {str} login_selector : the css selector of a element in login page
    @param {int} wait_time : wait n seconds to wait document loaded
    @returns {boolean}
    '''
    if self.action.element.wait(login_selector,wait_time):
      return False 
    else:
      return True
  
  def relogin(self):
    main_domain = BluesURL.get_main_domain(self.config['url']) 
    self.relogin_time+=1
    if self.loginer_executor.endswith('.py'):
      ps_script = 'python %s %s' % (self.loginer_executor,main_domain)
    
    if self.loginer_executor.endswith('.exe'):
      ps_script = '%s %s ' % (self.loginer_executor,main_domain)

    BluesConsole.info('Relogin by : %s' % ps_script)

    return BluesPowerShell.execute(ps_script)

