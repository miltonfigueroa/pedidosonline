from ._anvil_designer import Form4Template
from anvil import *
import Globals
import anvil.users
import anvil.server
#import anvil.tables as tables
#import anvil.tables.query as q
#from anvil.tables import app_tables
from datetime import date, datetime, timedelta


class Form4(Form4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.fecha_inicio.date=date.today()
    self.fecha_final.date=date.today()
    
    self.aplicafiltro()
    self.repeating_pedidos.set_event_handler('x-sel-pedido', self.sel_pedido)

  def regresa_click(self, **event_args):
    """This method is called when the button is clicked"""
    Globals.modo_regresa=True
    open_form("Form3")
    
  def sel_pedido(self, **event_args):
    Globals.modo_regresa=True
    
    Globals.cve_doc_regresa = event_args['cve_doc']
    open_form("Form3")

  def aplicafiltro(self, **event_args):
    """This method is called when the button is clicked"""
    #print(self.fecha_inicio.date)
    self.repeating_pedidos.items = anvil.server.call('get_pedidosp' ,anvil.users.get_user()['email'],self.fecha_inicio.date,self.fecha_final.date,self.Pendientes.text)
    
    self.repeating_pedidos.set_event_handler('x-sel-pedido', self.sel_pedido)

   

  def Pendiente_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
  
    if self.Pendiente.checked:
      self.Pendientes.text='S'
    else:
      self.Pendientes.text='N'
    self.aplicafiltro()
     

  def fecha_inicial_show(self, **event_args):
    """This method is called when the DatePicker is shown on the screen"""
    self.fecha_inicio.date=datetime.now()-timedelta(days=30)
    self.aplicafiltro()





 


