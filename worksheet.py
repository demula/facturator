from modelos import extraer_tipo_desde_codigo_factura, extraer_codigo_desde_codigo_factura
from user_data import extraer_datos_factura_desde_access_db, marcar_factura_enviada_access_db
from os import listdir
from os.path import isfile, join, abspath
import pyodbc


DBfile = 'resources/factusol_database.mdb'
conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + DBfile)
cursor = conn.cursor()

archivos_factturas = [(f.split(".")[0], abspath(f)) for f in listdir("facturas") if isfile(join("facturas", f))]

for (numero, ruta_pdf) in archivos_factturas:
    print numero
    tipo = extraer_tipo_desde_codigo_factura(numero)
    codigo = extraer_codigo_desde_codigo_factura(numero)

    factura = extraer_datos_factura_desde_access_db(cursor, numero, ruta_pdf)
    print factura

    marcar_factura_enviada_access_db(conn, cursor, factura)

    factura = extraer_datos_factura_desde_access_db(cursor, numero, ruta_pdf)
    print factura

cursor.close()
conn.close()