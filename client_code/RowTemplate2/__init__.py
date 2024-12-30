from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate2(RowTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def selecciona_pedido_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.raise_event('x-sel-pedido', cve_doc=self.item['cve_doc'])

  def modifica_fecha(self, **event_args):
    """This method is called when the selected date changes"""
    anvil.server.call('update_factura', self.item['cve_doc'],self.item['entrega'])


