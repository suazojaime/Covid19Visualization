import pandas as pd
from datetime import datetime, timedelta, date
from matplotlib import pyplot as plt
import matplotlib

import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


df_totales = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto1/Covid-19_std.csv',sep=',')
df_actuales = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto25/CasosActualesPorComuna_std.csv',sep=',')
df_paso = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto74/paso_a_paso_std.csv',sep=',')
                       
df_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto38/CasosFallecidosPorComuna_std.csv',sep=',')

Comuna = 'San Felipe'


codigo = df_paso[df_paso['comuna_residencia'] == Comuna]['codigo_comuna'].unique()[0]

print(df_paso['comuna_residencia'].sort_values().unique())

df_actuales['Fecha'] = df_actuales['Fecha'].astype('datetime64')

df_comuna =  df_actuales[df_actuales['Codigo comuna'] == codigo]



df_paso_comuna = df_paso[df_paso['codigo_comuna'] == codigo]
df_paso_comuna['Fecha'] = df_paso_comuna['Fecha'].astype('datetime64')


df_fallecidos_comuna = df_fallecidos[df_fallecidos['Codigo comuna'] == codigo]
df_fallecidos_comuna['Fecha'] = df_fallecidos_comuna['Fecha'].astype('datetime64')


def paso_fecha(fecha):
    try:
        paso_ = df_paso_comuna['Paso'][df_paso_comuna['Fecha'] == fecha].values[0]
    except:
        paso_ = 0
    return paso_
    
df_comuna['Paso'] = df_comuna['Fecha'].apply(paso_fecha)


fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(df_comuna['Fecha'],df_comuna['Casos actuales'], label='Casos actuales',color = 'black', marker='o', markersize=3)
ax.plot(df_fallecidos_comuna['Fecha'],df_fallecidos_comuna['Casos fallecidos'], label = 'Fallecidos',color='green')
ax.legend(loc=1)
#ax.axvspan(datetime(2021, 4, 8), datetime(2021, 4, 20), alpha=0.2, color='red')



xfmt = mdates.DateFormatter('%Y-%m-%d')



ax1 = ax.twinx()



ax1.set_yticks([])



ax.fill_between(df_comuna['Fecha'],df_comuna['Casos actuales'],y2 = 0,where= df_comuna['Paso']==1  , alpha=0.4, color = 'r',label= 'Cuarentena')
ax.fill_between(df_comuna['Fecha'],df_comuna['Casos actuales'],y2 = 0,where= df_comuna['Paso']==2  , alpha=0.4, color = 'orange',label= 'Transición')
ax.fill_between(df_comuna['Fecha'],df_comuna['Casos actuales'],y2 = 0,where= df_comuna['Paso']==3  , alpha=0.4, color = 'yellow',label= 'Preparación')
ax.fill_between(df_comuna['Fecha'],df_comuna['Casos actuales'],y2 = 0,where= df_comuna['Paso']==4  , alpha=0.4, color = 'blue',label= 'Apertura')

ax.legend(loc=2)



ax1.xaxis.set_major_formatter(xfmt)
plt.setp(ax.xaxis.get_majorticklabels(), rotation=-80)
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=15))

ax.set_zorder(ax1.get_zorder()+1)
ax.patch.set_visible(False)

fig.subplots_adjust(bottom=0.3)


plt.title('Casos actuales comuna de ' + Comuna)

plt.draw()
plt.pause(0.0001)
