from ._anvil_designer import RowTemplate5Template
from anvil import *
import anvil.server
from .. import Globals


class RowTemplate5(RowTemplate5Template):

  def __init__(self, **properties):
    self.set_event_handler('x-sel-pago', self.sel_pago)
    self.set_event_handler('x-regresa_pago', self.regresa_pago)
    # Set Form properties and Data Bindings.
    self.init_components(**properties)    
    return

  def sel_pago(self, **event_args):

    if self.label_1.text is None or self.label_1.text == '0.00'  or self.item['monto']=='Total General'  or self.item['monto']=='Documento' or self.item['monto']=='Financiamiento':
      self.pagar.visible = False
    # Any code you write here will run before the form opens.

  def pago_selected(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
  
    if self.pagar.checked:
      #saldo=self.item['saldonum'] replace('-','')
      saldo=float(self.item['saldo'].replace(',',''))

      if Globals.g_pagototal > saldo:
          self.pago.text = self.item['saldo']
          Globals.g_pagototal= Globals.g_pagototal- saldo
          
      else:
          self.pago.text= "{0:,.2f}".format(Globals.g_pagototal)
          Globals.g_pagototal=0
    else:
      saldo=float(self.pago.text.replace(',',''))
      Globals.g_pagototal= Globals.g_pagototal+saldo

      self.pago.text = ''
    return
    
  def regresa_pago(self, **event_args):
    if self.pago.text is not None:
      if self.pago.text > '':
        self.pago.text=self.pago.text.replace(',','')
        self.item['pago']=float(self.pago.text)
      else:
        self.item['pago']=0
      