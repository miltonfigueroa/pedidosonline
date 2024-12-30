from ._anvil_designer import subepdfTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import BlobMedia
import anvil.media


class subepdf(subepdfTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Ejemplo: Crear un BlobMedia desde un archivo PDF en memoria
    archivo_pdf=anvil.server.call('generar_pdf')
    anvil.media.download(archivo_pdf)

