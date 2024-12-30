from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)


    # Any code you write here will run when the form opens.

  def link_1_show(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    #self.nombreart.text=anvil.server.call('get_desc_art', self.item['cve_art'])
    impdec=float(self.item['tot_partida'])
    self.d_importe.text=anvil.server.call('formato',impdec)

 

  def delete_click(self, **event_args):
    """This method is called when the button is clicked"""
    #anvil.server.call('remove_partida', self.repeating_panel_partidas.items, 2)
    self.parent.raise_event('x-borra-partida', num_par=self.item['num_par'])
   

  def d_importe_change(self, **event_args):
    """This method is called when the text in this text area is edited"""
    pass



  





 

