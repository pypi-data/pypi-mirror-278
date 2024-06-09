import re,os
from urllib.parse import urlparse
from tld import get_fld

class BluesURL():

  @classmethod
  def get_domain(self,url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

  @classmethod
  def get_main_domain(self,url):
    return get_fld(url)
  
  @classmethod
  def get_filename(self,url):
    parsed_url = urlparse(url)
    return os.path.basename(parsed_url.path)