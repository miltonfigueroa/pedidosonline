from ._anvil_designer import RowTemplate3Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate3(RowTemplate3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.descr.text=anvil.server.call('get_desc_art', self.item['cve_art'])+ ' '+self.item['obspartida']
    self.f_precio.text=anvil.server.call('formato',self.item['precio'])
    self.f_total_partida.text=anvil.server.call('formato',self.item['tot_partida'])
    # Any code you write here will run when the form opens.