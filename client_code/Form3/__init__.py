from ._anvil_designer import Form3Template
from anvil import *
from .. import Globals
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import date

import anvil.users


class Form3(Form3Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    lista  = anvil.server.call('leeforma')
    self.lista_formas.items = [(x['descripcion'], x['numreg']) for x in lista]

      

  def muestra(self, **event_args): 
    if Globals.modo_regresa:
        Globals.modo_regresa=False
        self.clave_text_box.text=Globals.cve_doc_regresa
        self.usuario_conectado.text= Globals.usuario_conectado
        self.users.text=Globals.users
        if Globals.cve_doc_regresa !=None:
          self.despliega_factura()
    else:
        anvil.users.logout()
        anvil.users.login_with_form()
        self.num_par_g=1
        self.impformat.text='0.00'
        self.fecha_doc.date=date.today()
        self.importe.text=float(0)           
        self.usuario_conectado.text= Globals.usuario_conectado=anvil.users.get_user()['email']
        self.users.text, autoriza =anvil.server.call( 'seguridad', self.usuario_conectado.text, 'I')
        Globals.users=self.users.text
        if not autoriza:
            alert("Se ha exedido el numero de usuarios conectados")
            anvil.users.logout()
            open_form("Form3")
    
    try:
      anvil.server.call("foo")
    except anvil.server.SessionExpiredError:
      anvil.server.reset_session()

 
  def borra_partida(self, **event_args):
   
    borrado,resta=anvil.server.call( 'remove_partida', self.repeating_panel_partidas.items, event_args['num_par'])
    self.repeating_panel_partidas.items=borrado
    importe_num=float(self.importe.text)-resta
    self.importe.text=str(importe_num)
    self.impformat.text=anvil.server.call('formato',importe_num)
     

  def submit_button_click(self, **event_args):
    if len(self.clave_text_box.text) == 0 or self.clave_text_box.text ==  None :
      alert("No ha generado un numero de pedido")
    else:
      if self.repeating_panel_partidas.items is None:
        alert("No ha grabado ninguna partida en el pedido")
      else:
        self.graba_factura()
      
    
  def graba_factura(self):
    cve_doc = self.clave_text_box.text
    cve_clpv= self.lista_clientes.selected_value
    fecha_doc=self.fecha_doc.date
    importe=self.importe.text
    resultado=anvil.server.call('add_factura', cve_doc, cve_clpv,fecha_doc,importe , self.datos_entrega.text, self.contacto_entrega.text,anvil.users.get_user()['email'],self.exento.checked)
    anvil.server.call('add_partidas',self.repeating_panel_partidas.items,cve_doc,self.exento.checked)
    #self.clear_inputs()
    #self.clave_text_box.text = None
    if resultado=='C':
        alert("Pedido Grabado")
    else:
        alert("El pedido ya fue procesado, no se puede modificar")
    
  def clear_inputs(self):
    self.clave_text_box.text=None
    self.importe.text=float(0)
    self.iarticulo.selected_value=''
    self.lista_clientes.selected_value=''
    self.fecha_doc.date=date.today()
    self.impformat.text='0.00'
    self.repeating_panel_partidas.items=None
    self.datos_entrega.text=None
    self.contacto_entrega.text=None
    self.busca_prod.text=None
    self.iprecio.text=None
    self.iobs.text=None
    self.nit.text=''
    self.direccion.text=''
    self.nit_consulta.text=''
    self.num_par_g=1
    self.orden.source=None
    self.nombre_archivo.text=None
    return
    
        

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    self.image_1.source = file

  
  def clave_text_box_pressed_enter(self, **event_args):
    self.despliega_factura()
    
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    if self.icantidad.text is not None:
     if self.icantidad.text > 0:
      cant = round(float(self.icantidad.text),4)
      precio=round(float(self.iprecio.text),4)
      preciof=anvil.server.call('formato',precio)      
      tot_partida=round(cant*precio,2)
      importe_num=float(self.importe.text)+tot_partida
      self.importe.text=round(importe_num,2)
      self.impformat.text=anvil.server.call('formato',importe_num)
      num_par=self.num_par_g
      self.num_par_g=self.num_par_g+1
      uni_med=self.iarticulo.selected_value['uni_med']
      art=self.iarticulo.selected_value['cve_art']
      descri=anvil.server.call('get_desc_art', art)
      obspartida=self.iobs.text
      if num_par==1:
        self.repeating_panel_partidas.items= [{ 'descripcion': descri, 'cve_art': self.iarticulo.selected_value['cve_art'], 'precio': precio,  'cant' : cant, 'tot_partida' : tot_partida, 'num_par' : num_par , 'obspartida' : obspartida,  'uni_med' : uni_med  }]
      else:
        self.repeating_panel_partidas.items=self.repeating_panel_partidas.items+ [{ 'descripcion': descri, 'cve_art': self.iarticulo.selected_value['cve_art'], 'precio': precio,  'cant' : cant, 'tot_partida' : tot_partida,  'num_par' : num_par , 'obspartida' : obspartida ,  'uni_med' : uni_med }]
      
      #self.repeating_panel_partidas.items, res_suma = anvil.server.call('get_partidas', self.clave_text_box.text)
      self.iarticulo.text = ''
      self.iprecio.text=''
      self.icantidad.text = None
      self.busca_prod.text = None
      self.iobs.text= None
      self.busca_prod.focus()

     else:
       alert("La cantidad debe ser mayor que cero")
    else:
      alert("La cantidad debe ser mayor que cero")
      
  def lista_clientes_change(self, **event_args):
      if self.lista_clientes.selected_value != '00':
        cliente_selected=anvil.server.call('get_cliente', self.lista_clientes.selected_value, 'C')
        Globals.cliente=self.lista_clientes.selected_value
        Globals.nombre_cliente =cliente_selected['nombre']
        self.nit.text=cliente_selected['rfc']
        self.direccion.text=cliente_selected['calle']

  def lista_formas_change(self, **event_args):
      if self.lista_formas.selected_value != '00':
        forma_selected=anvil.server.call('get_forma', self.lista_formas.selected_value)
    
  
  def despliega_factura(self):
    factura=anvil.server.call('get_factura', self.clave_text_box.text)  
   
    if factura is not None:
      self.fecha_doc.date=factura['fecha_doc']
      self.lista_clientes.selected_value=factura['cve_clpv']
      self.importe.text=factura['importe']
      self.datos_entrega.text=factura['calle_entrega']   
      self.contacto_entrega.text=factura['contacto_entrega']
      importe_num=float(self.importe.text)
      self.impformat.text=anvil.server.call('formato',importe_num)
      clave=factura['cve_clpv'].strip()
      lista=anvil.server.call('leecliente',clave, 'C')
      self.lista_clientes.items = [(x['nombre'], x['clave']) for x in lista]
      cliente_selected=anvil.server.call('get_cliente',clave, 'C')
      self.nit.text=cliente_selected['rfc']
      self.direccion.text=cliente_selected['calle']
      self.repeating_panel_partidas.items, self.num_par_g = anvil.server.call('get_partidas', self.clave_text_box.text)
      orden_seleccionada=app_tables.ordenes.get(cve_doc=self.clave_text_box.text)
      if orden_seleccionada !=None:
         self.orden.source=orden_seleccionada['orden']
         self.nombre_archivo.text=orden_seleccionada['archivo']
      return
    
  def lista_pedidos_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("IngresoPagos")
  
  def busca_nit(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    lista  = anvil.server.call('leecliente', self.nit_consulta.text, 'N')
    self.lista_clientes.items = [(x['nombre'], x['clave']) for x in lista]
    #if self.lista_clientes.selected_value != '':
    self.lista_clientes_change()
    self.lista_clientes.focus()
    #self.busca_prod.focus()
  
    
  def nuevo_pedido_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.clear_inputs()
    self.clave_text_box.text=anvil.server.call('siguiente_pedido',anvil.users.get_user()['email'])
    self.fecha_doc.date=date.today()
    

  def busca_prod_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    mayu=self.busca_prod.text
    mayu=mayu.upper()
    lista = anvil.server.call('leeprod', mayu)
    self.iarticulo.items = [(r['desc'], r['selecciona'] ) for r in lista]
  
    if self.iarticulo.selected_value != '00':
      self.sel_art_change()
      self.iprecio.focus()
    

  def click_users(self, **event_args):
    """This method is called when the button is clicked"""
    if self.users.text == 'T':
        open_form("Form1")
    else:
        self.users.text, autoriza =anvil.server.call( 'seguridad', self.usuario_conectado.text, 'O')
        anvil.users.logout()
        open_form("Form3")
        
  def sel_art_change(self, **event_args):
    self.iprecio.text=self.iarticulo.selected_value["precio"]
    
  #  self.nombreart.text=self.iarticulo.selected_value["descr"]
    

         

  def imprimirya(self, **event_args):
    """This method is called when the button is clicked"""
    print(self.clave_text_box.text)
    open_form('Reporte',self.clave_text_box.text)

  def iprecio_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.icantidad.focus()

  def carga(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    self.orden.source=file   
    self.nombre_archivo.text=file.name
    orden_seleccionada=app_tables.ordenes.search(cve_doc=self.clave_text_box.text)
    encontro= 'n'
    for row in orden_seleccionada:
        encontro='s'
    if encontro=='n':
      app_tables.ordenes.add_row(archivo=file.name, orden=file, cve_doc=self.clave_text_box.text)
    else:
      orden_seleccionada = app_tables.ordenes.get(cve_doc=self.clave_text_box.text)
      orden_seleccionada.update(archivo=file.name, orden=file)
   
    
    

  def descarga(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.media.download(self.orden.source)
    
    

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.clear_inputs()

  def iobs_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def estado_click(self, **event_args):
    """This method is called when the button is clicked"""
    print(Globals.cliente,Globals.nombre_cliente)
    open_form("EstadoCuenta")
    pass

 

  


  



 










