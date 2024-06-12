import math
import pandas as pd
import matplotlib.pyplot as plt
from numpy import linspace



def normalize(df): #min_max
    # copy the dataframe
    df_norm = df.copy()
    # apply min-max scaling
    for column in df_norm.columns:
        if(len(df_norm[column].unique()) > 1): #fix NaN generation
          df_norm[column] = (df_norm[column] - df_norm[column].min()) / (df_norm[column].max() - df_norm[column].min())
        else:
          df_norm[column] = 0
    return df_norm

#trata outliers dificudade
def trataOutliersDif(listDif):
  limMin = -3
  limMax =  3
  #limMin = -10
  #limMax =  10
  for i, val in enumerate(listDif):
    if val > limMax:
      listDif[i] = limMax
    else:
      if val < limMin:
        listDif[i] = limMin
  return listDif

def trataOutliersDis(listDis):
  limMin = -3
  limMax = 3
  #limMin = -2.5
  #limMax =  2.5
  #limMin = -10
  #limMax =  10
  for i, val in enumerate(listDis):
    if val > limMax:
      listDis[i] = limMax
    else:
      if val < limMin:
        listDis[i] = limMin
  return listDis

def trataOutliersGues(listGues):
  limMin = 0
  limMax =  1
  #limMin = -10
  #limMax =  10
  for i, val in enumerate(listGues):
    if val > limMax:
      listGues[i] = limMax
    else:
      if val < limMin:
        listGues[i] = limMin
  return listGues

def calcICC(a, b, c,theta):
  #return c + (1 - c) * (1/(1+math.e**(-a*(x_axis - b))))
  return c + ((1 - c) / (1 + math.e ** (-a * (theta - b))))

def plotICC(path_of_irt_item_param, path_out_plot, title):
  line = 0.3
  name_file = path_of_irt_item_param
  print('reading: '+name_file)
  dataset = pd.read_csv(name_file)
  dataset = dataset.drop('Unnamed: 0',axis=1)

  dataset['Dificuldade'] = trataOutliersDif(dataset['Dificuldade'])
  dataset['Discriminacao'] = trataOutliersDis(dataset['Discriminacao'])
  dataset['Adivinhacao'] = trataOutliersGues(dataset['Adivinhacao'])

  plt.figure(figsize=(6,5))
  for i in dataset.index:
    a = dataset['Discriminacao'][i]
    b = dataset['Dificuldade'][i]
    c = dataset['Adivinhacao'][i]
    x_axis = linspace(-6, 6, 100)
    y_axis = calcICC(a,b,c,x_axis)

    plt.plot(x_axis, y_axis,color='lightgray',linewidth=line)

  a = dataset['Discriminacao'].mean()
  b = dataset['Dificuldade'].mean()
  c = dataset['Adivinhacao'].mean()
  k = 0
  if a < 0:
    k = 0.5
  x_axis = linspace(-6,6, 100)
  y_axis = calcICC(a,b,c,x_axis)

  plt.text(-0,0.1+k,'Guessing: '+str(round(c,2)),fontsize=14)
  plt.text(0,0.2+k,'Discrimination: '+str(round(a,2)),fontsize=14)
  plt.text(0,0.3+k,'Difficulty: '+str(round(b,2)),fontsize=14)
  plt.plot(x_axis, y_axis,color='black')
  plt.ylabel('Probability of Correct Response P(Θ)',fontsize=16)
  plt.xlabel('Ability θ',fontsize=16)
  plt.title(title,fontsize=16)

  plt.savefig(path_out_plot)



