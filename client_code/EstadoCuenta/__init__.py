from ._anvil_designer import EstadoCuentaTemplate
from anvil import *
import anvil.server
#import anvil.users
from .. import Globals

class EstadoCuenta(EstadoCuentaTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.nombre_cliente.text=Globals.nombre_cliente
    self.repeating_estado_cuenta.items = anvil.server.call('get_estado_cuenta' , Globals.cliente)
    # Any code you write here will run before the form opens.

  def regresa_click(self, **event_args):
    """This method is called when the button is clicked"""
    Globals.modo_regresa=True
    Globals.cve_doc_regresa=None
    open_form("Form3")
