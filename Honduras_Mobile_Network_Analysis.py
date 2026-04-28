import pandas as pd
import matplotlib.pyplot as plt


#Ajust the digit outputs
pd.options.display.float_format = '{:.2f}'.format

#Extracting the document that comes from the national reports

file = "API_HND_DS2_es_csv_v2_21843.csv"

try:
    datos = pd.read_csv(file, skiprows=4, encoding='utf-8')
except FileNotFoundError:
    print(f"Archivo no encontrado: {file}")
    exit() 

#Delete the empty column that is named "Unnamed"
datos = datos.loc[:, ~datos.columns.str.contains('^Unnamed')]

#With this variable we can easily adjust the years that we want to compare
años = [str(anio) for anio in range(2000, 2024)]
columna_años = [a for a in años if a in datos.columns]
assert len(columna_años) > 0, "Ningún año del rango existe en el dataset"

#Look for the rows that we are going to compare
resultado_telefonia = datos[datos['Indicator Name'].str.contains("Suscripciones a telefonía celular móvil", na=False)]
resultado_poblacion_total = datos[datos['Indicator Name'].str.contains("Población, total",na=False)]

#early return
if resultado_telefonia.empty:
    print("No se encontró el indicador de telefonia")
    exit()
if resultado_poblacion_total.empty:
    print("No se encontró el indicador de poblacion total") 
    exit()

fila_pib_telefonia = resultado_telefonia.iloc[0]
fila_pib_poblacion_total = resultado_poblacion_total.iloc[0]


#Look for the columns values in such row
valores_telefonia = fila_pib_telefonia[columna_años]
valores_poblacion_total = fila_pib_poblacion_total[columna_años]

penetracion = (valores_telefonia / valores_poblacion_total) * 100
penetracion = pd.to_numeric(penetracion, errors='coerce')  # <- agregar esta línea



#initializing the graph
fig, (ax, ax2) = plt.subplots(2, 1, figsize=(16, 10))
plt.tight_layout(h_pad=4)
ax.plot(columna_años, valores_telefonia,marker="o", color='red', label='Suscripciones a telefonía celular móvil')
ax.plot(columna_años, valores_poblacion_total, color='green', label='Poblacion total')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))


ax.set_title('Comparación entre población total y redes de telefonia movil')
ax.set_xlabel('Años')
ax.set_ylabel('Suscripciones')
ax.legend()
plt.xticks(rotation=45)


ax2.plot(columna_años, penetracion, marker="o", color='purple', linewidth=2)
ax2.axhline(y=100, color='gray', linestyle='--', alpha=0.6, label='100% — 1 SIM por persona')
ax2.axvline(x='2011', color='red', linestyle='--', alpha=0.6, label='Ley de Escuchas (2011)')
ax2.fill_between(columna_años, penetracion, alpha=0.1, color='purple')
ax2.set_title('Penetración celular en Honduras — suscripciones por cada 100 habitantes')
ax2.set_xlabel('Año')
ax2.set_ylabel('%')
ax2.legend()
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)


#Save and show
plt.savefig('Graph.png', dpi=150, bbox_inches='tight')
plt.show()



print(penetracion)