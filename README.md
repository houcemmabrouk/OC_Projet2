# books_scrapper
Ce code permet d'extraire à partir du site http://books.toscrape.com/ les informations suivantes pour tous les livres :
- product_page_url
- universal_ product_code (upc)
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url
- Les sauvegarder dans un fichier scrap.csv
- Sauvegarder les couvertures des livres dans un dossier book_images qui sera placé dans le currrent working directory

Pour utiliser ce programme vous aurez besoin d'effectuer ceci dans votre terminal : 

# Téléchargement du projet
Dans le Terminal executez la commande suivante
- git clone [https://github.com/houcemmabrouk/OC_Projet2.git]

# Installer un environnement virtuel
Dans le Terminal executez les commandes suivantes
- mkdir mon-nouveau-projet-python
- cd mon-nouveau-projet-python
- python -m venv env

# Activer un environnement virtuel
Dans le Terminal executez la commande suivante
- source env/bin/activate

# Installer les dependances
Dans le Terminal executez la commande suivante
- pip install -r requirements.txt 
