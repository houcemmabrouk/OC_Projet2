import requests
from bs4 import BeautifulSoup
import csv


#to do list

#CSV ETL
#optimize page counting
#operateurs simplifies
#Requirements.txt
#Milestones & Issues
#PEP 8
#Git commit


#I Write_All_Urls_In_List

#1A-Variables Initialization
url = ""
j = 0
count = 0
url_list = []
dictionnaire = {"Internal ID": None, "product_page_url": None, "universal_product_code": None,
                "title": None,"price_including_tax": None,"price_excluding_tax": None,
                "number_available":None,"product_description": None, "category": None,
                "review_rating":None, "image_url":None
                }

#1B-Counting number of pages utiliser boucle while

#1C-Searching for all valid urlsgit st
for i in range(1,51):

    page = "http://books.toscrape.com/catalogue/category/books_1/page-" + str(i) + ".html"
    pageResponse = requests.get(page)
    if pageResponse.ok:
            superSoup = BeautifulSoup(pageResponse.text,"html.parser")
            h3 = superSoup.find_all("h3")
            j= j + 1
            for article in h3:
                links = article.find("a")
                incomplete_url = links["href"]
                temp_url = url = incomplete_url.replace("../..","http://books.toscrape.com/catalogue")
                url_list.append(temp_url)


with open("scrap.csv", "w") as csvfile:
    #csvfile.write("Internal ID" + "," + "title" + "," + "category" + "," + "universal_ product_code" + "," + "price_excluding_tax" + "," + "price_including_tax" + "," + "number_available" + "," + "review_rating" + "," + "product_description" + "," + "review_rating" + "," + "product_page_url" + "," + "image_url")

    fieldnames = ["Internal ID", "product_page_url", "title", "product_description", "category", "image_url",
                  "universal_product_code", "price_excluding_tax", "price_including_tax",
                  "number_available", "review_rating"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for url in url_list:
        response = requests.get(url)

        if response.ok:
            count = count + 1
            list_result = []
            dictionnaire.update({"Internal ID": str(count)})

            #Extraction_url
            dictionnaire.update({"product_page_url" : url})

            #Extraction_title
            soup = BeautifulSoup(response.text,"html.parser")
            title = soup.find("h1")
            dictionnaire.update({"title": title.text.replace(",","")})


            #Extraction_descritpion
            description_parent = soup.find("h2")
            description = description_parent.findNext("p")
            dictionnaire.update({"product_description": description.text.replace(",","")})

            #Extraction_category
            category_parent = soup.find("ul")
            category_parent1 = category_parent.findNext("a")
            category_parent2 = category_parent1.findNext("a")
            category_parent3 = category_parent2.findNext("a")
            list_result.append(category_parent3.text)
            dictionnaire.update({"category": category_parent3.text})

            #Extraction_image_url
            image_url_parent = soup.find("article")
            image_url_parent1 = image_url_parent.find("img")
            #Attribut
            image_url_incomplete = image_url_parent1["src"]
            #Reconstruction
            image_url = image_url_incomplete.replace("../..","http://books.toscrape.com")
            dictionnaire.update({"image_url": image_url.replace(",","")})

            #Extraction_Remaining_Elements
            soup = BeautifulSoup(response.text,"html.parser")
            table = soup.find("table")
            tr = table.find_all("tr")
            temp_list_result = []
            for td in tr:
                info = td.find("td")
                info_formated = info.text
                info_formated1 = info_formated.replace("Â","")
                list_result.append(info_formated1)
                temp_list_result.append(info_formated1.replace(",",""))

            dictionnaire.update({"universal_product_code": temp_list_result[0]})
            dictionnaire.update({"price_excluding_tax": temp_list_result[2]})
            dictionnaire.update({"price_including_tax": temp_list_result[3]})
            dictionnaire.update({"number_available": temp_list_result[5]})
            dictionnaire.update({"review_rating": temp_list_result[6]})


            #Writing alternative method
            #csvfile.write(dictionnaire["Internal ID"] + "," + dictionnaire["title"] + "," + dictionnaire["category"] + "," + dictionnaire["universal_product_code"] + "," + dictionnaire["price_excluding_tax"] + "," + dictionnaire["price_including_tax"] + "," + dictionnaire["number_available"] + "," + dictionnaire["review_rating"] + "," + dictionnaire["product_description"] + "," + dictionnaire["review_rating"] + "," + dictionnaire["product_page_url"] + "," + dictionnaire["image_url"] + '\n')

            #CSV data writing
            writer.writerow({"Internal ID": dictionnaire["Internal ID"],
                             "title" : dictionnaire["title"],
                             "product_page_url": dictionnaire["product_page_url"],
                             "product_description": dictionnaire["product_description"],
                             "category": dictionnaire["category"],
                             "image_url": dictionnaire["image_url"],
                             "universal_product_code": dictionnaire["universal_product_code"],
                             "price_excluding_tax": dictionnaire["price_excluding_tax"],
                             "price_including_tax": dictionnaire["price_including_tax"],
                             "number_available": dictionnaire["number_available"],
                             "review_rating": dictionnaire["review_rating"]
                            })


