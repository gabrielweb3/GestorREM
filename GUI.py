# -*- coding: utf-8 -*-
"""
FUNCIONES DE GUI

Created on Wed Jan 18 11:15:18 2023

@author: d935892
Gabriel Olivera
"""


######## cargar librerias #########
#librerias PI
import sys  
sys.path.append('C:\\Program Files (x86)\\PIPC\\AF\\PublicAssemblies\\4.0\\')  
import clr
from clr import AddReference
# clr.load("coreclr")
clr.AddReference('OSIsoft.AFSDK')  

# librerias del sistema operativo
import os
from os import scandir
from os import remove

from OSIsoft.AF import *  
from OSIsoft.AF.PI import * 
from OSIsoft.AF.Search import *   
from OSIsoft.AF.Asset import *  
from OSIsoft.AF.Data import *  
from OSIsoft.AF.Time import *  
from OSIsoft.AF.UnitsOfMeasure import *

#librerias tkinter para interfaz grafica
import tkinter
from tkinter import *
from tkinter import ttk

#otras librerias 
import time # medicion de tiempos de ejecucion

from datetime import datetime # manejo de series de tiempo en dataframes
import pandas as pd # analisis de datos
import numpy as np # analisis de datos

# libreria de exportacion de datos
from filtradoDatos import *
from filtradoDatos import AnalisisDatos


global var_lista_botones, elementos, lista_sensores, sensores_a_graficar, lista_errores  #, Bandera_Interfaz
lista_errores = []
# Bandera_Interfaz = False

