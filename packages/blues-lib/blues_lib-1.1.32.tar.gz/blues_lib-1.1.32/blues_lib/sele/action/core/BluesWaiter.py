from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions 
from selenium.common.exceptions import NoSuchElementException 


# 使用expected_conditions内置函数，超时未满足条件会直接抛出异常
class BluesWaiter():

  def __init__(self,driver):
    self.driver = driver

  def alert_to_be_presence(self,timeout=10):
    '''
    @description : Determines whether the alert is presence
    @param {ini} timeout : Maximum waiting time
    @returns {Alert} : can't use alert.accept()
    '''
    wait_func = expected_conditions.alert_is_present()
    return self.__get_wait_value(wait_func,timeout)
  
  def to_be_stale(self,selector,timeout=10):
    '''
    @description : wait a dom element to be removed, the reference will lose efficacy
    @param {str} selector :  the element's css selector
    @param {ini} timeout : Maximum waiting time
    @returns {bool}
    '''
    element = self.to_be_presence(selector)
    wait_func = expected_conditions.staleness_of(element)
    return self.__get_wait_value(wait_func,timeout)

  def to_be_presence(self,selector,timeout=10):
    '''
    @description : get the first matched element
    @param {str} selector :  the element's css selector
    @param {ini} timeout : Maximum waiting time
    @returns {WebElement}
    '''
    locator = (By.CSS_SELECTOR,selector)
    wait_func = expected_conditions.presence_of_element_located(locator)
    return self.__get_wait_value(wait_func,timeout)

  def all_to_be_presence(self,selector,timeout=10):
    '''
    @description : get all elements matched
    @returns {Array<WebElement>}
    '''
    locator = (By.CSS_SELECTOR,selector)
    wait_func = expected_conditions.presence_of_all_elements_located(locator)
    elements = self.__get_wait_value(wait_func,timeout)
    return elements if elements else None

  def to_be_invisible(self,selector,timeout=10):
    '''
    @description : Determines whether a element exist and visible
    @param {str} selector :  the element's css selector
    @param {ini} timeout : Maximum waiting time
    @returns {WebElement}
    '''
    locator = (By.CSS_SELECTOR,selector)
    wait_func = expected_conditions.invisibility_of_element_located(locator)
    return self.__get_wait_value(wait_func,timeout)

  def to_be_selected(self,selector,timeout=10):
    '''
    @description : Determines whether a element exist and visible and selected
     - only can be used to radio and checkbox
    @param {str} selector :  the element's css selector
    @param {ini} timeout : Maximum waiting time
    @returns {WebElement}
    '''
    locator = (By.CSS_SELECTOR,selector)
    wait_func = expected_conditions.element_to_be_selected(locator)
    return self.__get_wait_value(wait_func,timeout)

  def to_be_clickable(self,selector,timeout=10):
    '''
    @description : Determines whether a element exist and visible and clickable
     - disabled button : return false
    @param {str} selector :  the element's css selector
    @param {ini} timeout : Maximum waiting time
    @returns {WebElement}
    '''
    locator = (By.CSS_SELECTOR,selector)
    wait_func = expected_conditions.element_to_be_clickable(locator)
    return self.__get_wait_value(wait_func,timeout)

  def to_be_visible(self,selector,timeout=10):
    '''
    @description : Determines whether a element exist and visible
    @param {str} selector :  the element's css selector
    @param {ini} timeout : Maximum waiting time
    @returns {WebElement}
    '''
    locator = (By.CSS_SELECTOR,selector)
    wait_func = expected_conditions.visibility_of_element_located(locator)
    return self.__get_wait_value(wait_func,timeout)

  def value_contains(self,selector,text,timeout=10):
    '''
    @description : Determines whether the value attribute of a element contains a string
    @param {str} selector :  the element's css selector
    @param {str} text : this search string
    @param {ini} timeout : Maximum waiting time
    @returns {WebElement}
    '''
    locator = (By.CSS_SELECTOR,selector)
    wait_func = expected_conditions.text_to_be_present_in_element_value(locator,text)
    return self.__get_wait_value(wait_func,timeout)

  def text_contains(self,selector,text,timeout=10):
    '''
    @description : Determines whether the text in an element tag contains a string
     - It can be inside a child of an element
    @param {str} selector :  the element's css selector
    @param {str} text : this search string
    @param {ini} timeout : Maximum waiting time
    @returns {WebElement}
    '''
    locator = (By.CSS_SELECTOR,selector)
    wait_func = expected_conditions.text_to_be_present_in_element(locator,text)
    return self.__get_wait_value(wait_func,timeout)

  def title_is(self,title,timeout=10):  
    '''
    @description : Determines whether the document title is equal to a string
    @param {str} title : the compare string
    @param {ini} timeout : Maximum waiting time
    @returns {bool}
    '''
    wait_func = expected_conditions.title_is(title)
    return self.__get_wait_value(wait_func,timeout)

  def title_contains(self,title,timeout=10):  
    '''
    @description : Determines whether the document title contains a string
    @param {str} title : the compare string
    @param {ini} timeout : Maximum waiting time
    @returns {bool}
    '''
    wait_func = expected_conditions.title_contains(title)
    return self.__get_wait_value(wait_func,timeout)

  def wait_for(self,wait_func=None,timeout=10):
    # this func has a para is the driver
    def dft_wait(driver):
      # this return value will be the parent func's return value
      return driver.current_url
    func = wait_func if wait_func else dft_wait
    poll_frequency=0.5
    ignored_exceptions = [NoSuchElementException]
    timeout_message = 'timeout of wait_for'
    # can return any type result
    return WebDriverWait(self.driver,timeout,poll_frequency,ignored_exceptions).until(func,timeout_message)

  def __get_wait_value(self,wait_func,timeout=10):
    try:
      return WebDriverWait(self.driver,timeout=timeout).until(wait_func)
    except Exception as e:
      return None