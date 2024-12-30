from ._anvil_designer import ReciboTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Recibo(ReciboTemplate):
  def __init__(self, clientep, fechap,  **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.cliente.text=clientep
    self.fecha_recibo.text=fechap

    # Any code you write here will run before the form opens.
