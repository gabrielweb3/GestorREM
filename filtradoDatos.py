# -*- coding: utf-8 -*-
"""

FUNCIONES DE FILTRADO DE DATOS

Created on Mon Jan 23 14:41:57 2023

@author: d935892
Gabriel Olivera
"""


# importacion de librerias
import pandas as pd # analisis de datos
import numpy as np # analisis de datos
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from plotly.offline import plot
import plotly.figure_factory as ff


# from GUIfunctions import GUI

global datos
global filtrado 

class AnalisisDatos():
    
    global datos
    filtrado = {
            'Rangos Validez':False,
                }
    
    def variables_a_graficar(variables):
        print('Se graficara:'+variables)
    
    def levantar_datos(estacion):
        datos = pd.read_csv(estacion,sep='\t')
        
        return datos        
        
    def transformar_indice_fechas(datos):
        datos[datos.columns[0]] = pd.to_datetime(datos[datos.columns[0]], errors='coerce')
        
        return datos
    
    def transformar_a_valores_numericos(datos):
        for column in range(1,len(datos.columns)):
            datos[datos.columns[column]] = pd.to_numeric(datos[datos.columns[column]],errors='coerce')
        return datos
    
    
    def transformar_sensores_para_analisis(lista,tipo_variable):
        
        AnalisisDatos.sin_datos_seleccionados(lista)
       
        # creo tag de varaible con su tipo designado
        for i in range(0,len(lista)):
           
            if lista[i][-1] == 'm' or lista[i][-1] == 'ds' or lista[i][-1] == 'min' or lista[i][-1] == 'max':
                pass
            else:     
                lista[i] = str(lista[i]) + ' ' + str(tipo_variable) 
            
        return lista
    
    def sin_datos_seleccionados(lista):
        # import tkinter
        # print(len(lista))

        if len(lista)==0:
            # print(len(lista))
            AnalisisDatos.warnings(0)
            # return tkinter.messagebox.showerror(title='Error en función', message='Seleccione algún sensor para realizar cálculo deseado')
        else:
            # print('no pasa nada')
            pass
        
    def warnings(codigo):
        import tkinter
        # sin datos seleccionados
        if codigo==0:
            return tkinter.messagebox.showerror(title='Error en función', message='Seleccione algún sensor para realizar cálculo deseado')
        
        # seleccionar dos veletas para calculo diferencia 
        elif codigo==1:
            tkinter.messagebox.showerror(title='Falla en cálculo', message='Seleccione por lo menos dos veletas para realizar cálculo')
            
        # seleccionar dos anemometros para calculo de diferencia
        elif codigo==2:
            tkinter.messagebox.showerror(title='Falla en cálculo', message='Seleccione dos anemómetros y una veleta para realizar cálculo')
 

        
    def limpiar_NAN(datos):
        datos = datos.dropna()
        
        return datos
    
    def mapear_meses(fila):
        
        if fila==1:
            fila='Enero'
        elif fila==2:
            fila='Febrero'
        elif fila==3:
            fila='Marzo'
        elif fila==4:
            fila='Abril'
        elif fila==5:
            fila='Mayo'
        elif fila==6:
            fila='Junio'
        elif fila==7:
            fila='Julio'
        elif fila==8:
            fila='Agosto'
        elif fila==9:
            fila='Septiembre'
        elif fila==10:
            fila='Octubre'
        elif fila==11:
            fila='Noviembre'
        elif fila==12:
            fila='Diciembre'
                        
        return fila
    
    def desglozar_sensores(sensores):        
        informacion_instrumento = []
        informacion_sensores = {'Tipo':[],
                                'Altura':[],
                                'Orientacion':[]}
        # print(sensores)
        
        # divido string en informacion util
        for i in range(0,len(sensores)):
            informacion_instrumento.append(sensores[i].split('_'))            
        # reemplazo las siglas por el nombre del sensor
            if 'Ane' in sensores[i] and not 'Fict' in sensores[i]:
                informacion_instrumento[i][0] = 'Anemómetro'
            elif 'Vel' in sensores[i]:
                informacion_instrumento[i][0] = 'Veleta'
            elif 'Pir' in sensores[i]:
                informacion_instrumento[i][0] = 'Piranómetro'
            elif 'Ter' in sensores[i]:
                informacion_instrumento[i][0] = 'Termómetro'
            elif 'Bar' in sensores[i]:
                informacion_instrumento[i][0] = 'Barómetro'
            elif 'Hig' in sensores[i]:
                informacion_instrumento[i][0] = 'Higrómetro'
            elif 'Pre' in sensores[i]:
                informacion_instrumento[i][0] = 'Pluviómetro'
            elif 'AneFict' in sensores[i]:
                informacion_instrumento[i][0] = 'Anemómetro Ficticio'
                
            informacion_sensores['Tipo'].append(informacion_instrumento[i][0])
            informacion_sensores['Altura'].append(informacion_instrumento[i][1])
            informacion_sensores['Orientacion'].append(informacion_instrumento[i][2])
                   
        return informacion_sensores
        
    # crea una altura de dos alturas a menos de 2.5m de diferencia, funcion para ficticios
    def ascociar_alturas_cercanas(alturas):
        promedios = []
        n = len(alturas)
        
        for i in range(n):
            suma = 0
            count = 0            
            for j in range(n):
                if abs(alturas[i] - alturas[j]) < 2.5:
                    suma += alturas[j]
                    count += 1
            if count > 0:
                promedio = round(suma / count,1)
                promedios.append(str(promedio))
        
        return pd.Series(promedios).unique()
            
    
