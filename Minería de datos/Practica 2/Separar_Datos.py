import pandas as pd

# 1. Cargar el log
df = pd.read_csv('ExampleLog.csv')

# 2. Definir qué actividades son "Atención"
actividades_atencion = ['Handle Case', 'Handle email', 'Call outbound', 'email outbound']

# 3. Identificar los IDs que tienen al menos una actividad de atención
ids_con_atencion = df[df['Activity'].isin(actividades_atencion)]['Case ID'].unique()

# 4. Separar el dataframe original basado en esos IDs
df_atendidos = df[df['Case ID'].isin(ids_con_atencion)]
df_no_atendidos = df[~df['Case ID'].isin(ids_con_atencion)]

# 5. Guardar los dos nuevos CSVs
df_atendidos.to_csv('Casos_Con_Atencion.csv', index=False)
df_no_atendidos.to_csv('Casos_Sin_Atencion.csv', index=False)
input()