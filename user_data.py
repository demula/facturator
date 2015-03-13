#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from modelos import extraer_codigo_desde_codigo_factura, extraer_tipo_desde_codigo_factura, Factura

QUERY_SELECT_FACTURA = 'SELECT CEMFAC, CNOFAC, TOTFAC, FECFAC, CLIFAC, EMAFAC FROM F_FAC WHERE TIPFAC = ? AND CODFAC = ?'
QUERY_MARCAR_ENVIADA = 'UPDATE F_FAC SET EMAFAC = ? WHERE TIPFAC = ? AND CODFAC = ?'

FACTURA_ENVIADA = 1


def extraer_datos_factura_desde_access_db(cursor, numero_factura, ruta_archivo_pdf):
    tipo = extraer_tipo_desde_codigo_factura(numero_factura)
    codigo = extraer_codigo_desde_codigo_factura(numero_factura)

    facturas = []
    for (email, nombre_fiscal, total, fecha, numero_cliente, enviada) in cursor.execute(QUERY_SELECT_FACTURA, tipo,
                                                                                        codigo):  # cursors are iterable
        facturas.append(Factura(email, tipo, codigo, nombre_fiscal, total, fecha, numero_cliente, enviada, ruta_archivo_pdf))
    if facturas.__len__() == 1:
        return facturas[0]


def marcar_factura_enviada_access_db(conexion, cursor, factura):
    updated = cursor.execute(QUERY_MARCAR_ENVIADA, FACTURA_ENVIADA, factura.tipo, factura.codigo)
    conexion.commit()
