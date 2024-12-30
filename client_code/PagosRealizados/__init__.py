from ._anvil_designer import PagosRealizadosTemplate
from anvil import *
import anvil.server
from .. import Globals

class PagosRealizados(PagosRealizadosTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.repeating_pagos.items = anvil.server.call('lee_pagos' , Globals.usuario,Globals.cuenta)
 
 

  def presiona_eliminar(self, **event_args):
    Globals.borrados=''
    Globals.lista=[]
    self.repeating_pagos.raise_event_on_children("x-sel_eliminado", **event_args)    
    result = alert(content="De Click en 'ELIMINAR' para confirmar",
              title="Confirme la eliminación de los registros "+Globals.borrados,
              style="info",
              #large=True,
              buttons=[
                ("Eliminar", "SI"),
                ("No", "NO")
              ])
    print(f"The user chose {result}") 
    if result=='SI':
      print(Globals.lista)
      anvil.server.call( 'borra_pagos', Globals.cuenta,  Globals.borrados)
      alert('Registros Eliminados')
      open_form('PagosRealizados')
      

  def click_regresar(self, **event_args):
    open_form("IngresoPagos")

    
  def llma_rutina(self, **event_args):
    """This method is called when the user presses Enter in this text box"""

    self.repeating_pagos.raise_event_on_children("x-sel_eliminado")
