# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 04:38:52 2022

@author: Juan
"""
from tkinter import ttk
import numpy as np
import tkinter as tk
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from scipy import stats
from statistics import mode

#----------------------------------------------------------------------

archivo="abalone.csv"
datos=pd.read_csv(archivo)
datos.columns=["Sex","length","Diameter","Heigth","Whole Heigth","Shucked weight","Viscera weight","Shell weight","Rings"]

#--------------------------------------------------------------------------


root = tk.Tk()
frame = tk.Frame(root)

root.title('Graficadora')
root.geometry('820x850')
root.minsize(width=820, height=800)
root.maxsize(width=1000, height=800)
root.configure(bg='aquamarine')



#-----------------------------------------------------------------------------------


def check_a():
    if(int_atipico.get()==1):
        txtalpha.grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)
    elif int_atipico.get()==0:
        txtalpha.grid_forget()
    

def graficas(event): 
    seleccion = seleccion_grafica.get()
    check_atipico.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)
    btnGraficar.grid(column=0, row=7, sticky=tk.W, padx=5, pady=5)
    
    if seleccion=="Scatter":
        btnGraficar.grid(column=0, row=10, sticky=tk.W, padx=5, pady=5)
        labe2_text.grid(column=0, row=7, sticky=tk.W, padx=5, pady=5)
        combo3.grid(column=0, row=8, sticky=tk.W, padx=5, pady=5)
    else:
        labe2_text.grid_forget()
        combo3.grid_forget()
        

def eliminarAtipicos(Variable,alpha,DF):

    Data=DF
    Q1=np.percentile(Data[Variable], 25,
               method = 'midpoint')
    Q3=np.percentile(Data[Variable], 75,
               method = 'midpoint')
    IQR=Q3-Q1

    upper = np.where(DF[Variable] >= (Q3 + alpha * IQR))

    lower = np.where(DF[Variable] <= (Q1 - alpha * IQR))
    Data.drop(upper[0], inplace = True)
    Data.drop(lower[0], inplace = True)
    return DF


def tipo_curtosis(c):
    
    if c >0:
        Tcur = tk.Label(root, text="Distribución Leptocurtica", bg='aquamarine', font=('arial',12))
        Tcur.place(x=600,y=520)
    elif c<0:
        Tcur = tk.Label(root, text="Distribución platicurtica", bg='aquamarine', font=('arial',12))
        Tcur.place(x=600,y=520)
    else:
        Tcur = tk.Label(root, text="Distribución Mesocurtica", bg='aquamarine', font=('arial',12))
        Tcur.place(x=600,y=520)


def tipo_asimetria(media,mediana,moda):
    if media < mediana < moda: #Asimetria negativa(A la izquierda)
        TAsime = tk.Label(root, text="Asimetría negativa", bg='aquamarine', font=('arial',12))
        TAsime.place(x=600,y=540)
    elif media > mediana > moda: #Asimetria positiva(a la derecha)
        TAsime = tk.Label(root, text="Asimetría positiva", bg='aquamarine', font=('arial',12))
        TAsime.place(x=600,y=540)
    elif moda == media == mediana:
        TAsime = tk.Label(root, text="Simétrica", bg='aquamarine', font=('arial',12))
        TAsime.place(x=600,y=540)
        

def graficar():
    fig.clear()
    datos2 = datos.copy()
    plot = fig.add_subplot(111)
    canvas.get_tk_widget().place(x=300,y=20)
    
    media = datos2[seleccion_variable.get()].mean()
    Txmedia = "Media: " + str(media)
    Tmedia = tk.Label(root, text=Txmedia, bg='aquamarine', font=('arial',12))
    Tmedia.place(x=300,y=520)
    
    moda = mode(datos2[seleccion_variable.get()])
    Txmoda = "Moda: " + str(moda)
    Tmoda = tk.Label(root, text=Txmoda, bg='aquamarine', font=('arial',12))
    Tmoda.place(x=300,y=600)
    
    mediana = datos2[seleccion_variable.get()].median()
    Txmediana = "Mediana: " + str(mediana)
    Tmediana = tk.Label(root, text=Txmediana, bg='aquamarine', font=('arial',12))
    Tmediana.place(x=300,y=540)
    
    asimetria = datos2[seleccion_variable.get()].skew()
    Txasimetria = "Asimetria: " + str(asimetria)
    Tasimetria = tk.Label(root, text=Txasimetria, bg='aquamarine', font=('arial',12))
    Tasimetria.place(x=300,y=560)
    

    curtosis=datos2[seleccion_variable.get()].kurtosis()
    Txcurtosis= "Curtosis: " + str(curtosis)
    Tcurtosis = tk.Label(root, text=Txcurtosis, bg='aquamarine', font=('arial',12))
    Tcurtosis.place(x=300,y=580)
    
    tipo_curtosis(curtosis)
    tipo_asimetria(media,mediana,moda)
    
    if(int_atipico.get()==1):
        alpha=float(txtalpha.get(1.0, "end-1c"))
        datos_atipicos = eliminarAtipicos(seleccion_variable.get(), alpha, datos2)
        
        if seleccion_grafica.get() == 'Histogram':
            
            plot.hist(datos_atipicos[seleccion_variable.get()])
            canvas.draw()
            
        if seleccion_grafica.get() == 'Scatter':
            datos_atipicos2 = eliminarAtipicos(seleccion_variable2.get(), alpha, datos2)
            plot.scatter(datos_atipicos[seleccion_variable.get()],datos_atipicos2[seleccion_variable2.get()])
            canvas.draw()
        
        if seleccion_grafica.get() == 'Box plot':
            
            plot.boxplot(datos_atipicos[seleccion_variable.get()])
            canvas.draw()
            
        if seleccion_grafica.get() == 'Norm plot':

             stats.probplot(datos_atipicos[seleccion_variable.get()],dist=stats.norm, sparams=(6,),plot=plot)
             canvas.draw()
        

    else:
        if seleccion_grafica.get() == 'Histogram':
            
            plot.hist(datos2[seleccion_variable.get()])
            canvas.draw()
            
        if seleccion_grafica.get() == 'Scatter':
            
            plot.scatter(datos2[seleccion_variable.get()],datos2[seleccion_variable2.get()])
            canvas.draw()
        
        if seleccion_grafica.get() == 'Box plot':
            
            plot.boxplot(datos2[seleccion_variable.get()])
            canvas.draw()
            
        if seleccion_grafica.get() == 'Norm plot':

             stats.probplot(datos2[seleccion_variable.get()],dist=stats.norm, sparams=(6,),plot=plot)
             canvas.draw()
    
    
#-------------------------------------------------------


label_text = tk.Label(root, text="Escoge una gráfica:", bg='aquamarine', font=('arial',12))
label_text.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)


label1_text = tk.Label(root, text="Escoge una variable:", bg='aquamarine', font=('arial',12))
label1_text.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)


seleccion_variable = tk.StringVar()
combo = ttk.Combobox(textvariable=seleccion_variable,state='readonly',values=["Sex","length","Diameter","Heigth","Whole Heigth","Shucked weight","Viscera weight","Shell weight","Rings"])
combo.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)


seleccion_grafica = tk.StringVar()
combo2 = ttk.Combobox(textvariable=seleccion_grafica,state='readonly',values=["Histogram", "Box plot", "Norm plot", "Scatter"])
combo2.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)


seleccion_variable2 = tk.StringVar()
labe2_text = tk.Label(root, text="Escoge la segunda variable:", bg='aquamarine', font=('arial',12))
combo3 = ttk.Combobox(textvariable=seleccion_variable2,state='readonly',values=["Sex","length","Diameter","Heigth","Whole Heigth","Shucked weight","Viscera weight","Shell weight","Rings"])


int_atipico = tk.IntVar()
txtalpha = tk.Text(root,height=1, width=15)
check_atipico = tk.Checkbutton(root,command=check_a, text='Sin atípicos. Escria el valor de alpha', variable=int_atipico, bg='aquamarine',font=('arial',12),onvalue=1,offvalue=0)
#-------------------------------------------------------------


fig = Figure(figsize=(5, 5), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)


#-------------------------------------------------------------


btnGraficar = tk.Button(root, text ="Graficar",width=15,height=2,command=graficar)
btnGraficar.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)


combo2.bind("<<ComboboxSelected>>",graficas)
tk.mainloop()

