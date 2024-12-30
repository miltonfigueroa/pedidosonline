from ._anvil_designer import ReporteTemplate
from anvil import *
from .. import Globals
from datetime import datetime
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Reporte(ReporteTemplate):
  def __init__(self,cve_doc, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    factura=anvil.server.call('get_factura', cve_doc)
    self.fecha.text=factura['fecha_doc']
   
    self.cve_doc.text=factura['cve_doc']
    self.importe.text=anvil.server.call('formato',factura['importe'])
    self.dir_entrega.text=factura['calle_entrega']
    self.contacto.text=factura['contacto_entrega']
    cliente=anvil.server.call('leecliente', factura['cve_clpv'], 'C')
    clienteactual=cliente[0]
   
    self.nombre_cliente.text=clienteactual['nombre']
    self.direccion.text=clienteactual['direccion']
    self.repeating_panel_part_rep.items, partidas = anvil.server.call('get_partidas', cve_doc)
 
  def regresa_click(self, **event_args):
    """This method is called when the button is clicked"""
    Globals.modo_regresa=True
    open_form("Form3")
    pass