class GUI():
    

    def connect_to_PISystem(serverName):  
        piSystems = PISystems()  
        global piSystem  
        piSystem = piSystems[serverName]  
        piSystem.Connect()
        
    def connect_to_Server(serverName):  
        piServers = PIServers()  
        global piServer  
        piServer = piServers[serverName]  
        # piServer.Connect(False)
        piSystem.Connect()
        
    def obtener_elementos(objeto):    
        if isinstance(objeto, PISystem):
             elementos_encontrados=objeto.Databases
        else:
             elementos_encontrados=objeto.Elements    
        return elementos_encontrados
    
    def transformar_coleccion_AF(coleccion):
        objetos_encontrados=[]    
        for elemento in coleccion:            
            objetos_encontrados.append(elemento) 
        return objetos_encontrados
        
    def seleccionar_base_REM():
        global elementos
        # conecto a servidor pi
        GUI.connect_to_PISystem('PIDataCollective')
        GUI.connect_to_Server('PIDataCollective')
        # conecto a base de datos pi
        elementos = GUI.transformar_coleccion_AF(GUI.obtener_elementos(piSystem))
        # elijo la base de datos de mi interes
        baseDatosSeleccionada = [elementos[-5].Name]
        # elijo los elementos de la base de datos
        elementosBaseREM = GUI.transformar_coleccion_AF(elementos[-5].Elements)
        return elementosBaseREM
    
    def cargar_lista_estaciones(base):
        # selecciono lista de elementos y las almaceno en vector
        listaEstaciones = []
        for i in range(len(base)): listaEstaciones.append(base[i].Name)
        return listaEstaciones
    
    def seleccionar_estacion(base,seleccionada):
        # elijo uno de los elementos de la lista
        estacionSeleccionada = base[seleccionada]
        return estacionSeleccionada
    
    def obtener_elementos_estacion(estacion,base):
        
        # vector para almacenar estacion seleccionada desde base pi
        estacionPI = []
        
        # comparo si la estacion seleccionada por el usuario se encuentra en la lista de estacionesPI
        for i in range(0,len(base)):
            # if str(estacion.get())==str(base[i].Name):
            if str(estacion)==str(base[i].Name):

                estacionPI.append(base[i])
                
        elementosEstacion = GUI.transformar_coleccion_AF(estacionPI[0].Elements)
        # print(elementosEstacion[0].Name)

        # alamaceno lista de elementos en vector
        listaSensores = []
        for i in range(len(elementosEstacion)): listaSensores.append(elementosEstacion[i].Name)

        return listaSensores, elementosEstacion
    
    # def obtener_fechas_inicio_fin():
        
    
    def desglozar_y_obtener_datos_sensor(lista, elementos):
        # global elementos
        # accedo a atributos de cada sensor
        propiedadesSensor = []
        for i in range(len(elementos)):
            propiedadesSensor.append(GUI.transformar_coleccion_AF(elementos[i].Attributes))
        # accedo a datos crudos de cada sensor
        crudosSensor = []
        for i in range(len(propiedadesSensor)):
            crudosSensor.append((propiedadesSensor[i][0]))
        # accedo a los datos de cada sensor para almacenarlos
        datosCrudosSensor = []
        for i in range(len(crudosSensor)):
            datosCrudosSensor.append(GUI.transformar_coleccion_AF(crudosSensor[i].Attributes))
        # almaceno los diferentes tipos de datos en vectores diferentes
        # avg
        promediosDatosCrudos = []
        for i in range(len(datosCrudosSensor)): promediosDatosCrudos.append(datosCrudosSensor[i][0])
        # min
        maximosDatosCrudos = []
        for i in range(len(datosCrudosSensor)): maximosDatosCrudos.append(datosCrudosSensor[i][1])
        # min
        desviacionDatosCrudos = []
        for i in range(len(datosCrudosSensor)): desviacionDatosCrudos.append(datosCrudosSensor[i][2])
        # std
        minimosDatosCrudos = []
        for i in range(len(datosCrudosSensor)): minimosDatosCrudos.append(datosCrudosSensor[i][3])
        # accedo a datos procesados de cada sensor
        procesadosSensor = []
        for i in range(len(propiedadesSensor)):
            procesadosSensor.append((propiedadesSensor[i][1]))
        # accedo a los datos de cada sensor para almacenarlos
        datosProcesadosSensor = []
        for i in range(len(procesadosSensor)):
            datosProcesadosSensor.append(GUI.transformar_coleccion_AF(procesadosSensor[i].Attributes))
        # almaceno los diferentes tipos de datos en vectores diferentes
        # avg
        promediosDatosProcesados = []
        for i in range(len(datosProcesadosSensor)): promediosDatosProcesados.append(datosProcesadosSensor[i][0])
        # min
        maximosDatosProcesados = []
        for i in range(len(datosProcesadosSensor)): maximosDatosProcesados.append(datosProcesadosSensor[i][1])
        # min
        desviacionDatosProcesados = []
        for i in range(len(datosProcesadosSensor)): desviacionDatosProcesados.append(datosProcesadosSensor[i][3])
        # std
        minimosDatosProcesados = []
        for i in range(len(datosProcesadosSensor)): minimosDatosProcesados.append(datosProcesadosSensor[i][2])

        piPoint_Estaciones = []

        for i in range(0,len(minimosDatosProcesados)):
            
            # piPoint_Estaciones.append(promediosDatosProcesados[i].get_PIPoint())
            # piPoint_Estaciones.append(desviacionDatosProcesados[i].get_PIPoint())
            # piPoint_Estaciones.append(maximosDatosProcesados[i].get_PIPoint())
            # piPoint_Estaciones.append(minimosDatosProcesados[i].get_PIPoint())
            
            piPoint_Estaciones.append(promediosDatosProcesados[i])
            piPoint_Estaciones.append(desviacionDatosProcesados[i])
            piPoint_Estaciones.append(maximosDatosProcesados[i])
            piPoint_Estaciones.append(minimosDatosProcesados[i])
    
        
        return piPoint_Estaciones
    
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
    # funcion para devolver nombres de columnas para que tengan mismo formato que visualSGM
    # def mapear_sensores(lista,elementos):
    def mapear_sensores(elementos):
        # global elementos
        #array para almacenar los nombres de tags y sus correspondientes nombre en el sistema
        tabla_de_relacion = []
        
        # GUI.obtener_fechas_inicio_fin(elementos)
        
        # creo vectores para almacenar informacion necesaria
        tiposVariables = ['_m','_ds','_min','_max']
        nombreSensor = []
        # rango de tiempo para consulta de los elementos necesarios
        timerange = AFTimeRange('01/01/1970 00:00','01/01/1970 00:10')
        
        # agrego valor del atributo nombre 4 veces para cada sensor
        for i in range(0,len(elementos)):
            nombreSensor.append(str((GUI.transformar_coleccion_AF(elementos[i].Attributes)[7]).GetValue(timerange)))
            nombreSensor.append(str((GUI.transformar_coleccion_AF(elementos[i].Attributes)[7]).GetValue(timerange)))
            nombreSensor.append(str((GUI.transformar_coleccion_AF(elementos[i].Attributes)[7]).GetValue(timerange)))
            nombreSensor.append(str((GUI.transformar_coleccion_AF(elementos[i].Attributes)[7]).GetValue(timerange)))
            
            tabla_de_relacion.append(str(elementos[i].Name)+'-'+str((GUI.transformar_coleccion_AF(elementos[i].Attributes)[7]).GetValue(timerange)))        
        # variable para contar el vector tiposVariable 
        j=0
        # inserto tiposVariable en el nombre de cada sensor
        for i in range(0,len(nombreSensor)):
            nombreSensor[i]=str(nombreSensor[i])+str(tiposVariables[j])
            
            j+=1
            # cuando la variable de conteo llegue a 4 reinicio la cuenta
            if j==4:
                j=0
        # agrego en la posicion cero del vector el nombre de la columna de timestamps        
        nombreSensor.insert(0,'Fecha_hora')
        
                
        # print(tabla_de_relacion)
        
        return nombreSensor, tabla_de_relacion
            
    def obtener_fechas_inicio_fin(elementos):
        
        import datetime
        
        # rango de tiempo para consulta de los elementos necesarios
        timerange = AFTimeRange('01/01/1970 00:00','01/01/1970 00:10')
        
        # fecha de inicio
        fecha_inicio_datos = str((GUI.transformar_coleccion_AF(elementos[0].Attributes)[2]).GetValue(timerange))
        
        # fecha de fin
        fecha_fin = datetime.datetime.now()
        fecha_fin_datos = str(fecha_fin.strftime('%d/%m/%Y')+' 00:00:00')
        
        return fecha_inicio_datos, fecha_fin_datos
        

    def mapear_como_PI(sensores):
        # creo vectores para almacenar informacion necesaria
        tiposVariables = [' m',' ds',' min',' max']
        # print(sensores)
        
        j = 0
        
        for i in range(0,len(sensores)):
            if sensores[i] == '_':
                sensores[i] = str(sensores[i][1:-1] + tiposVariables[j])
                
            else:
                sensores[i] = str(sensores[i] + tiposVariables[j])
            j+=1
            # cuando la variable de conteo llegue a 4 reinicio la cuenta
            if j==4:
                j=0
                
        # agrego en la posicion cero del vector el nombre de la columna de timestamps        
        sensores.insert(0,'Fecha_hora')
        
        return sensores

 
    # INFERFAZ GRAFICA #
    def interfazPrincipal(estaciones):
        
        global sensores_a_graficar, Bandera_Interfaz
        
        sensores_a_graficar = []
        
        # if len(sensores_a_graficar)==0:
        #     sensores_a_graficar=[]
        # ventana principal
        ventana = tkinter.Tk()
        ventana.title('Gestor de Datos REM')
        ventana.config(bg='#3E4140')
        # ventana.geometry("500x600")○
        
        s=ttk.Style()
        s.theme_names()
        s.theme_use()
        s.theme_use('clam')
        # s.theme_use('step')
        s.configure('Kim.TButton', foreground='maroon')
        s.theme_use()

        # pestañas
        pestana = ttk.Notebook(ventana)
        pestana.grid(row=0, column=0, padx=5, pady=5)
        
        # pestaña carga de datos
        consulta = tkinter.Frame(pestana,bg='#3E4140')
        
        # cuadros prinpales
        cuadro_principal = tkinter.LabelFrame(consulta,bg='#3E4140',fg='white')
        cuadro_principal.grid(row=1, column=0, pady=5, padx=5, sticky = W + E)
        
        # carga de datos
        cuadro_1 = tkinter.LabelFrame(cuadro_principal,text='Carga de datos',bg='#3E4140',fg='white')
        cuadro_1.grid(row=0, column=0, pady=5, padx=5,sticky=N + S + W + E)
        # filtro de datos
        cuadro_filtros = tkinter.LabelFrame(cuadro_principal,text='Analisis de datos',bg='#3E4140',fg='white')
        cuadro_filtros.grid(row=0, column=1, pady=5, padx=5, sticky = N + S + W + E)
        # información de estaciones
        cuadro_informacion = tkinter.LabelFrame(cuadro_principal,text='Historial de estación',bg='#3E4140',fg='white')
        cuadro_informacion.grid(row=0, column=2, pady=5, padx=5, sticky = N + S + W + E)
        
        
        ######## COLUMNA 1 carga de datos #########
        
        # cuadros de trabajo
        cuadro_2 = tkinter.LabelFrame(cuadro_1,text='Seleccion de estacion',bg='#3E4140',fg='white')
        cuadro_2.grid(row=1,column=0,padx=5,pady=5)
        cuadro_3 = tkinter.LabelFrame(cuadro_1,text='Base de datos',bg='#3E4140',fg='white')
        cuadro_3.grid(row=0,column=0,pady=5,padx=5,sticky=W + E)
        cuadro_4 = tkinter.LabelFrame(cuadro_1,text='Seleccion de periodo',bg='#3E4140',fg='white')
        cuadro_4.grid(row=2,column=0,pady=5,padx=5,sticky=W + E)        
        
        #base de datos
        # lista de base de datos
        baseSeleccionada = GUI.seleccionar_base_REM()
        lbl_base_datos = tkinter.Label(cuadro_3, text='Red de Estaciones de Medición', bg='#3E4140',fg='white')
        lbl_base_datos.grid(row=0,column=1,padx=5,pady=5)
        
        # seleccion estacion
        # variable para almacenar estacion seleccionada
        var_estacion_seleccionada = StringVar()        
        
        # lista de estaciones para visualizar
        listaEstaciones = GUI.cargar_lista_estaciones(baseSeleccionada)
        
        lbl_sele_estacion = tkinter.Label(cuadro_2, text='Estacion', bg='#3E4140',fg='white')
        lbl_sele_estacion.grid(row=2,column=0,padx=5,pady=5)
        lista_estaciones = ttk.Combobox(cuadro_2, width=30, values=estaciones,
                                        textvariable=var_estacion_seleccionada,
                                        state="readonly")
        lista_estaciones.grid(row=3, column=0, pady=5, padx=5)
    
        # variables para entrys de fechas de inicio y fin
        global var_fecha_ini, var_fecha_fin
        var_fecha_ini = StringVar()
        # var_fecha_ini.set('01/01/2022 00:00')
        var_fecha_ini.set('')

        var_fecha_fin = StringVar()
        # var_fecha_fin.set('01/01/2023 23:50')
        var_fecha_fin.set('')

        
        # seleccion de periodo
        lbl_fecha_ini = tkinter.Label(cuadro_4, text='Fecha Inicio',bg='#3E4140',fg='white')
        lbl_fecha_ini.grid(row=0,column=0,padx=5,pady=5)
        entry_fecha_ini = tkinter.Entry(cuadro_4,width=33,textvariable=var_fecha_ini).grid(row=1,column=0,padx=5,pady=5)
        lbl_fecha_fin = tkinter.Label(cuadro_4,text='Fecha Fin',bg='#3E4140',fg='white')
        lbl_fecha_fin.grid(row=2,column=0,padx=5,pady=5)
        entry_fecha_fin = tkinter.Entry(cuadro_4,width=33,textvariable=var_fecha_fin).grid(row=3,column=0,padx=5,pady=5)
        
        # # loading bar
        barra1 = ttk.Progressbar(ventana, orient=HORIZONTAL, length=460, mode='determinate')
        barra1.grid(row=10, column=0, pady=5, padx=5)
        
        # boton cargar datos
        btn_cargar_datos = tkinter.Button(cuadro_1,text='Cargar datos',
                                            command=lambda: GUI.cargar_datos(listaEstaciones,cuadro_5,
                                                                             var_estacion_seleccionada.get(),
                                                                             baseSeleccionada,
                                                                             barra1,
                                                                             ventana),
                                          bg='#3E4140',fg='white')
        btn_cargar_datos.grid(row=4,column=0,padx=5,pady=5,sticky=W + E + N + S)
        
        ######## COLUMNA 2 carga de datos #########
        # cuadros de trabajo
        cuadro_5 = tkinter.LabelFrame(cuadro_1,text='Seleccion de sensores',bg='#3E4140',fg='white')   
        cuadro_5.grid(row=0,column=1,padx=5,pady=5,rowspan=4,sticky=N + S)
        lbl_tipo_sensor = tkinter.Label(cuadro_5,text='Tipo',bg='#3E4140',fg='white')
        lbl_tipo_sensor.grid(row=1,column=0,padx=5,pady=5)
        lbl_alt_sensor = tkinter.Label(cuadro_5,text='Altura(m)',bg='#3E4140',fg='white')
        lbl_alt_sensor.grid(row=1,column=1,padx=5,pady=5)
        lbl_ori_sensor = tkinter.Label(cuadro_5,text='Orientacion(°)',bg='#3E4140',fg='white')
        lbl_ori_sensor.grid(row=1,column=2,padx=5,pady=5)        
        
        # cuadros para rangos de validez
        cuadro_limites_filtros = tkinter.LabelFrame(cuadro_filtros,text='Rangos de validez',bg='#3E4140',fg='white')
        cuadro_limites_filtros.grid(row=0,column=0,padx=5,pady=5,sticky=W + E + N + S)
        # etiquetas de limites para sensores
        etiqueta_limite_anemo = tkinter.Label(cuadro_limites_filtros,text='Anemómetros:',bg='#3E4140',fg='white')
        etiqueta_limite_vane = tkinter.Label(cuadro_limites_filtros,text='Veletas:',bg='#3E4140',fg='white')
        etiqueta_limite_term = tkinter.Label(cuadro_limites_filtros,text='Termómetros:',bg='#3E4140',fg='white')
        etiqueta_limite_higro = tkinter.Label(cuadro_limites_filtros,text='Higrómetro:',bg='#3E4140',fg='white')
        etiqueta_limite_baro = tkinter.Label(cuadro_limites_filtros,text='Barómetro:',bg='#3E4140',fg='white')
        etiqueta_limite_pira = tkinter.Label(cuadro_limites_filtros,text='Piranómetro:',bg='#3E4140',fg='white')
        etiqueta_limite_minimos = tkinter.Label(cuadro_limites_filtros,text='Minimos',bg='#3E4140',fg='white')
        etiqueta_limite_maximos = tkinter.Label(cuadro_limites_filtros,text='Máximos',bg='#3E4140',fg='white')
        
        # variables para minimos y maximos
        var_ane_lim_min = StringVar();  var_ane_lim_max = StringVar();
        var_ane_lim_min.set('3');var_ane_lim_max.set('25')

        var_vane_lim_min = StringVar(); var_vane_lim_max = StringVar()        
        var_vane_lim_min.set('0');var_vane_lim_max.set('359')
        
        var_ter_lim_min = StringVar();var_ter_lim_max = StringVar()
        var_ter_lim_min.set('-15');var_ter_lim_max.set('55')
        
        var_hig_lim_min = StringVar();var_hig_lim_max = StringVar()
        var_hig_lim_min.set('0');var_hig_lim_max.set('100')
        
        var_bar_lim_min = StringVar();var_bar_lim_max = StringVar()
        var_bar_lim_min.set('900');var_bar_lim_max.set('1200')
        
        var_pir_lim_min = StringVar();var_pir_lim_max = StringVar()
        var_pir_lim_min.set('0');var_pir_lim_max.set('1500')

        # entrys de límites
        entr_ane_lim_min = tkinter.Entry(cuadro_limites_filtros,width=5,textvariable=var_ane_lim_min)
        entr_ane_lim_max = tkinter.Entry(cuadro_limites_filtros,width=5,textvariable=var_ane_lim_max)
        entr_vane_lim_min = tkinter.Entry(cuadro_limites_filtros,width=5,textvariable=var_vane_lim_min)
        entr_vane_lim_max = tkinter.Entry(cuadro_limites_filtros,width=5,textvariable=var_vane_lim_max)
        entr_term_lim_min = tkinter.Entry(cuadro_limites_filtros,width=5,textvariable=var_ter_lim_min)
        entr_term_lim_max = tkinter.Entry(cuadro_limites_filtros,width=5,textvariable=var_ter_lim_max)
        entr_higr_lim_min = tkinter.Entry(cuadro_limites_filtros,width=5,textvariable=var_hig_lim_min)
        entr_higr_lim_max = tkinter.Entry(cuadro_limites_filtros,width=5,textvariable=var_hig_lim_max)
        entr_baro_lim_min = tkinter.Entry(cuadro_limites_filtros,width=5,textvariable=var_bar_lim_min)
        entr_baro_lim_max = tkinter.Entry(cuadro_limites_filtros,width=5,textvariable=var_bar_lim_max)
        entr_pira_lim_min = tkinter.Entry(cuadro_limites_filtros,width=5,textvariable=var_pir_lim_min)
        entr_pira_lim_max = tkinter.Entry(cuadro_limites_filtros,width=5,textvariable=var_pir_lim_max)
        

        etiqueta_limite_anemo.grid(row=1,column=0,padx=5,pady=5)
        etiqueta_limite_vane.grid(row=2,column=0,padx=5,pady=5)
        etiqueta_limite_term.grid(row=3,column=0,padx=5,pady=5)
        etiqueta_limite_higro.grid(row=4,column=0,padx=5,pady=5)
        etiqueta_limite_baro.grid(row=5,column=0,padx=5,pady=5)
        etiqueta_limite_pira.grid(row=6,column=0,padx=5,pady=5)
        etiqueta_limite_minimos.grid(row=0,column=1,padx=5,pady=5)
        etiqueta_limite_maximos.grid(row=0,column=2,padx=5,pady=5)

        entr_ane_lim_min.grid(row=1,column=1,padx=5,pady=5)
        entr_ane_lim_max.grid(row=1,column=2,padx=5,pady=5)
        entr_vane_lim_min.grid(row=2,column=1,padx=5,pady=5)
        entr_vane_lim_max.grid(row=2,column=2,padx=5,pady=5)
        entr_term_lim_min.grid(row=3,column=1,padx=5,pady=5)
        entr_term_lim_max.grid(row=3,column=2,padx=5,pady=5)
        entr_higr_lim_min.grid(row=4,column=1,padx=5,pady=5)
        entr_higr_lim_max.grid(row=4,column=2,padx=5,pady=5)
        entr_baro_lim_min.grid(row=5,column=1,padx=5,pady=5)
        entr_baro_lim_max.grid(row=5,column=2,padx=5,pady=5)
        entr_pira_lim_min.grid(row=6,column=1,padx=5,pady=5)
        entr_pira_lim_max.grid(row=6,column=2,padx=5,pady=5)
        
        # boton de aplicar rangos de validez
        btn_aplicar_rangos = tkinter.Button(cuadro_limites_filtros,text='Aplicar Rangos de Validez',bg='#3E4140',fg='white',
                                        command=lambda: AnalisisDatos.ValidacionDatos.rangos_de_validez(
                                            AnalisisDatos.levantar_datos('datosPI.txt' ),                                                                                  
                                            var_tipo_variable.get(),
                                            sensores_a_graficar,
                                            limites = {
                                                       'Ane':[int(var_ane_lim_min.get()),int(var_ane_lim_max.get())],
                                                       'Vel':[int(var_vane_lim_min.get()),int(var_vane_lim_max.get())],
                                                       'Ter':[int(var_ter_lim_min.get()),int(var_ter_lim_max.get())],
                                                       'Hig':[int(var_hig_lim_min.get()),int(var_hig_lim_max.get())],
                                                       'Bar':[int(var_bar_lim_min.get()),int(var_bar_lim_max.get())],
                                                       'Pir':[int(var_pir_lim_min.get()),int(var_pir_lim_max.get())]
                                                       }                                          
                                          ))
        btn_aplicar_rangos.grid(row=7,column=1,columnspan=2,padx=5,pady=5)        
        
        # cuadro de botones de análisis gráfico
        cuadro_7 = tkinter.LabelFrame(cuadro_filtros,text='Análisis Gráfico',bg='#3E4140',fg='white',)
        cuadro_7.grid(row=1,column=0,padx=5,pady=5,sticky=N + S + W + E)
                
        # variable de seleccion de variable correspondiente a la columna 3
        var_tipo_variable = StringVar()
        
        # boton de analizar datos
        btn_analizar_datos = tkinter.Button(cuadro_7, text='Histograma',
                                            command=lambda: AnalisisDatos.Analisis_Grafico.histograma(AnalisisDatos.levantar_datos('datosPI.txt' ),
                                                                                               sensores_a_graficar,
                                                                                              # elementos,
                                                                                              var_tipo_variable.get(),
                                                                                              var_estacion_seleccionada.get()),
                                            bg='#3E4140',fg='white')

        # boton de promedio de datos
        btn_evolucion_temporal = tkinter.Button(cuadro_7, text='Evolución Temporal',
                                            command=lambda: AnalisisDatos.Analisis_Grafico.evolucion_temporal(AnalisisDatos.levantar_datos('datosPI.txt'),
                                                                                               sensores_a_graficar,
                                                                                              # elementos,
                                                                                              var_tipo_variable.get(),
                                                                                              var_estacion_seleccionada.get()),
                                            bg='#3E4140',fg='white')
        
         # boton de promedio de datos
        btn_regresion_lineal = tkinter.Button(cuadro_7, text='Regresion Lineal',
                                            command=lambda: AnalisisDatos.Analisis_Grafico.regresion_lineal(AnalisisDatos.levantar_datos('datosPI.txt' ),
                                                                                               sensores_a_graficar,
                                                                                              # elementos,
                                                                                              var_tipo_variable.get(),
                                                                                              var_estacion_seleccionada.get()),
                                            bg='#3E4140',fg='white')
        
          # boton de promedio de datos
        btn_rosa_viento = tkinter.Button(cuadro_7, text='Rosa viento',
                                            command=lambda: AnalisisDatos.Analisis_Grafico.rosa_frecuencia(AnalisisDatos.levantar_datos('datosPI.txt' ),
                                                                                               sensores_a_graficar,
                                                                                              # elementos,
                                                                                              var_tipo_variable.get(),
                                                                                              var_estacion_seleccionada.get()),
                                            bg='#3E4140',fg='white')
        
          # boton de promedio de datos
        btn_promedios_mensuales = tkinter.Button(cuadro_7, text='Promedios mensuales',
                                            command=lambda: AnalisisDatos.Analisis_Grafico.promedios_mensuales(AnalisisDatos.levantar_datos('datosPI.txt' ),
                                                                                               sensores_a_graficar,
                                                                                              # elementos,
                                                                                              var_tipo_variable.get(),
                                                                                              var_estacion_seleccionada.get()),
                                            bg='#3E4140',fg='white')
        
          # boton de promedio de datos
        btn_diferencia_veletas = tkinter.Button(cuadro_7, text='Diferencia entre veletas',
                                            command=lambda: AnalisisDatos.Analisis_Grafico.diferencia_veletas(AnalisisDatos.levantar_datos('datosPI.txt' ),
                                                                                               sensores_a_graficar,
                                                                                              # elementos,
                                                                                              var_tipo_variable.get(),
                                                                                              var_estacion_seleccionada.get()),
                                            bg='#3E4140',fg='white')
        
        # boton diferencias anemometros
        btn_diferencia_anemometros = tkinter.Button(cuadro_7, text='Diferencia entre anemómetros',
                                            command=lambda: AnalisisDatos.Analisis_Grafico.diferencia_entre_anemometros(AnalisisDatos.levantar_datos('datosPI.txt' ),
                                                                                               sensores_a_graficar,
                                                                                              # elementos,
                                                                                              var_tipo_variable.get(),
                                                                                              var_estacion_seleccionada.get()),
                                            bg='#3E4140',fg='white')
        
        # boton diferencias anemometros
        btn_disponibilidad_datos = tkinter.Button(cuadro_7, text='Disponibilidad Datos',
                                            command=lambda: AnalisisDatos.Analisis_Grafico.disponibilidad_datos(AnalisisDatos.levantar_datos('datosPI.txt' ),
                                                                                               sensores_a_graficar,
                                                                                              # elementos,
                                                                                              var_tipo_variable.get(),
                                                                                              var_estacion_seleccionada.get(),
                                                                                              var_fecha_ini.get(),
                                                                                              var_fecha_fin.get(),
                                                                                              ),
                                            bg='#3E4140',fg='white')
        
        btn_evolucion_temporal.grid(row=1,column=1,padx=5,pady=5,sticky=W + E)
        btn_analizar_datos.grid(row=2,column=1,padx=5,pady=5,sticky=W + E)
        btn_regresion_lineal.grid(row=3,column=1,padx=5,pady=5,sticky=W + E)
        btn_rosa_viento.grid(row=1,column=2,padx=5,pady=5,sticky=W + E)
        btn_promedios_mensuales.grid(row=2,column=2,padx=5,pady=5,sticky=W + E)
        btn_diferencia_veletas.grid(row=4,columns=3,padx=5,pady=5,sticky=W + E)
        btn_diferencia_anemometros.grid(row=5,columns=3,padx=5,pady=5,sticky=W + E)
        btn_disponibilidad_datos.grid(row=3,column=2,padx=5,pady=5,sticky=W + E)
       
        ######### COLUMNA 3 carga de datos s###########
        
        # SELECCION TIPO DE VARIABLE
        # cuadro de trabajo
        cuadro_6 = tkinter.LabelFrame(cuadro_1,text='Seleccion de Variable',bg='#3E4140',fg='white')
        cuadro_6.grid(row=0,column=2,pady=5,padx=5,rowspan=4,sticky=N)
        lbl_tipo_variable = tkinter.Label(cuadro_6,text='Seleccionar tipo de variable',bg='#3E4140',fg='white')
        lbl_tipo_sensor.grid(row=0,column=0,padx=5,pady=5)
        
        
        
        ######## COLUMNA 3 información de estación #########
        # cuadro de seleccion de estacion
        cuando_seleccion_informacion = tkinter.LabelFrame(cuadro_informacion,text='Informacion de estación',bg='#3E4140',fg='white')
        cuando_seleccion_informacion.grid(row=0,column=0,pady=5,padx=5)
        # boton de información de estacion
        # boton de analizar datos
        btn_info_estacion = tkinter.Button(cuando_seleccion_informacion, text='Historial de instrumentos',bg='#3E4140',fg='white')
        btn_info_estacion.grid(row=0,column=0,pady=5,padx=5)
                            
        

        
        # botones de seleccion de variables
        radio_promedio = Radiobutton(cuadro_6, text="Promedios", variable=var_tipo_variable, value='m',bg='#3E4140',command=lambda: GUI.click_tipo_variable(var_tipo_variable.get()), fg='white')
        radio_desviacion = Radiobutton(cuadro_6, text="Desviación Estandar", variable=var_tipo_variable,command=lambda: GUI.click_tipo_variable(var_tipo_variable.get()), value='ds',bg='#3E4140',fg='white')
        radio_maximo = Radiobutton(cuadro_6, text="Máximos", variable=var_tipo_variable,command=lambda: GUI.click_tipo_variable(var_tipo_variable.get()), value='min',bg='#3E4140',fg='white')
        radio_minimo = Radiobutton(cuadro_6, text="Mínimos", variable=var_tipo_variable,command=lambda: GUI.click_tipo_variable(var_tipo_variable.get()), value='max',bg='#3E4140',fg='white')
        
        radio_promedio.grid(row=1,column=1,pady=5,padx=5,sticky=W)
        radio_desviacion.grid(row=2,column=1,pady=5,padx=5,sticky=W)
        radio_maximo.grid(row=3,column=1,pady=5,padx=5,sticky=W)
        radio_minimo.grid(row=4,column=1,pady=5,padx=5,sticky=W)
        
        radio_promedio.select()

        # agrego pestaña
        pestana.add(consulta,text = "Consulta de Datos") # linea 917
        ventana.mainloop()
        
    ################################################################################################################################################################################
    # FUNCION PAra map 
    def ts(value):
        try:
            ts=value.Timestamp.ToString("yyyy-MM-dd HH:mm:ss")
        except:
            ts=np.nan
        return ts
    ##################################################################################################################################################################
    # FUNCION PAra map 
    def nu(value):
        
        try:
            r=value.Value
        except:
            r=np.nan
            
        
        return  r
    #############################################################################################################################################################
    # FUNCION PAra map 
    def filtro(texto):
        try:
            cola=texto[15:]
        except:
            cola=np.nan
        return  cola
    ##################################################################################################################################################
    # FUNCION PARA map avvanzada
    def av(value):
        #return  value.Timestamp.LocalTime.Minute
        if (value.Timestamp.LocalTime.Minute%10==0)and(value.Timestamp.LocalTime.Second==0):
            union[nombre_atributo][ 1 ]=value.Value
        return  union

        
    def cargar_datos(lista,cuadro,estacion_seleccionada,base,barra,ventana):
        
        global lista_sensores, Bandera_Interfaz
            
        GUI.mostrar_lista_sensores(lista,cuadro,estacion_seleccionada,base)
        lista_sensores, elementos = GUI.obtener_elementos_estacion(estacion_seleccionada,base)

        # lista de señales a cargar
        senales = GUI.desglozar_y_obtener_datos_sensor(lista,elementos)
        
        # crear ficticios
        AnalisisDatos.ValidacionDatos.AnemometrosFicticios.crear_ficticios(lista_sensores)
        
        # mapear sensores para obtener nombres de las columnas en el mismo formato que visual
        # GUI.mapear_sensores(lista,elementos)
        GUI.mapear_sensores(elementos)
        
        # obtener fechas para 
        fecha_inicio, fecha_fin = GUI.obtener_fechas_inicio_fin(elementos)
    
        # extraigo fechas de inicio y fin de la interfaz
        var_fecha_ini.set(fecha_inicio)
        var_fecha_fin.set(fecha_fin)
        
        # fecha_inicio = var_fecha_ini.get()
        # fecha_fin = var_fecha_fin.get()
        
        #Se definen variables necesarias para la consulta
        #Variable del tipo AFtimeRange con los valores de inicio y fin del periodo
        timerange = AFTimeRange(fecha_inicio, fecha_fin)
        atributos_PI = []

        #Agrego los AFData correspondientes a los nombres de los Tags
        for senal in senales:    #☻☻☻☻☻☻☻☻
                    
            # atributos_PI.append(PIPoint.FindPIPoint(piServer, senal))

            atributos_PI.append(senal.PIPoint)     
            
        #Genero las fechas ordenadas
        fecha_inicio_time=datetime.strptime(fecha_inicio,'%d/%m/%Y %H:%M:%S')
        # fecha_inicio_num=date2num(fecha_inicio_time)
        fecha_fin_time=datetime.strptime(fecha_fin,'%d/%m/%Y %H:%M:%S')
        # fecha_fin_num=date2num(fecha_fin_time)
        
        rango_fechas=pd.date_range(start=fecha_inicio_time, end=fecha_fin_time, freq="10min")
        indice_fechas=range(0,len(rango_fechas))
        
        df=pd.DataFrame(rango_fechas)# creo la primer columna del dataframe recipiente para todos los datos 
        df=df.rename(columns={0:"Fecha_hora"})# renombro la columna 
    
        # bloque de consulta y acopio de datos en el recipiente 
        from tqdm import tqdm
        for consulta in tqdm(atributos_PI):# envuelvo en tqdm para que dibuje la barra de progreso

            try:
                nombre_atributo=consulta# registro el nombre de la variable
                # errores
                GUI.almacenar_errores(consulta.Name)
                resultado=consulta.RecordedValues(timerange, AFBoundaryType.Inside, "", False)# importo los datos en formato de PI
            
                ts_resultado=list(map(GUI.ts,resultado))# creo una lista con los timestamp de cada dato importado 
                resultado=list(map(GUI.nu,resultado))# creo una lista con los valores de cada dato importado
                f=list(map(GUI.filtro,ts_resultado))# creo una lista con la terminacion de cada timestamp importado
                df_auxi = pd.DataFrame(list(zip(ts_resultado, resultado,f)), columns =['Fecha_hora', nombre_atributo,'cola'])# creo una dataframe auxiliar con las 3 listas anteriores
        
                df_auxi.dropna(axis=0, how='any',  inplace=True)# elimino filas con valores nan
         
                df_auxi = df_auxi[   df_auxi["cola"]=="0:00"]# elimino filas con diezminutales inpuros 
        
                df_auxi.drop_duplicates(subset=['Fecha_hora'],keep='first',inplace=True,ignore_index=True)# elimino filas con fechas repetidas 
        
                df_auxi["Fecha_hora"]= pd.to_datetime(df_auxi['Fecha_hora'], format="%Y/%m/%d %H:%M:%S")# convierto la columna de fechas a datetime
                
                df_auxi.sort_values(by='Fecha_hora',inplace=True,ignore_index=True)# ordeno los datos por su fecha
                
                # ordeno los datos con referencia al timestamp completo del peridod de interes 
                df=df.join(df_auxi.set_index('Fecha_hora'), on='Fecha_hora') 
                df.drop(['cola'], axis=1, inplace=True)               
            
                
            except:                             
                pass
            
            #cargar y actualizar barra de carga
            barra['value']+=100/len(atributos_PI)
            ventana.update_idletasks()
            
        # df.to_csv(str('prueba.txt'),sep='\t',index=False)

        # mapear sensores para obtener nombres de las columnas en el mismo formato que visual
        # df.columns = GUI.mapear_sensores(lista,elementos)
            
            
        # registro columnas con nombre de pi   
        j = 0
        columnas_PI = []
        # columnas_PI.append('Fecha_hora')
        for i in range(1,len(df.columns)):    
            # print(df.columns[i].Name.split('_'))
            j += 1
            if j==4:
                if df.columns[i].Name[19] != '_':
                    columnas_PI.append(df.columns[i].Name[19:32])
                    columnas_PI.append(df.columns[i].Name[19:32])
                    columnas_PI.append(df.columns[i].Name[19:32])
                    columnas_PI.append(df.columns[i].Name[19:32])
                else:
                    columnas_PI.append(df.columns[i].Name[20:32])
                    columnas_PI.append(df.columns[i].Name[20:32])
                    columnas_PI.append(df.columns[i].Name[20:32])
                    columnas_PI.append(df.columns[i].Name[20:32])
                j = 0
            
            
        columnas_PI = GUI.mapear_como_PI(columnas_PI)
        # print(columnas_PI)
        
        # copio dataframe para tener una matriz con columnas de pi
        df_PI = df.copy()
            
        # renombro columnas pi
        df_PI.columns = columnas_PI
                
        # mapeo columnas para que se llamen igual que visual
        df.columns,variable_no_usada = GUI.mapear_sensores(elementos)
        # print(df.columns)
        # exporto a formato de visual
        df.to_csv(str(estacion_seleccionada+'.txt'),sep='\t',index=False)
        df_PI.to_csv('datosPI.txt',sep='\t',index=False)

        mapeo = GUI.mapear_sensores(elementos)
        # AnalisisDatos.promedios_mensuales(df,mapeo[1])
        
        # variable de interfaz
        # Bandera_Interfaz = True
        
        return df
    
        
    def mostrar_lista_sensores(lista,cuadro,estacion_seleccionada,base):
        # GUI.limpiar_lista_sensores(cuadro,estacion_seleccionada,base)
        
        global var_lista_botones, lista_sensores

         # botones de seleccion de sensor
        lista_sensores, elementos = GUI.obtener_elementos_estacion(estacion_seleccionada,base)


        # agrego anemometros ficticios a lista de sensores
        lista_Sensores = AnalisisDatos.ValidacionDatos.AnemometrosFicticios.crear_ficticios(lista_sensores)
        # lista_Sensores = sorted(lista_Sensores)
        lista_Sensores = AnalisisDatos.desglozar_sensores(lista_sensores)
        
        
        
        check_lista_botones = list(range(0,len(lista_sensores)))
        lbl_lista_alturas = list(range(0,len(lista_sensores)))
        lbl_lista_orientacion = list(range(0,len(lista_sensores)))
        var_lista_botones = list(range(0,len(lista_sensores)))
        

        
        if len(lista_Sensores)!=0:
        
            for i in range(0,len(lista_sensores)):
                var_lista_botones[i] = tkinter.BooleanVar()
                check_lista_botones[i] = ttk.Checkbutton(cuadro,
                                                         text=lista_Sensores['Tipo'][i],
                                                         variable=var_lista_botones[i],
                                                         command=lambda: GUI.button_clicked(lista_sensores)
                                                         )
                                                         # style='TButton',)
                                                         # bg='#3E4140',fg='white',)
                lbl_lista_alturas = tkinter.Label(cuadro,
                                                  text=lista_Sensores['Altura'][i],
                                                  bg='#3E4140',fg='white',)
                lbl_lista_orientacion = tkinter.Label(cuadro,
                                                  text=lista_Sensores['Orientacion'][i],
                                                  bg='#3E4140',fg='white',)
                
                y = i+2
                check_lista_botones[i].grid(row=y,column=0,padx=5,pady=5,sticky=W)
                lbl_lista_alturas.grid(row=y,column=1,padx=5,pady=5,sticky=E)
                lbl_lista_orientacion.grid(row=y,column=2,padx=5,pady=5,sticky=E)
                

        return estacion_seleccionada
    
    # listar qué sensores se cliquearon
    def button_clicked(lista):
        global var_lista_botones, elementos, sensores_a_graficar
        
        # print(len(lista))
        
        sensores_a_graficar = []
        
        for i in range(0,len(lista)):
            if lista[i] not in sensores_a_graficar and var_lista_botones[i].get():
                sensores_a_graficar.append(lista[i])
                        
        # GUI.retener_lista_sensores(sensores_a_graficar)
        return sensores_a_graficar

        
    def click_tipo_variable(tipo):  
        
        print(tipo)
        return tipo
        
    # def retener_lista_sensores(lista_sensores):
    #     return lista_sensores
        
    def limpiar_lista_sensores(base):
        
        # selecciono base
        # base = GUI.seleccionar_base_REM()

        # limpiar lista actual
        GUI.interfazPrincipal(GUI.cargar_lista_estaciones(base))


    def almacenar_errores(iteracion):
        global lista_errores
        # almacenar iteraciones
        lista_errores.append(iteracion)
        
        return (lista_errores)
        
        
        
        