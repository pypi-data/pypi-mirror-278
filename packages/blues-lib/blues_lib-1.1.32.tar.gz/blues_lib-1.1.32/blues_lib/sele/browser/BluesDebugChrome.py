import sys,os,re,subprocess,time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesPowerShell import BluesPowerShell 
from sele.browser.BluesChrome import BluesChrome  

# debug模式下chrome被PS提前打开，不是由webdriver启动，wire无法实现代理
class BluesDebugChrome(BluesChrome):
  # cover the parent options.detach and prefs can't be set in debug mode
  EXPERIMENTAL_OPTIONS = {}

  def __init__(self,config={},arguments={},experimental_options={}):
    '''
    @description : Get a Chrome Driver instance
    @param {dict} config
    @param {list} arguments
    @param {dict} experimental_options
    '''
    self.chrome_exe = BluesPowerShell.get_env_value('CHROME_EXE')
    self.process_args=''
    self.__validate(arguments)
    super().__init__(config,arguments,experimental_options)

  def before_created(self,config,arguments,experimental_options):
    '''
    @description cover the parent method
    '''
    super().before_created(config,arguments,experimental_options)
    self.__set_args_options()
    self.__restart()

  def __validate(self,arguments):
    error = self.__get_env_error()
    if error:
      raise Exception(error)

    error = self.__get_args_error(arguments)
    if error:
      raise Exception(error)

  def quit(self):
    '''
    @description : close the driver ane the chrome, the driver.quit can't close the chrome that opened by ps script
      don't dirver.quit() or the user login session will be removed
    '''
    self.__close_chrome()

  def __get_env_error(self):
    if not self.chrome_exe:
      return 'Env vairable chrome_exe missing'
    else:
      return ''

  def __get_args_error(self,arguments):
    '''
    @description : Determines whether the entry is legal
    '''
    if not arguments.get('--user-data-dir'):
      return 'Parameter arguments.--user-data-dir missing'
      
    if not arguments.get('--remote-debugging-address'):
      return 'Parameter arguments.--remote-debugging-address missing'

    return ''

  def __set_args_options(self):
    args = ''
    for key,value in self.arguments.items():
      arg_value = '%s=%s' % (key,value) if value else key
      if key == '--remote-debugging-address':
        # must set port or the driver can't connect to the browser
        args+='--remote-debugging-port=%s' % value.split(':')[1]
      else:
        args+=' %s ' % arg_value
    
    self.process_args = args

    # cover the all default options (these default options can't be used to connect to a existed debuug chrome)
    self.experimental_options['debuggerAddress'] = self.arguments['--remote-debugging-address']

  def __close_chrome(self):
    BluesPowerShell.stop_process('chrome')

  def __restart(self):
    '''
    @description : repopen the specific chrome (stop all chrome processes)
    '''
    self.__close_chrome()
    result = BluesPowerShell.start_process(self.chrome_exe,self.process_args)
    if result['code']!=200:
      raise Exception('Chrome restart failure %s' % result['message'])

  