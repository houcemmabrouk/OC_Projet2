# OC_Projet2
Depot pour le projet 2
Ce code permet d'extraire à partir du site http://books.toscrape.com/ les informations suivantes pour tous les livres :
product_page_url, universal_ product_code (upc), title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating,image_url
Les sauvegarder dans un fichier scrap.csv
Sauvegarder les couvertures des livres dans un dossier book_images qui sera placé dans le currrent working directory
Pour utiliser ce programme vous aurez besoin d'effectuer ceci dans votre terminal : 
# Installer python 3.8
>sudo apt install python3.8

# Installer un environnement virtuel
>mkdir mon-nouveau-projet-python
>cd mon-nouveau-projet-python
>virtualenv --python = python3 venv

# Activer un environnement virtuel
>cd mon-nouveau-projet-python
>source venv / bin / activate

# Installer les bibliothèques python requises avec les commandes suivantes
pip install requests
pip install bs4
pip install os
