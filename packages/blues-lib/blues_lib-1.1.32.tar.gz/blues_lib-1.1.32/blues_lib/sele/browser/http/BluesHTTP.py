import sys,os,re,json

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesFiler import BluesFiler  
from util.BluesURL import BluesURL   
from util.BluesConsole import BluesConsole
from config.BluesConfig import BluesConfig 

class BluesHTTP():
  def __init__(self,driver):
    self.driver = driver

  def get_messages(self,config={}):
    '''
    @description : get all http request and response message
    @param {dict} config
     - {int} max_count : the maximum number of request messages, -1 means infinity
     - {str} url_pattern : Only data that matches the url pattern is retrieved
     - {str} cookie_pattern : Only data that matches the cookie pattern is retrieved
     - {function} filter(message) : Only data that meets the filtering conditions is obtained
     - {bool} request_only : If true, without response's body
    @returns {dict[] | None}
    '''
    if not self.driver.requests:
      return None

    messages = []
    max_count = config.get('max_count',-1) # -1 indicates that all data is obtained
    url_pattern = config.get('url_pattern')
    message_filter = config.get('message_filter')
    request_only = config.get('request_only',False)

    for request in self.driver.requests:
      if not request.response:
        continue

      # filter by url_pattern
      if url_pattern:
        if not re.search(url_pattern,request.url):
          continue

      message = self.__get_message(request,request_only)
      # filter by user-defined func
      if message_filter:
        if not message_filter(message):
          continue
      # show the only url
      if max_count==1:
        BluesConsole.info(request.url,'Matched only url')

      messages.append(message)

      # break by max_count
      if max_count!=-1 and len(messages)>=max_count:
        break

    if messages:
      return messages
    else:
      BluesConsole.warn(('No matching http message was obtained!',config))
      return None

  def __get_message(self,request,request_only=False):
    return {
      'url':request.url, 
      'path':request.path, 
      'querystring':request.querystring, 
      'method':request.method, 
      'headers':dict(request.headers), 
      'cookie':self.__get_header_cookie(request.headers),
      'params':request.params, 
      'date':request.date.isoformat(), 
      #'cert':request.cert, 
      'body':self.__get_request_body(request.body), 
      'response':self.__get_response(request.response,request_only), 
    }

  def __get_request_body(self,body):
    return str(body, encoding='utf-8')

  def __get_response(self,response,request_only=False):
    res_message = {
      'status_code':response.status_code, 
      'reason':response.reason, 
      'headers':dict(response.headers), 
      'date':response.date.isoformat(), 
    }
    if not request_only:
      encoding = response.headers.get('Content-encoding', 'identity')
      body = decode(response.body, encoding)
      res_message['body'] = body

    return res_message

  def save_to_txt(self,content,file=''):
    default_file = BluesConfig.get_download_http_domain_file(self.driver.current_url,'txt')
    file_path = file if file else default_file
    return BluesFiler.write(file_path,content)

  def save_to_json(self,messages,file=''):
    '''
    @description : save messages to json file
    @param {any} messages
    @param {str} file : the json file's absolute path, If this value is empty:
      - the dir will be c:/blues_lib/download/cookie/
      - the file will be domain.json
    '''
    default_file = BluesConfig.get_download_http_domain_file(self.driver.current_url,'json')
    file_path = file if file else default_file
    try:
      BluesFiler.write_json(file_path,messages)
      return {
        'code':200,
        'message':'success',
        'file':file_path,
      }
    except Exception as e:
      return {
        'code':500,
        'message':'%s' % e,
      }

  def get_cookie_requests(self,config={}):
    '''
    @description : get all requets filter by cookie
    '''
    domain = BluesURL.get_main_domain(self.driver.current_url)
    def message_filter(message):
      if not re.search(domain,message['url']):
        return False

      cookie = message['cookie'] 
      if not cookie:
        return False

      cookie_pattern = config.get('cookie_pattern')
      if not cookie_pattern:
        return True

      if not re.search(cookie_pattern,cookie):
        return False

      return True

    if not config.get('message_filter'):
      config['message_filter'] = message_filter
    
    requests = self.get_messages(config)
    return requests if requests else None

  def __get_header_cookie(self,headers):
    if headers.get('cookie'):
      return headers.get('cookie')
    if headers.get('Cookie'):
      return headers.get('Cookie')
    if headers.get('COOKIE'):
      return headers.get('COOKIE')
    return ''


  