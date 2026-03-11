import pandas as pd

# Leer el archivo CSV
df = pd.read_csv("src/data/data_entries.csv")

# Rellenar los valores vacíos en la columna 'accidentType' con "ninguna"
df['accidentType'] = df['accidentType'].fillna('ninguna')

# También rellenar strings vacíos con "ninguna"
df['accidentType'] = df['accidentType'].replace('', 'ninguna')

# Rellenar los valores vacíos en la columna 'accidentSeverity' con "ninguna"
df['accidentSeverity'] = df['accidentSeverity'].fillna('ninguna')

# También rellenar strings vacíos con "ninguna"
df['accidentSeverity'] = df['accidentSeverity'].replace('', 'ninguna')

# Guardar el archivo CSV actualizado
df.to_csv("src/data/data_entries.csv", index=False)

print("Archivo limpiado exitosamente!")
print(f"Total de registros: {len(df)}")
print(f"Registros con 'ninguna' en accidentType: {len(df[df['accidentType'] == 'ninguna'])}")
print(f"Registros con 'ninguna' en accidentSeverity: {len(df[df['accidentSeverity'] == 'ninguna'])}")