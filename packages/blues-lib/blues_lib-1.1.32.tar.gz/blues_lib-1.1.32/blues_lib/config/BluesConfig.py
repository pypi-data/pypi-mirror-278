import sys,os,re,time

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesURL import BluesURL   
from util.BluesFiler import BluesFiler    

class BluesConfig():

  DOWNLOAD_ROOT = 'c:/blues_lib/download/'  
  DOWNLOAD_MODULES = {
    'http':'http',
    'report':'report',
    'image':'image',
  }

  @classmethod
  def get_download_dir(cls,module=''):
    if not module:
      dl_dir= cls.DOWNLOAD_ROOT
    else:
      module_dir = cls.DOWNLOAD_MODULES.get(module,module) 
      dl_dir = '%s%s/' % (cls.DOWNLOAD_ROOT,module_dir)

    # create dir
    BluesFiler.makedirs(dl_dir)
    return dl_dir 

  @classmethod
  def get_download_file(cls,module,filename):
    return '%s%s' % (cls.get_download_dir(module),filename)

  @classmethod
  def get_download_http_file(cls,filename):
    return cls.get_download_file('http',filename)
  
  @classmethod
  def get_download_http_domain_file(cls,url,extension='txt'):
    domain = BluesURL.get_main_domain(url)
    filename = '%s.%s' % (domain,extension)
    return cls.get_download_http_file(filename)

  @classmethod
  def get_filename(cls,extension=''):
    return '%s.%s' % (int(time.time()*1000),extension)