# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 09:21:56 2023

@author: d935892


script para pruebas con dataframe principal
"""

from filtradoDatos import *

# definicion estacion y carga datos
Estacion = 'Valentines 100 Ammonit.txt'
EstacionPI = 'datosPI.txt' 
# Estacion = 'Piedra Sola Ammonit.txt'
datos = AnalisisDatos.levantar_datos(Estacion)
datosPI = AnalisisDatos.levantar_datos(EstacionPI)

# datos.index = AnalisisDatos.transformar_indice_fechas(datos)
datos.index = pd.DatetimeIndex(datos['Fecha_hora'],dayfirst=True)

limites = {'Ane':[3,25],
            'Vel':[0,360],
            'Ter':[-15,55],
            'Hig':[0,100],
            'Bar':[900,1200],
            'Pir':[0,1500]
            }

stirng = ['_Ane_160_123','_Ane_98_30']

# fechas
# inicio = datos.index[0]
# fin = datos.index[-1]

inicio = '22/11/2022 03:00:00'
fin = '02/08/2023 00:00:00'

# cantidad total de datos
# str(inicio.strftime('%d/%m/%Y')+' 00:00:00')
# str(fin.strftime('%d/%m/%Y')+' 00:00:00')

rango = pd.date_range(str(inicio.strftime('%d/%m/%Y')+' 00:00:00'),str(fin.strftime('%d/%m/%Y')+' 00:00:00'),freq='10Min')
TOTAL_DATOS = len(rango)

# cantidad de datos no validos 
no_validos = []

# nuevo df
df = datos.copy()

for columna in datos.columns:
    df[columna] = pd.to_numeric(df[columna],errors='coerce')
    no_validos.append(df[columna].count())
    
# disponibilidad por variable
disponibilidad_por_variable = []

for var in no_validos:
    disponibilidad_por_variable.append(round(var/TOTAL_DATOS,2)*100)
    print(var/TOTAL_DATOS)
    
# agrego disponibilidad
df.iloc[0] = disponibilidad_por_variable

# creo tag de varaible con su tipo designado
# lista = AnalisisDatos.transformar_sensores_para_analisis(datos.columns,'_m')
    
# lista = ['Ane_42_111 m','Ane_42_351 m', 'Bar_91.7_0 m', 'Ter_3.1_0 m', 'Vel_39.9_351 m']
# # sensores = ['Ane_42_111 m', 'Ter_3.1_0 m',] 
# ficticios=['Anemómetro Ficticio 1_42_', 'Anemómetro Ficticio 2_74.9_', 'Anemómetro Ficticio 3_91.7_']

# # anemometros = AnalisisDatos.desglozar_sensores(ficticios)

# # tipos = list(limites.keys())
# # alturas = []
# # AnalisisDatos.ValidacionDatos.AnemometrosFicticios.crear_ficticios(lista)
# alturas = AnalisisDatos.ValidacionDatos.AnemometrosFicticios.crear_ficticios(lista)
# print(type(AnalisisDatos.ValidacionDatos.AnemometrosFicticios.crear_ficticios(lista)))
# ficticios = list(AnalisisDatos.ValidacionDatos.AnemometrosFicticios.crear_ficticios(lista))
# for i in range(0,len(anemometros['Tipo'])):
#     if 'Anemómetro' in anemometros['Tipo'][i]:
#         # almaceno altura
#         alturas.append(anemometros['Altura'][i])
# def promedio_alturas(alturas):
#     promedios = []
#     n = len(alturas)
    
#     for i in range(n):
#         suma = 0
#         count = 0
        
#         for j in range(n):
#             if abs(alturas[i] - alturas[j]) < 2.5:
#                 suma += alturas[j]
#                 count += 1
        
#         if count > 0:
#             promedio = suma / count
#             promedios.append(promedio)
    
#     print (pd.Series(promedios).unique())


# promedio_alturas([75,76,45,44,31,30])
# print('alturas: ',alturas)    
# dup = [x for i, x in enumerate(alturas) if x in alturas[:i]]
# print(dup)  # [1, 5, 1]         
# # datos.columns = AnalisisDatos.transformar_sensores_para_analisis(datos.columns,'m')
# mylist = None

# if alturas is not None:
#     for x in alturas:
#         print(x)
# print(len(datos[sensores[0]]))

# for tipo in tipos:

#     for sensor in sensores:
#         if tipo in sensor:
            
#             cond1 = datos[sensor]>limites[tipo][0]
#             cond2 = datos[sensor]<limites[tipo][1]

#             datos = datos[cond1 | cond2]
#             # datos = datos[datos[sensor] > limites[tipo][0] | datos[sensor] < limites[tipo][1]]
           
            
# print(len(datos[sensores[0]]))

# for i in 

# for i in datos.columns:
    
# paso=0
# for i in range(0,12):
#     tajada = round(len(datos['Fecha_hora'])/12)
#     paso = paso + tajada
#     print('tamaño paso:',str(paso))
#     division=datos['Fecha_hora'][:paso][0]
#     print((division))
    
    
    # datos['Fecha_hora'][i] = datos.index[i].value
# copia
# auxiliar = datos.copy()

# filtro repetidos
# sin_repetidos
# for i in range(1,len(datos.columns),4):
    
#     auxiliar[datos.columns[i]] = AnalisisDatos.ValidacionDatos.filtrar_repetidos(datos,datos.columns[i],3)
#     auxiliar[datos.columns[i]] = AnalisisDatos.ValidacionDatos.filtrar_pendientes_consecutivas(datos,datos.columns[i],3)

# auxiliar = AnalisisDatos.ValidacionDatos.filtrado_simple(datos,3)
# pendientes consecutivas 
    
# diferencia entre anemómetros

# lista sensores 
# ['Ane_42_111', 'Ane_42_351', 'Ane_74.9_107', 'Ane_74.9_348', 'Ane_91.7_106', 'Ane_91.7_346', 'Bar_91.7_0', 'Ter_3.1_0', 'Ter_91.6_0', 'Vel_39.9_351', 'Vel_89.7_346']


