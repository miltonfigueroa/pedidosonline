from ._anvil_designer import RowTemplate6Template
from anvil import *
import anvil.server
from .. import Globals

class RowTemplate6(RowTemplate6Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties) 
    self.set_event_handler('x-sel_eliminado', self.sel_eliminado)


  def sel_eliminado(self,**event_args):

    if self.check_elimina.checked:
      self.item['eliminado']='SI'
      self.label_eliminado.text='si'
      Globals.borrados=Globals.borrados+' , '+ str(self.l_numreg.text)
      Globals.lista.append (self.l_numreg.text)
 
    else:
      self.item['eliminado']='NO'
      self.label_eliminado.text='no'


  def pasa(self, **event_args):
    print('pasa')