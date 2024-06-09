from selenium import webdriver

class BluesFirefox():
  
  def __init__(self):
    profile = self.__get_default_preferences()
    self.driver = webdriver.Firefox(firefox_profile=profile)

  def __get_default_preferences(self):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList",2) 
    profile.set_preference("browser.download.manager.showWhenStarting",False) 
    profile.set_preference("browser.download.dir",'C:/sele/firfox') 
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk","application/octet-stream") 
    return profile