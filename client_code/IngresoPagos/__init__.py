from ._anvil_designer import IngresoPagosTemplate
from anvil import *
import anvil.server
import anvil.users
#import anvil.tables as tables
#import anvil.tables.query as q
from anvil.tables import app_tables

from datetime import date
from .. import Globals

class IngresoPagos(IngresoPagosTemplate):
  def limpia_forma(self, **event_args):
     self.no_recibo.text= ''
     self.no_referencia.text= ''
     self.nit_consulta.text= ''
     self.total_pagar.text= ''
     self.lista_clientes.selected_value= ''  
     Globals.cliente = ''
     self.total_pagar_pressed_enter()
     self.referencia2.text= ''
     Globals.g_pagototal=0
     return
   
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    lista  = anvil.server.call('leeforma')
    self.lista_formas.items = [(x['descripcion'], x['numreg']) for x in lista] 
    lista  = anvil.server.call('leecuenta')
    self.cuentas_bancarias.items = [(x['descripcion'], x['numreg']) for x in lista] 
    lista  = anvil.server.call('leeconcepto')
    self.drop_tipo.items = [(x['concepto'], x['clave']) for x in lista] 
    Globals.cuenta='01'
    Globals.concepto='CLICOB'
    self.fecha_tran.date=date.today()
    anvil.users.login_with_form()
    
    self.usuario_conectado.text= anvil.users.get_user()['email']
    Globals.usuario=anvil.users.get_user()['iniciales']
    return
    
  def llama_grabar_pago(self, **event_args):
    #  fechatran, monto, cliente, ncliente, nit, fpago
 
    if Globals.g_pagototal > 0:  # and self.drop_tipo.selected_value=='Cuotas':
      alert('Pago pendiente de distribuir '+ str(Globals.g_pagototal)+', revise')
    else:
      fpago=self.lista_formas.selected_value
      npago=int(fpago)-1
      #print(self.lista_formas.items[npago][0])
      ncuenta=Globals.cuenta
      self.repeating_detalle_pagos.raise_event_on_children("x-regresa_pago")
      detalle=anvil.server.call('grabar_pago',self.fecha_tran.date, self.total_pagar.text, Globals.cliente, Globals.nombre_cliente ,Globals.nit, fpago, self.repeating_detalle_pagos.items,ncuenta,self.lista_formas.items[npago][0],Globals.usuario,self.drop_tipo.selected_value,self.no_referencia.text,self.no_recibo.text,Globals.dir_cliente,Globals.lote,Globals.oc,self.referencia2.text,Globals.concepto)
      self.emite_recibo_click(detalle)
      alert("Pedido Grabado")
      self.limpia_forma()
    return
  
  
  def busca_nit(self, **event_args):
    lista  = anvil.server.call('leecliente', self.nit_consulta.text)
    self.lista_clientes.items = [(x['nombre'], x['clave']) for x in lista]
    self.lista_clientes_change()
    return

  def lista_clientes_change(self, **event_args):
    if self.lista_clientes.selected_value != '00':
        cliente_selected=anvil.server.call('get_cliente', self.lista_clientes.selected_value,'C')
        Globals.cliente=self.lista_clientes.selected_value
        Globals.nombre_cliente =cliente_selected['nombre']
        Globals.nit=cliente_selected['rfc']
        Globals.dir_cliente=cliente_selected['direccion']
        Globals.oc=cliente_selected['oc']
        Globals.lote=cliente_selected['lote']
        if Globals.nit is None:
          Globals.nit = ''
    return


  def total_pagar_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
 
    Globals.g_pagototal=self.total_pagar.text
    self.repeating_detalle_pagos.items = anvil.server.call('get_cuenta_cobrar' , Globals.cliente)
    self.repeating_detalle_pagos.raise_event_on_children("x-sel-pago")
    return

  def pagos_realizados_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('PagosRealizados')
    pass

  def concepto_change(self, **event_args):
    Globals.concepto=self.drop_tipo.selected_value
    return
  
  def cuenta_change(self, **event_args):
    cuentaint=self.cuentas_bancarias.selected_value
    if cuentaint > 9:
      Globals.cuenta=str(cuentaint)
    else:
      Globals.cuenta='0'+str(cuentaint)
    return

  def emite_recibo_click(self, detalle):
    """This method is called when the button is clicked"""
    cliente = Globals.nombre_cliente
    archivo_pdf=anvil.server.call('generar_pdf',cliente, self.fecha_tran.date,detalle)
    anvil.media.download(archivo_pdf)

  def salida_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()
    open_form("IngresoPagos")

  def referencia2_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if len(self.referencia2.text) > 19:
      alert('La longitud supera 20 caracteres')

  def no_referencia_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if len(self.no_referencia.text) > 19:
      alert('La longitud supera 20 caracteres')



