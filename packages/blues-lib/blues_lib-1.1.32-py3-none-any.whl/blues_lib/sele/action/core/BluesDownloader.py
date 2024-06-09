import sys,os,re,urllib
from urllib.parse import urlparse
from .BluesElement import BluesElement 

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from config.BluesConfig import BluesConfig  
from util.BluesURL import BluesURL   

class BluesDownloader():

  def __init__(self,driver):
    self.driver = driver
    self.element_action = BluesElement(driver)

  def download_img(self,img_selector,file_name='',file_dir=''):
    '''
    @description : download image from a img element
    '''
    url = self.element_action.get_attr(img_selector,'src')
    if url:
      return self.download(url,file_name,file_dir)
    else:
      return None

  def download(self,url,file_name='',file_dir=''):
    '''
    @description : a common method to downlad a file by it's url
    '''
    if not url:
      return

    if not file_name:
      dl_name = BluesURL.get_filename(url)   

    dl_path = self.__get_file_path(dl_name,file_dir)
    try:
      # the return value's first element is the dl path
      return urllib.request.urlretrieve(url,dl_path)[0]
    except Exception as e:
      return None

  def __get_file_path(self,file_name,file_dir=''):
    if file_dir:
      dl_dir = file_dir
    else:
      dl_dir = BluesConfig.get_download_dir('file')

    return '%s%s' % (dl_dir,file_name)