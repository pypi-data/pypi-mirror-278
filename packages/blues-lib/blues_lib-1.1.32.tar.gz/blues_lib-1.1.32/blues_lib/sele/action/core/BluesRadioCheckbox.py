from .BluesElement import BluesElement

class BluesRadioCheckbox():
  
  def __init__(self,driver):
    self.driver = driver
    self.element_action = BluesElement(driver)

  def select(self,selector):
    '''
    @description : select all matched elements
      if you want operator multi elements, the css selector should contains multi options
      such as: 'input[value=car],input[value=boat]'
    '''
    web_elements = self.element_action.wait_all(selector)
    if not web_elements:
      return

    for web_element in web_elements:
      if not web_element.is_selected():
        web_element.click()

  def deselect(self,selector):
    '''
    @description : deselect all matched elements
    '''
    web_elements = self.element_action.wait_all(selector)
    if not web_elements:
      return

    for web_element in web_elements:
      if web_element.is_selected():
        web_element.click()

  def is_selected(self,selector):
    web_element = self.element_action.wait(selector)
    return web_element.is_selected() if web_element else False