################################################################################
######################## ANALISIS GRAFICO DE DATOS ############################# 
################################################################################
    
    class Analisis_Grafico():

        def evolucion_temporal(datos,lista,tipo_variable,estacion):
            
            # creo tag de varaible con su tipo designado
            lista = AnalisisDatos.transformar_sensores_para_analisis(lista,tipo_variable)

            # filtro repetidos
            # for i in range(1,len(datos.columns[0]),4):
            #     datos[datos.columns[i]] = AnalisisDatos.ValidacionDatos.filtrar_repetidos(datos,datos.columns[i],3)
            
               
            # creacion de graficos de evolucion temporal
            fig = make_subplots(rows=int(len(lista)),cols=1)
            fig = make_subplots(rows=1,cols=1)
            for i in range(0,len(lista)):
                fig.append_trace(go.Scatter(x=datos['Fecha_hora'],
                                            y=datos[lista[i]],
                                            name=str(lista[i])),
                                  row=1,col=1)           
            fig.update_layout(title_text=str(estacion)+" Evolucion Temporal")
            plot(fig,filename=str(estacion)+' Evolucion Temporal')     
    
 
        def histograma(datos,lista,tipo_variable,estacion):
            
            lista = AnalisisDatos.transformar_sensores_para_analisis(lista,tipo_variable)
            # filtro repetidos
            # for i in range(1,len(datos.columns[0]),4):
            #     datos[datos.columns[i]] = AnalisisDatos.ValidacionDatos.filtrar_repetidos(datos,datos.columns[i],3)
                   
            # creacion de graficos de evolucion temporal
            fig = make_subplots(rows=int(len(lista)),cols=1)
            fig = make_subplots(rows=1,cols=1)
            for i in range(0,len(lista)):
                fig.append_trace(go.Histogram(x=datos[lista[i]],
                                            name=str(lista[i]), nbinsx=40,
                                            histnorm='probability density',
                                            opacity=0.6,),
                                  row=1,col=1)           
            fig.update_layout(title_text=str(estacion)+" Histograma",
                              barmode='overlay')
            plot(fig,filename=str(estacion)+' Histograma')     
           
           # https://plotly.com/python/plotly-express/ 
            
        def regresion_lineal(datos,lista,tipo_variable,estacion):
            
             # creo tag de varaible con su tipo designado
            lista = AnalisisDatos.transformar_sensores_para_analisis(lista,tipo_variable)

            # creacion de graficos de regresion lineal
            fig = px.scatter(
                    datos,
                    x = datos[lista[-1]],
                    y = datos[lista[0]],
                    opacity=0.65,
                    trendline='ols',                    
                    trendline_color_override='darkblue',
                    # text=datos.columns[-1],
                    labels={'Anemometro'}
                )            
           
            fig.update_layout(title_text=str(estacion)+" Regresion lineal")
            plot(fig,filename=str(estacion)+' Regresion lineal')     
            
            
        def rosa_frecuencia(datos,lista,tipo_variable,estacion):
                
                 # creo tag de varaible con su tipo designado
                lista = AnalisisDatos.transformar_sensores_para_analisis(lista,tipo_variable)

                # creacion de graficos de rosa de velocidad
                fig = px.scatter_polar(
                        datos,
                        r = datos[lista[0]],
                        theta = datos[lista[-1]],
                        color_discrete_sequence=px.colors.sequential.Plasma_r,
                        template="plotly_dark",
                    ) 
                
                fig = go.Figure(go.Barpolar(
                        r = datos[lista[0]],
                        theta = datos[lista[-1]],
                        # color_discrete_sequence=px.colors.sequential.Plasma_r,
                        # template="plotly_dark",
                        opacity=0.8

                    ) )
                
                fig.update_layout(title_text=str(estacion)+" Rosa de velocidad",
                                  polar = dict(
                                    radialaxis = dict(range=[0, 5], showticklabels=False, ticks=''),
                                    angularaxis = dict(showticklabels=False, ticks='')
                                ))
                plot(fig,filename=str(estacion)+' Rosa de velocidad')    
        
        
        def promedios_mensuales(datos,lista,tipo_variable,estacion):
                
            # mapeo DATOS con mismo formato que LISTA
            lista = AnalisisDatos.transformar_sensores_para_analisis(lista,tipo_variable)

            # transformacion a valores numericos e index a fecha
            datos = AnalisisDatos.transformar_a_valores_numericos(datos)
            datos.index = pd.DatetimeIndex(datos['Fecha_hora'],dayfirst=True)

            # calculo promedios mensuales por año para DATOS
            promedios_mensuales = datos.groupby(by=[datos.index.year,datos.index.month]).mean()
            
            promedios_mensuales.insert(0,'Fecha','Fecha')
            
            for i in range(0,len(promedios_mensuales.index)):#promedios_mensuales.index[i][0])
                promedios_mensuales['Fecha'][i] = (list(promedios_mensuales.index[i]))
                promedios_mensuales['Fecha'][i][1]=AnalisisDatos.mapear_meses(promedios_mensuales['Fecha'][i][1])
                
            
            promedios_mensuales['Fecha']=promedios_mensuales['Fecha'][:].apply(str) 
            print(promedios_mensuales['Fecha'][2])
            
            # creacion de graficos de promedios mensuales
            fig = make_subplots(rows=int(len(lista)),cols=1)
            fig = make_subplots(rows=1,cols=1)        
            for y in range(0,len(lista)):
                fig.append_trace(go.Scatter(x=promedios_mensuales['Fecha'],
                                            y=promedios_mensuales[lista[y]],
                                            name=str(lista[y])),
                                  row=1,col=1)    
       
            fig.update_layout(title_text=str(estacion)+" Promedios Mensuales")
            plot(fig,filename=str(estacion)+' Promedios Mensuales')     

            
        def diferencia_veletas(datos,lista,tipo_variable,estacion):
            
            # creo tag de varaible con su tipo designado
            lista = AnalisisDatos.transformar_sensores_para_analisis(lista,tipo_variable)
            
            # checkear si son veletas 
            contador_de_veletas = 0
            nombre_veletas = []
            while contador_de_veletas<2:
                
                for instrumento in lista:
                    if 'Vel' in instrumento:
                        contador_de_veletas+=1         
                        nombre_veletas.append(instrumento)
                
                if not contador_de_veletas>=2:
                    AnalisisDatos.warnings(1)
                    # tkinter.messagebox.showerror(title='Falla en cálculo', message='Seleccione por lo menos dos veletas para realizar cálculo')
                elif contador_de_veletas==2:
                    break
                
            # calculo de diferencia de veletas para cada caso
            datos['Diferencia Veletas'] = datos[nombre_veletas[0]] - datos[nombre_veletas[1]] 
            # contemplar diferencias positivas, negativas y con error de zona norte
            for i in range(0,len(datos['Diferencia Veletas'])):    
                if abs(datos[nombre_veletas[0]][i] - datos[nombre_veletas[1]][i]) > 180:
                    datos['Diferencia Veletas'][i] = 360 - abs(datos[nombre_veletas[0]][i] - datos[nombre_veletas[1]][i])
                    if abs(datos[nombre_veletas[0]][i] - datos[nombre_veletas[1]][i]) > 0:
                        datos['Diferencia Veletas'][i] = datos['Diferencia Veletas'][i]*-1
                else:
                    datos['Diferencia Veletas'][i] = datos[nombre_veletas[0]][i] - datos[nombre_veletas[1]][i]
                    
                
            # calculo el promedio de los datos para agregar una linea horizontal
            promedio_diferencia_veletas = round(datos['Diferencia Veletas'].mean(),2)
            
            # scatter 
            fig = px.scatter(datos,x='Fecha_hora',y='Diferencia Veletas',
                             opacity=0.75)
            fig.add_hline(y=promedio_diferencia_veletas,
                          annotation_text='Dif: '+str(promedio_diferencia_veletas)+'°',
                          annotation_position="bottom left",
                          annotation=dict(font_size=20, font_family="Arial"))
            fig.update_layout(title_text=str(estacion)+" Diferencia de Veletas en el tiempo")
            plot(fig,filename=str(estacion)+' Diferencia Veletas')  
            
            
        
        def diferencia_entre_anemometros(datos,lista,tipo_variable,estacion):
              # creo tag de varaible con su tipo designado
            lista = AnalisisDatos.transformar_sensores_para_analisis(lista,tipo_variable)
            
            # contadores de sensores
            anemometros_para_calculo = []
            veletas_para_calculo = []
            
            for sensor in lista:
                if 'Ane' in sensor:
                    anemometros_para_calculo.append(sensor)
                
                elif 'Vel' in sensor:
                    veletas_para_calculo.append(sensor)
                    
            if len(anemometros_para_calculo)==2 and len(veletas_para_calculo)==1:
                # #calcular diferencia anemometros
                datos['diferencia anemometros'] = datos[anemometros_para_calculo[0]] - datos[anemometros_para_calculo[1]]
                # datos['valor numerico fecha'] = datos.index
                datos.index = pd.DatetimeIndex(datos['Fecha_hora'],dayfirst=True)
                for i in range(0,len(datos.index)):
                    datos['Fecha_hora'][i] = datos.index[i].value
                # calculo el promedio de los datos para agregar una linea horizontal
                # promedio_diferencia_anemometros = round(datos['diferencia anemometros'].mean(),4)
          
                
            # Create figure
            fig = go.Figure()
                
            paso = 0
            
            for step in range(0,20):

                # configuracion slider de fecha
                tajada = round(len(datos['Fecha_hora'])/20)
                paso = paso + tajada
                
                # diferencias promedios por periodo
                promedio_diferencia_anemometros = round(datos['diferencia anemometros'][:paso].mean(),4)
                
                inicio_periodo = str(datos['diferencia anemometros'][:paso][0])
                final_periodo = str(datos['diferencia anemometros'][:paso][-1])

               
                fig.add_trace(
                    go.Scatter(
                        visible=False,
                        x=datos[veletas_para_calculo[0]][:paso],
                        y=datos['diferencia anemometros'][:paso],
                        mode='markers',
                        marker=dict(size=3,
                                    colorscale='plotly3',), # one of plotly colorscales
                        marker_color=datos['Fecha_hora'][:paso],
                        name=inicio_periodo + '-' + final_periodo))

                # fig.add_annotation(
                #     text=inicio_periodo + '-' + final_periodo,)


            fig.data[19].visible = True

            steps=[]
            for i in range(len(fig.data)):
                periodo = dict(
                    method="update",
                    args=[{"visible": [False] * len(fig.data)},
                          {"title": str(estacion)+" Diferencia entre anemómetros en función de la dirección"}],  # layout attribute
                )
                periodo["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
                steps.append(periodo)
            
            sliders = [dict(
                active=19,
                currentvalue={"prefix": "Fechas "},
                pad={"t": 50},
                steps=steps
                )]
            
            fig.add_hline(y=0,
                   # annotation_text='Dif: '+str(promedio_diferencia_anemometros)+'m/s',
                  annotation_text=' ',
                  annotation_position="bottom left",
                  annotation=dict(font_size=20, font_family="Arial"))
            fig.update_layout(title_text=str(estacion)+" Diferencia entre anemómetros en función de la dirección",
                              sliders=sliders)
            plot(fig,filename=str(estacion)+' Diferencia Anemómetros')  
            
            
        def disponibilidad_datos(datos,lista,tipo_variable,estacion,inicio,fin):
             
            # creo tag de varaible con su tipo designado
            lista = AnalisisDatos.transformar_sensores_para_analisis(lista,tipo_variable)
            
            # defino el largo total de los datos 
            TotalDatos = len(pd.date_range(inicio,fin,freq='10Min'))
            print(inicio)
            print(fin)
            # print('largo total')
            # print(TotalDatos)
            
            # defino vectores para contar datos no válidos
            no_validos = []

            # dataframe para modificar numericamente
            df = datos.copy()
                    
            # transformo la copia a numerico y cuento los valores validos de la columna
            for col in datos.columns:
                df[col] = pd.to_numeric(df[col],errors='coerce')
                no_validos.append(df[col].count())
                print(df[col].count())
                
            # defino vector para almacenar la disponibilidad de cada variable
            disponibilidad_por_variable = []
            
            # almaceno la disponibilidad de cada variable 
            for var in no_validos:
                disponibilidad_por_variable.append(round(var/TotalDatos,2))

            # agrego disponibilidad
            df.iloc[0] = disponibilidad_por_variable
            
            # elijo la variable que quiero mostrar la disponibilidad
            # print('disponibilidad:')
            # print(df[lista[0]][0])
            # print(df.iloc[0])
            # print(lista)
            
            
################################################################################
######################### VALIDACION Y FILTRADO ################################ 
################################################################################

    class ValidacionDatos():
        
        def exportar_validados(datos,nombre_archivo):
            datos.to_csv(nombre_archivo,sep='\t',index=False)
        
        def filtrar_repetidos_consecutivos(dataframe, columna, repeticiones):
   
            contador = 1
            filas_filtradas = []
            for i in range(1, len(dataframe)):
                if dataframe[columna][i] == dataframe[columna][i-1]:
                    contador += 1
                else:
                    contador = 1
                if contador == repeticiones:
                    filas_filtradas.extend(range(i+1-repeticiones, i+1))
            
            dataframe[columna].iloc[filas_filtradas] = np.nan

            return dataframe[columna]
        
        def filtrar_pendientes_iguales_consecutivas(dataframe, columna, n):
            
            pendiente_anterior = None
            pendientes_consecutivas = 0
            filas_filtradas = []
            
            for i in range(1, len(dataframe)):
                pendiente_actual = dataframe[columna][i] - dataframe[columna][i-1]
                
                if pendiente_actual == pendiente_anterior:
                    pendientes_consecutivas += 1
                else:
                    pendiente_anterior = pendiente_actual
                    pendientes_consecutivas = 1
                    
                if pendientes_consecutivas == n:
                    filas_filtradas.extend(range(i+1-n, i+1))
            
            dataframe[columna].iloc[filas_filtradas] = np.nan

            return dataframe[columna]
            
        
        def filtrado_datos_congelados(dataframe,n):
            
            for i in range(1,len(dataframe.columns),4):
    
                dataframe[dataframe.columns[i]] = AnalisisDatos.ValidacionDatos.filtrar_repetidos_consecutivos(dataframe,dataframe.columns[i],3)
                dataframe[dataframe.columns[i]] = AnalisisDatos.ValidacionDatos.filtrar_pendientes_iguales_consecutivas(dataframe,dataframe.columns[i],3)

            return dataframe
        
        # rangos de datos
        def rangos_de_validez(datos,tipo_variable,lista,limites):
            
            # creo tag de varaible con su tipo designado
            lista = AnalisisDatos.transformar_sensores_para_analisis(lista,tipo_variable)

            # separpo los tipos de variables del diccionario            
            tipos = list(limites.keys())

            # filtro por cada tipo de variable por c
            for tipo in tipos:                
                for sensor in lista:
                    if tipo in sensor:          
                        # establezco condiciones
                        cond1 = datos[sensor]>=limites[tipo][0]
                        cond2 = datos[sensor]<=limites[tipo][1]        
                        # aplico
                        datos = datos[cond1]
                        datos = datos[cond2]

            
            
            # AnalisisDatos.ValidacionDatos.exportar_validados(datos,'datosPI.txt')
            datos.to_csv('datosPI.txt',sep='\t',index=False)
            return datos
        
        # subarashii
        # clase para trabajar unicamente con anemometros ficticios
        class AnemometrosFicticios():
        #     
            # funcion para crear etiquetas de ficticios desde nombres y alturas 
            def crear_etiquetas_ficticios(lista):                
                
                lista_desglozada = AnalisisDatos.desglozar_sensores(lista)
                # lista para almacenar alturas
                alturas = []
                for i in range(0,len(lista_desglozada['Tipo'])):
                    if 'Anemómetro' in lista_desglozada['Tipo'][i]:
                        # almaceno altura
                        alturas.append(float(lista_desglozada['Altura'][i]))
               
                # encuentro alturas duplicadas
                # alturas_ficticios = [x for i, x in enumerate(alturas) if x in alturas[:i]]
                alturas_ficticios = AnalisisDatos.ascociar_alturas_cercanas(alturas)
                # falta agragar que cree la etiqueta cuando la altura sea próxima

                for h in range(0,len(alturas_ficticios)):
                    
                    alturas_ficticios[h] = 'AneFict'+str(h+1)+'_'+alturas_ficticios[h]+'_'          
                    lista.append(alturas_ficticios[h])

                # lista1 = sorted(lista)

                return sorted(lista)
                    
                        
                        
            def crear_ficticios(lista):
                
                print('Creando ficticios...')
                        
                return AnalisisDatos.ValidacionDatos.AnemometrosFicticios.crear_etiquetas_ficticios(lista)
            
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
            