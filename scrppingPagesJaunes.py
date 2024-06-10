from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import openpyxl
import os


# Fonction pour lire l'état de la dernière page parcourue
def lire_etat():
    if os.path.exists("etat_page.txt"):
        with open("etat_page.txt", "r") as f:
            return int(f.read())
    return 0

# Fonction pour sauvegarder l'état de la dernière page parcourue
def sauvegarder_etat(page):
    with open("etat_page.txt", "w") as f:
        f.write(str(page))


# Initialiser le fichier Excel
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Infirmieres Liberales 2"
ws.append(["Prénom", "Numéro"])

compteur_page = lire_etat()

# Initialiser le navigateur 
driver = webdriver.Chrome()

# Ouvrir la page web
driver.get("https://www.pagesjaunes.fr/annuaire/bordeaux-33/infirmiere")

# Attendre que le bouton soit présent et cliquer dessus
wait = WebDriverWait(driver, 10)
time.sleep(1)
print("on accepte les cookies")
button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='didomi-notice-agree-button']"))) 
button.click()
print("cookies acceptés")
time.sleep(1)

compteur_page = 0
while compteur_page < 498:

    time.sleep(1)
    print("on cherche la liste")
    try:
        list_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="listResults"]/div/ul/*'))) 
        compteur_liste = 0

        for element in list_elements:
            if compteur_liste != 19 :
                try:
                    # Extraire le numéro de l'élément à partir de son XPath
                    element_id = element.get_attribute("id")
                    element_number = element_id.split("-")[-1]
                    print("element_number: ", element_number)
                    
                    # Construire l'XPath du bouton correspondant
                    button_xpath = f'//*[@id="epj-{element_number}"]/div[3]/button' 
                    print("button_xpath: ", button_xpath)
                    
                    # Cliquer sur le bouton correspondant
                    try:
                        button = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="epj-{element_number}"]/div[3]/button')))
                    except:
                        button = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="epj-{element_number}"]/div[2]/button' )))
                    button.click() 
                    
                    # Essayer de récupérer le numéro de téléphone avec le premier XPath
                    try:
                        num_de_tel = wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="bi-fantomas-{element_number}"]/div[1]/span')))
                    except:
                        try:
                            num_de_tel = wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="bi-fantomas-{element_number}"]/div[2]/span')))
                        except:
                            num_de_tel = wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="bi-fantomas-{element_number}"]/div/span')))

                    prenom = wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="epj-{element_number}"]/div[1]/div[2]/div/div[1]/a/h3')))
                    
                    # Récupérer le texte de l'élément
                    numero = num_de_tel.text
                    nom = prenom.text
                    print("Numéro récupéré :", numero)
                    print("Prénom récupéré :", nom)
                    ws.append([nom, numero])

                    compteur_liste += 1
                    print("compteur_liste:", compteur_liste)

                except Exception as e:
                    print(f"Erreur lors du traitement de l'élément {element_number}: {e}")
    
        compteur_page += 1
        wb.save("infirmieres_liberales.xlsx")

        sauvegarder_etat(compteur_page)

        print("pane numero ", compteur_page)
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='pagination-next']"))) 
        button.click()

    except: 
        print("erreur de page")
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='pagination-next']"))) 
        compteur_page += 1

        button.click()
        
# Fermer le navigateur
driver.quit()

