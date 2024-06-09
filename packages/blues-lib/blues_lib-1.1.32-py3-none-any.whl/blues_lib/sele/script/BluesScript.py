from .BluesJavaScript import BluesJavaScript             
from .BluesJQuery import BluesJQuery              

class BluesScript():

  def __init__(self,driver):
    self.javascript= BluesJavaScript(driver)
    self.jquery= BluesJQuery(driver)
 