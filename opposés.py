import pandas as pd

# Charger le fichier Excel
file_path = '/Users/arivain/Desktop/infirmieres_liberales_sans_doublons.xlsx'  # Remplacer par le chemin de votre fichier

df = pd.read_excel(file_path)

# Compter le nombre de personnes avec le numéro 'Opposé aux opérations de marketing'
nb_personnes_opposees = df[df['Numero'] == 'Opposé aux opérations de marketing'].shape[0]

print("Nombre de personnes opposées aux opérations de marketing:", nb_personnes_opposees)

# Supprimer les personnes dont le numéro est 'Opposé aux opérations de marketing'
df_cleaned = df[df['Numero'] != 'Opposé aux opérations de marketing']

# Enregistrer le DataFrame nettoyé dans un nouveau fichier Excel
cleaned_file_path = '/Users/arivain/Desktop/infirmieres_liberales_cleaned.xlsx'  # Remplacer par le chemin souhaité pour le fichier nettoyé
df_cleaned.to_excel(cleaned_file_path, index=False)

print(f"Fichier nettoyé enregistré sous : {cleaned_file_path}")