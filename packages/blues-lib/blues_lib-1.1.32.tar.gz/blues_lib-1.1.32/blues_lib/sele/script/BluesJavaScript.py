import requests
from .BluesJavaScriptService import BluesJavaScriptService
# 提供js相关功能，不依赖jQuery
class BluesJavaScript():
  
  PLUGINS = {
    '$':'https://libs.baidu.com/jquery/2.0.0/jquery.min.js',
    #'_':'https://cdn.bootcdn.net/ajax/libs/lodash.js/4.17.21/lodash.core.js',
  }

  def __init__(self,driver):
    self.driver = driver

  def load_blues_service(self):
    js_script = BluesJavaScriptService.service_script
    self.execute(js_script)

  def load_plugins(self,plugins):
    '''
    @description : load relay plugin auto
    @param {dict} plugins 
      - key : the global var name
      - value : the plugin's cdn
    '''
    for plugin_var,plugin_cdn in plugins.items():
      if not self.is_var_exists(plugin_var):
        self.load(plugin_cdn)

  def execute(self,script,*args):
    '''
    @description 执行js代码
    @param {str} script : js script
    @param {tuple} args : the rest params
    @returns {any} the js script's return value
    '''
    return self.driver.execute_script(script,*args)

  def alert(self,*args):
    '''
    @description : alert
    @param {tuple} args : one or more string 
    '''
    js_script = '''
    var alert_str = '';
    if(arguments.length>0){
      for(var i=0;i<arguments.length;i++){
        alert_str+=' '+arguments[i];
      }
    }
    return alert(alert_str);
    '''
    self.execute(js_script,*args)
  
  def execute_async_script(self,script):
    '''
    @description async 执行js代码
    @param {str} script js脚本
    @returns {str} the js script's return value
    '''
    return self.driver.execute_async_script(script)

  def execute_online_script(self,url):
    '''
    @description : run the external script 
    @param {str} url : the script file path
    @returns {str} : the js return value
    '''
    response = requests.get(url = url)
    return self.execute(response.text)
  

  def html(self,selector,html=None):
    '''
    @description : get or set html
    @param {str} selector css选择器
    @param {str} html 写入文本或HTML
    @returns {str|None} return dom html when as getter
    '''
    if html==None:
      script = """
       return $('{}').html()
      """.format(selector)
    else:
      script = """
        $('{}').html('{}')
      """.format(selector,html)
    return self.execute(script)

  def text(self,selector,text=None):
    '''
    @description : get or set text
    @param {str} selector css选择器
    @param {str} text 
    @returns {str|None} return dom html when as getter
    '''
    if text==None:
      script = """
       return $('{}').text()
      """.format(selector)
    else:
      script = """
        $('{}').text('{}')
      """.format(selector,text)
    return self.execute(script)


  def value(self,selector,value=None):
    '''
    @description : set or get form controller's value
    '''
    if value==None:
      script = """
        return $('{}').val()
      """.format(selector)
    else:
      script = """
        $('{}').val('{}')
      """.format(selector,value)
    return self.execute(script)

  def html_after(self,selector,html):
    '''
    @description PM04 追加元素内容
    @param {str} selector css选择器
    @param {str} html 写入文本或HTML
    '''
    script = """
      $('{}').append('{}')
    """.format(selector,html)
    return self.execute(script)

  def text_after(self,selector,text):
    '''
    @description : append text 
    @param {str} selector css选择器
    @param {str} text 
    '''
    script = """
      $('{}').text($('{}').text()+'{}')
    """.format(selector,selector,text)
    return self.execute(script)


  def value_after(self,selector,value):
    '''
    @description : set form controller's value
    '''
    script = """
      $('{}').val($('{}').val()+'{}')
    """.format(selector,selector,value)
    self.execute(script)

  def attr(self,selector,key_or_items):
    '''
    @description : get or set element's attribute
    @param {str} selector : element's css selector
    @param {str|dict} key_or_items : 
      - str : getter , such as 'name'
      - dict : setter , such as {'data-a','1','data-b','2'}
    @returns {str|None} : return the attr's value in gtter
    '''
    if type(key_or_items) == str:
      # must use return or can't get the js return value
      script = "return document.querySelector('%s').getAttribute('%s')" % (selector,key_or_items)
    else:
      attrs=''
      for key,value in key_or_items.items():
        attrs+=".setAttribute('%s','%s')" % (key,value)
      script = "document.querySelector('%s')%s" % (selector,attrs)
    return self.execute(script)
   
  def css(self,selector,key_or_items ):
    '''
    @description : get or set element's style
    @param {str} selector : element's css selector
    @param {str|dict} key_or_items : 
      - str : getter , such as 'name'
      - dict : setter , such as {'data-a','1','data-b','2'}
    @returns {str|None} : return the css style's value in gtter
    '''
    if type(key_or_items) == str:
      script = "return $('%s').css('%s')" % (selector,key_or_items)
    else:
      styles=''
      for key,value in key_or_items.items():
        styles+=".css('%s','%s')" % (key,value)
      script = "$('%s')%s" % (selector,styles)
    return self.execute(script)

  def click(self,selector):
    script = "document.querySelector('%s').click()" % selector
    self.execute(script)

  def scroll_to_bottom(self,step=500,interval=1000):
    '''
    @description : scroll the page to the bottom, support the content was loaded lazy
    @param {int} step : the scroll height one time
    @param {int} interval : the wait time afater scroll
    '''
    js_script='''
    // 最后一个参数是python程序自动传入的回调
    var callback = arguments[arguments.length-1];
    (function(){
      var scrollHeight = document.body.scrollTop; // 当前滚动条位置
      var step = %s;
      var interval = %s;
      function scroll(){
        // 与最新内容高度比较
        if(scrollHeight<document.body.scrollHeight-window.innerHeight){
          scrollHeight += step;
          window.scroll(0,scrollHeight);
          document.title = scrollHeight;
          setTimeout(scroll,interval);
        }else{
          window.scroll(0,scrollHeight);
          document.title = scrollHeight;
          // 必须显式回调结束程序，否则程序会超时异常
          callback(scrollHeight);
        }
      }
      // 使用setTimeout程序是必须用异步函数，否则浏览器不会等待程序执行完毕就关闭
      setTimeout(scroll,interval);
    })();
    ''' % (step,interval)
    # 返回值是callback抛出值
    return self.execute_async_script(js_script)

  def scroll_top(self,top=0,scroll_selector='document'):
    self.__scroll(top,0,scroll_selector)
  
  def scroll_left(self,left=0,scroll_selector='document'):
    self.__scroll(0,left,scroll_selector)

  def __scroll(self,top=0,left=0,scroll_selector='document'):
    '''
    @description : scroll in y-axis
    @param {int} top : the offset to top
      0 - to top
      -1 - to bottom
    @param {str} scroll_selector : the scroll element
    '''

    # 滚动尺寸 (y,x) 水平方向-正数内容向左滚动，垂直方向-正数内容向上滚动
    offset = (left,top)
    outer_selector = self.__get_scroll_element(scroll_selector)
    if top == -1:
      # scroll to the bottom
      document_height = self.get_element_size('document')[1]
      offset = (left,document_height)
    if left == -1:
      # scroll to the bottom
      document_width = self.get_element_size('document')[0]
      offset = (document_width,top)
    
    script = "window.scrollTo(%s,%s);" % offset
    return self.execute(script)

  def scroll_element_to_window(self,content_selector,scroll_selector='document'):
    '''
    @description : scroll the content element into the window 
    @param {str} content_selector : the element will be shown in window
    @param {str} scroll_selector : the scroll element
    '''
    outer_selector = self.__get_scroll_element(scroll_selector)
    script = "$(%s).scrollTop($('%s').offset().top-100);" % (outer_selector,content_selector)
    self.execute(script)

  def get_element_size(self,selector='window'):

    if selector == 'window':
      width_script = "return window.innerWidth;"
      height_script = "return window.innerHeight;"
    elif selector == 'document':
      width_script = "return document.documentElement.offsetWidth;"
      height_script = "return document.documentElement.offsetHeight;"
    else:
      width_script = "return document.querySelector('%s').offsetWidth;" % selector
      height_script = "return document.querySelector('%s').offsetHeight;" % selector

    return (self.execute(width_script),self.execute(height_script))

  def __get_scroll_element(self,selector):
    return selector if selector == 'document' else "'%s'" % selector

  def remove(self,selector):
    '''
    @description 移除元素
    @param {str} selector css选择器
    '''
    script = """
      $('{}').remove()
    """.format(selector)
    return self.execute(script)

  def empty(self,selector):
    '''
    @description 清空元素内容
    @param {str} selector css选择器
    '''
    script = """
      $('{}').empty()
    """.format(selector)
    return self.execute(script)

  def load(self,url):
    '''
    @description : 导入线上/本地 js脚本
    @param {str} url : the scirpt file's path
    '''
    create_script = "var sele_script=document.createElement('script');sele_script.src='%s';" % url
    onload_script = "sele_script.onload=function(){console.log('%s loaded by the selenium!')};" % url
    append_script = "var head=document.getElementsByTagName('head')[0];head.appendChild(sele_script);"
    load_script = "%s %s %s" % (create_script,onload_script,append_script)
    # wait the script loaded, Determine whether it is complete according to the dynamic insertion mark 'selenium-dynamic-script'
    return self.execute(load_script)

  def is_var_exists(self,var):
    '''
    @description : determine weather global vars exists
    @param {str|list|tuple} var : consider some var has alias
    @returns {bool}
    '''
    vars = [var] if type(var)==str else var 
    condition = ''
    for key in vars:
      condition+='|| window["%s"]' % key
    condition = condition[2:]
    script = "var global_var = %s; return !!global_var;" % condition
    return self.execute(script)

  def open_tab(self,url,name='_blank'):
    '''
    @description : open a url in a new tab, and swith the driver to the new tab
    '''
    script = "window.open('%s','%s')" % (url,name)
    self.execute(script)

