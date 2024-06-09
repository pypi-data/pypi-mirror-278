import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesURL import BluesURL  
from util.BluesConsole import BluesConsole   
from config.BluesConfig import BluesConfig   

# 提供Cookie相关功能
class BluesCookie():
 
  def __init__(self,driver):
    self.driver = driver

  def get(self,name=''):
    '''
    @description : get one cookie
    @param {str} name : cookie name
    @returns {dict} 形如：{'domain': 'mp.163.com', 'httpOnly': True, 'name': 'NTESwebSI', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '2A7C7F8FCD65F7D74650E13D349C60CC'}
    '''
    return self.driver.get_cookie(name)

  def get_all(self):
    '''
    @description : get all cookies
    @returns {dict[]} 形如：[{'domain': 'mp.163.com', 'httpOnly': True, 'name': 'NTESwebSI', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '2A7C7F8FCD65F7D74650E13D349C60CC'}]
    '''
    return self.driver.get_cookies()
      
  '''
  @description 添加cookie
  @param {dict} cookie 字典形式的cookie对象，至少包含(其他元素自动填充默认)：
    - name
    - value
    - domain 尽量都设置为一级域名
  '''
  def set(self,cookie):
    if cookie.get('name') and ('value' in cookie):
      self.driver.add_cookie(cookie)

  '''
  @description 删除cookie
  @param {string} name cookie name
  '''
  def remove(self,name=''):
    return self.driver.delete_cookie(name)
  
  def clear(self):
    return self.driver.delete_all_cookies()

  def add_cookies(self,cookies):
    '''
    @description : add cookie from string or dict
    @param {str|dict}: 
     - 'BIDUPSID=77884ECAEE62BDD2A4A723BEF544DCB2; PSTM=1715957318'
     - {'BIDUPSID':'77884ECAEE62BDD2A4A723BEF544DCB2', 'PSTM':'1715957318'}
    @returns {None}
    '''
    if type(cookies) == str:
      cookie_dict = self.get_cookie_dict(cookies)
    else:
      cookie_dict = cookies

    if not cookie_dict:
      return 

    main_domain = BluesURL.get_main_domain(self.driver.current_url)
    for key,value in cookie_dict.items():
      self.set({
        'name':key,
        'value':str(value), # value's type must be string
        'domain':'.%s' % main_domain, # set main domain
        'expires': '',
        'path': '/',
        'httpOnly': False,
        'HostOnly': False,
        'Secure': False
      })
    
  def get_cookie_dict(self,cookies):
    '''
    @description : convert cookie str to dict
    @param {str}: 
     - 'BIDUPSID=77884ECAEE62BDD2A4A723BEF544DCB2; PSTM=1715957318'
    @returns {dict}
    '''
    if not cookies:
      return None

    cookie_dict = {}
    cookie_list = cookies.split(';')
    for k_v in cookie_list:
      if not k_v:
        continue
      kv=k_v.split('=')
      if not kv[0] or len(kv)<2:
        continue
      key = kv[0].strip()
      value = kv[1].strip()
      cookie_dict[key]=value
    return cookie_dict
