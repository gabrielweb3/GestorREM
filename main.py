# -*- coding: utf-8 -*-
"""
SCRIPT PRINCIPAL DE GREM-LINK

Created on Mon Dec 26 14:59:17 2022

@author: d935892
Gabriel Olivera
"""

# import IPython
# app = IPython.Application.instance()
# app.kernel.do_shutdown(True) 

# Funciones de interaccion con GUI 
from GUI import GUI

# selecciono base
base = GUI.seleccionar_base_REM()

# llamo a GUI
GUI.interfazPrincipal(GUI.cargar_lista_estaciones(base))


# elementos: 0 - Crudos
# elementos: 1 - Procesados
# elementos: 2 - Fecha instalación
# elementos: 3 - Fecha desinstalación
# elementos: 4 - Mapeo
# elementos: 5 - Modelo
# elementos: 6 - Marca
# elementos: 7 - Nombre
# elementos: 8 - Comentarios
# elementos: 9 - Scale
# elementos: 10 - Offset
# elementos: 11 - Canal
# https://docs.osisoft.com/bundle/af-sdk/page/html/Overload_OSIsoft_AF_Asset_AFAttribute_GetValue.htm
# nombreSensor.append(str((GUI.transformar_coleccion_AF(elementos[i].Attributes)[7]).GetValue(timerange)))
# timerange = AFTimeRange('01/01/1970 00:00','01/01/1970 00:10')

# [branch "develop"]
# 	remote = origin
# 	merge = refs/heads/develop
