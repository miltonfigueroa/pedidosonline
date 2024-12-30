import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.pdf
import io


from datetime import datetime
from anvil import *
import anvil.users
from datetime import datetime
from datetime import date

@anvil.server.callable
def foo():
    return
  
@anvil.server.callable
def verifica_pedido(cve_doc):
  factura=anvil.server.call('get_factura', cve_doc)
  if factura is not None:
      resultado='1'
  else:
      resultado='0'
  return(resultado)
      
      
@anvil.server.callable
def inicia_usuarios(empresa):
    empresa = app_tables.empresas.get(Codigo=empresa)
    FechaVigencia=empresa['FechaVigencia']
    #inicia=empresa['Iniciar']
    #fechavalida = datetime.strptime(fecha_param, '%Y-%m-%d')   

    if  FechaVigencia>date.today():
        user_rows = app_tables.users.search()
        for row in user_rows:
            row["conectado"]= 0
      

@anvil.server.callable
def seguridad(usuario, tipo):
    
    if 'milton@sardegnasoft.com'== usuario:
        adminusr= 'T'
    else:
        adminusr= 'CERRAR SESION'
    user_rows = app_tables.users.search()
    conectado=0
    for row in user_rows:
            yaconectado=row["conectado"]
            if yaconectado is None:
               yaconectado=0
            conectado=conectado+yaconectado
    
    if tipo=='I':
        opera=1
    else:
        opera=-1

    conectado= conectado+opera
    if conectado > 999:
        autorizado = False
    else:
        autorizado = True
        user_row = app_tables.users.get(email=usuario)
        yaconectado=user_row["conectado"]
        if yaconectado is None:
          yaconectado=0
        user_row["conectado"]= yaconectado+opera
    
    return adminusr , autorizado

@anvil.server.callable
def get_users():
    users=app_tables.users.search()
    return users


@anvil.server.callable
def remove_partida(partidas,partida):
  
  fila=partidas
  for ix, item in enumerate(fila):
     
    if fila[ix]['num_par'] == partida:
      resta=fila[ix]['tot_partida']
      del fila[ix]    
  return(fila, resta) 
    
    
@anvil.server.callable
def refresca(self):
    res_suma=0
    self.repeating_panel_partidas.items, res_suma = anvil.server.call('get_partidas', self.clave_text_box.text)
    self.iarticulo.text = ""
    self.icantidad.text = 0
    self.importe.text = str(round(res_suma,2))
 
@anvil.server.callable
def formato(importe):
    importeformat="{0:,.2f}".format(importe)
    #print(importeformat)
    return importeformat


@anvil.server.callable
def create_pdf(cliente, fecha_recibo):
    pdf = anvil.pdf.render_form('Recibo', cliente, fecha_recibo)
    pdf_stream = io.BytesIO(pdf.get_bytes()).getvalue().decode('utf-8')
    
    print(pdf_stream)
    return pdf_stream
  

