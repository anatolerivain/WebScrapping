import pandas as pd

# Lire le fichier Excel
file_path = '/Users/arivain/Desktop/infirmieres_liberales_7000_3.xlsx'  # Remplacer par le chemin de votre fichier
df = pd.read_excel(file_path, header=None, names=["Prenom", "Numero"])

df_no_duplicates = df.drop_duplicates(keep='first')
new_file_path = '/Users/arivain/Desktop/infirmieres_liberales_sans_doublons.xlsx'
df_no_duplicates.to_excel(new_file_path, index=False)
print(f"Fichier sans doublons enregistré dans {new_file_path}")
