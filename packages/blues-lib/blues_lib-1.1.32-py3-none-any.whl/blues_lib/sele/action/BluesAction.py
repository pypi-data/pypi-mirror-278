from .core.BluesElement import BluesElement
from .core.BluesForm import BluesForm  
from .core.BluesWindow import BluesWindow   
from .core.BluesTab import BluesTab    
from .core.BluesDocument import BluesDocument    
from .core.BluesCookie import BluesCookie     
from .core.BluesEvent import BluesEvent      
from .core.BluesMover import BluesMover       
from .core.BluesFrame import BluesFrame        
from .core.BluesSelecter import BluesSelecter          
from .core.BluesAlert import BluesAlert           
from .core.BluesWaiter import BluesWaiter            
from .core.BluesDownloader import BluesDownloader             
from .core.BluesRadioCheckbox import BluesRadioCheckbox              
from .core.BluesShortcut import BluesShortcut               


class BluesAction():

  def __init__(self,driver):
    self.element = BluesElement(driver)
    self.form = BluesForm(driver)
    self.window = BluesWindow(driver)
    self.tab = BluesTab(driver)
    self.document = BluesDocument(driver)
    self.cookie = BluesCookie(driver)
    self.event = BluesEvent(driver)
    self.mover = BluesMover(driver)
    self.frame = BluesFrame(driver)
    self.selecter = BluesSelecter(driver)
    self.alert = BluesAlert(driver)
    self.waiter = BluesWaiter(driver)            
    self.downloader = BluesDownloader(driver)            
    self.radio_checkbox = BluesRadioCheckbox(driver)            
    self.shortcut = BluesShortcut(driver)            
              