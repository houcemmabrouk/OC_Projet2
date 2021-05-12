import requests
from bs4 import BeautifulSoup
import csv
import time
import os.path

# Variables initialization
urls = []
product_info = {"internal_id": None, "product_page_url": None, "universal_product_code": None,
               "title": None, "price_including_tax": None, "price_excluding_tax": None,
               "number_available": None, "product_description": None, "category": None,
               "review_rating": None, "image_url": None
               }
all_product_info = {}

# scraper returns data for specific soup givin a specifc HTML tag to a specific Sublevel
def scraper(level, html_tag, soup):
    for level_counter in range(level):
        soup = soup.findNext(html_tag)
    return soup.text

# Store all category_url in category_urls []
def generate_category_urls(homepage_url):
    homepage_response = requests.get(homepage_url)
    homepage_soup = BeautifulSoup(homepage_response.text, "html.parser")
    categorySoup = homepage_soup.find("ul", class_="nav nav-list").find("li").find("ul").find_all("li")

    category_urls = []
    for souptemp in categorySoup:
        a = souptemp.find("a")
        link = a["href"]
        category_urls.append("http://books.toscrape.com/" + link)
    return category_urls
category_urls = generate_category_urls("http://books.toscrape.com")
print("category urls found and generated " + str(len(category_urls)))

# generate_all_pages_of_one_category stores all books pages of a single category
def generate_all_pages_of_one_category(category_url):
    pages = []
    pages.append(category_url)
    page_number = 2
    page = category_url.replace("index", "page-2")
    page_response = requests.get(page)
    while page_response.ok:
        page = page.replace("index", "page-2")
        pages.append(page)
        page_number = int(page[len(page) - 6])
        page_number += 1
        page = page.replace("page-" + str(page[len(page) - 6]), "page-" + str(page_number))
        page_response = requests.get(page)
    return pages

# generate_all_urls_of_one_page stores all books urls of a single page
def generate_all_urls_of_one_page(page_url):
    urls =[]
    page_response = requests.get(page_url)
    if page_response.ok:
        super_soup = BeautifulSoup(page_response.text, "html.parser")
        h3 = super_soup.find_all("h3")
        for article in h3:
            links = article.find("a")
            incomplete_url = links["href"]
            temp_url = url = incomplete_url.replace("../../..", "http://books.toscrape.com/catalogue")
            urls.append(temp_url)
    return urls

# utf8_format translates string from latin-1 to utf-8
def utf8_format(text):
    return text.encode("latin-1").decode("utf-8")

# generate_all_urls_of_one_page stores all books urls of a single page
def generate_categorys_pages(categorys_list):
    categorys_pages = []
    for category_url in categorys_list:
        categorys_pages.extend(generate_all_pages_of_one_category(category_url))
    return categorys_pages
all_category_pages = (generate_categorys_pages(category_urls))

# generate_all_urls_of_one_page stores all books urls of a single page
def generate_all_books_url(categorys_pages_list):
    books_url = []
    for page in categorys_pages_list:
        books_url.extend(generate_all_urls_of_one_page(page))
    return books_url
urls_store =[]
urls_store = generate_all_books_url(all_category_pages)

# scrap : scrapes an url_list and stores data into all_product_info
def scrap(url_list):
    for url in url_list:
        response = requests.get(url)
        if response.ok:
            product_info= {}
            soup = BeautifulSoup(response.text, "html.parser")

            # Add internal_id to product_info
            internal_id = str(url_list.index(url))
            product_info.update({ "internal_id" : internal_id})

            # Add product_page_url to product_info
            product_page_url = url
            product_info.update({"product_page_url" : url})

            # Add title to product_info
            title = utf8_format(scraper(0, "title", soup.find("h1")))
            product_info.update({"title": title})

            # Add product_description to product_info
            product_description = utf8_format((scraper(1, "p", soup.find("h2"))))
            product_info.update({"product_description": product_description})

            # Add category to product_info
            category = utf8_format((scraper(3, "a", soup.find("ul"))))
            product_info.update({"category": category})

            # Add image_url to product_info
            incomplete_image_url = (soup.find("article").find("img")["src"])
            image_url = incomplete_image_url.replace("../..","http://books.toscrape.com")
            product_info.update({"image_url": image_url})

            # Add universal_product_code to product_info
            universal_product_code = (scraper(1, "td", soup.find("table").find("tr")))
            product_info.update({"universal_product_code": universal_product_code})

            # Add price_excluding_tax to product_info
            price_excluding_tax = utf8_format((scraper(3, "td", soup.find("table").find("tr"))))
            product_info.update({"price_excluding_tax": price_excluding_tax})

            # Add price_including_tax to product_info
            price_including_tax = utf8_format((scraper(4, "td", soup.find("table").find("tr"))))
            product_info.update({"price_including_tax": price_including_tax})

            # Add number_available to product_info
            number_available = utf8_format((scraper(6, "td", soup.find("table").find("tr"))))
            product_info.update({"number_available": number_available})

            # Add review_rating to product_info
            review_rating = utf8_format((scraper(7, "td", soup.find("table").find("tr"))))
            product_info.update({"review_rating": review_rating})

            # Store product_info item in all_product_info
            all_product_info[internal_id] = product_info
            print("Book n° " + product_info["internal_id"] + " " + product_info["title"] + " scrapping completed")
    return all_product_info


# write book info from all_product_info into scrap.csv
def write_csv(all_product_info_dict):
    with open("scrap.csv", "w") as csvfile:
        fieldnames = ["internal_id", "product_page_url", "title", "product_description", "category", "image_url",
                      "universal_product_code", "price_excluding_tax", "price_including_tax",
                      "number_available", "review_rating"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for index in all_product_info:
            #CSV data writing
            writer.writerow({"internal_id": all_product_info[index]["internal_id"],
                             "title": all_product_info[index]["title"],
                             "product_page_url": all_product_info[index]["product_page_url"],
                             "product_description": all_product_info[index]["product_description"],
                             "category": all_product_info[index]["category"],
                             "image_url": all_product_info[index]["image_url"],
                             "universal_product_code": all_product_info[index]["universal_product_code"],
                             "price_excluding_tax": all_product_info[index]["price_excluding_tax"],
                             "price_including_tax": all_product_info[index]["price_including_tax"],
                             "number_available": all_product_info[index]["number_available"],
                             "review_rating": all_product_info[index]["review_rating"]
                            })
    csvfile.close()
    print("all data saved in scrap.csv file")

# Saving book picture in image folder
def save_pictures(all_product_info_dict):
    # Target directory creation
    directory = "book_images"
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, directory)
    if not os.path.exists(path):
        os.makedirs(path)

    # Save image in target directory
    for index in all_product_info:
        image_url = all_product_info[index]["image_url"]
        universal_product_code = all_product_info[index]["universal_product_code"]
        imageRequest = requests.get(image_url, allow_redirects=True)
        imageFileName = path + "/" + universal_product_code + ".jpg"
        open(imageFileName, 'wb').write(imageRequest.content)
        print("Book n° " + all_product_info[index]["internal_id"] + " " + all_product_info[index]["title"] + " picture saved")

all_product_info = scrap(urls_store)
write_csv(all_product_info)
save_pictures(all_product_info)
