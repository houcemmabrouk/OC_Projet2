import requests
from bs4 import BeautifulSoup
import csv
import time
import os.path

# 1A-VariablesInitialization
productCount = 0
urls = []
productInfo = {"internal_id": None, "product_page_url": None, "universal_product_code": None,
               "title": None, "price_including_tax": None, "price_excluding_tax": None,
               "number_available": None, "product_description": None, "category": None,
               "review_rating": None, "image_url": None
               }

all_product_info = {}




# scraper returns data for specific soup givin a specifc HTML tag to a specific Sublevel
def scraper(level, HTMLtag, soup):
    for levelCounter in range(level):
        soup = soup.findNext(HTMLtag)
    return soup.text


# Store all category_url in category_urls []
def generate_category_urls(homepage_url):
    homepageResponse = requests.get(homepage_url)
    homepage_soup = BeautifulSoup(homepageResponse.text, "html.parser")
    categorySoup = homepage_soup.find("aside").find("div").findNext("div").find("ul").find("li").find("ul").find_all("li")

    category_urls = []
    for souptemp in categorySoup:
        a = souptemp.find("a")
        link = a["href"]
        category_urls.append("http://books.toscrape.com/" + link)
    return category_urls
category_urls = generate_category_urls("http://books.toscrape.com")

# allPagesOneCategory stores all books pages of a single category
def allPagesOneCategory(categoryUrl):
    pages = []
    pages.append(categoryUrl)
    pageNumber = 2
    page = categoryUrl.replace("index", "page-2")
    pageResponse = requests.get(page)
    while pageResponse.ok:
        page = page.replace("index", "page-2")
        pages.append(page)
        pageNumber = int(page[len(page) - 6])
        pageNumber += 1
        page = page.replace("page-" + str(page[len(page) - 6]), "page-" + str(pageNumber))
        pageResponse = requests.get(page)
    return pages

# allUrlsOnePage stores all books urls of a single page
def allUrlsOnePage(pageUrl):
    urls =[]
    pageResponse = requests.get(pageUrl)
    if pageResponse.ok:
        superSoup = BeautifulSoup(pageResponse.text, "html.parser")
        h3 = superSoup.find_all("h3")
        for article in h3:
            links = article.find("a")
            incomplete_url = links["href"]
            temp_url = url = incomplete_url.replace("../../..", "http://books.toscrape.com/catalogue")
            urls.append(temp_url)
    return urls

# utf8Format translates string from latin-1 to utf-8
def utf8Format(text):
    return text.encode("latin-1").decode("utf-8")

def generate_categorys_pages(categorys_list):
    categorys_pages = []
    for category_url in categorys_list:
        categorys_pages.extend(allPagesOneCategory(category_url))
    return categorys_pages


all_category_pages = (generate_categorys_pages(category_urls))

#print(all_category_pages)

#print(len(all_category_pages))


def generate_all_books_url(categorys_pages_list):
    books_url = []
    for page in categorys_pages_list:
        books_url.extend(allUrlsOnePage(page))
    return books_url

urls_store =[]
urls_store = generate_all_books_url(all_category_pages)
#print(urls_store)
#print(len(urls_store))

def scrap_write(url_list):
    with open("scrap.csv", "w") as csvfile:
        fieldnames = ["internal_id", "product_page_url", "title", "product_description", "category", "image_url",
                      "universal_product_code", "price_excluding_tax", "price_including_tax",
                      "number_available", "review_rating"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        productCount = 0
        for url in url_list:
            #print(url)
            response = requests.get(url)
            if response.ok:
                productCount = productCount + 1
                #print(productCount)
                soup = BeautifulSoup(response.text, "html.parser")
                # Add internal_id to productInfo
                internal_id = str(productCount)
                productInfo.update({ "internal_id" : internal_id})

                # Add product_page_url to productInfo
                product_page_url = url
                productInfo.update({"product_page_url" : url})

                # Add title to productInfo
                title = utf8Format(scraper(0, "title", soup.find("h1")))
                productInfo.update({"title": title})

                # Add product_description to productInfo
                product_description = utf8Format((scraper(1, "p", soup.find("h2"))))
                productInfo.update({"product_description": product_description})

                # Add category to productInfo
                category = utf8Format((scraper(3, "a", soup.find("ul"))))
                productInfo.update({"category": category})

                # Add image_url to productInfo
                incomplete_image_url = (soup.find("article").find("img")["src"])
                image_url = incomplete_image_url.replace("../..","http://books.toscrape.com")
                productInfo.update({"image_url": image_url})

                # Add universal_product_code to productInfo
                universal_product_code = (scraper(1, "td", soup.find("table").find("tr")))
                productInfo.update({"universal_product_code": universal_product_code})

                # Add price_excluding_tax to productInfo
                price_excluding_tax = utf8Format((scraper(3, "td", soup.find("table").find("tr"))))
                productInfo.update({"price_excluding_tax": price_excluding_tax})

                # Add price_including_tax to productInfo
                price_including_tax = utf8Format((scraper(4, "td", soup.find("table").find("tr"))))
                productInfo.update({"price_including_tax": price_including_tax})

                # Add number_available to productInfo
                number_available = utf8Format((scraper(6, "td", soup.find("table").find("tr"))))
                productInfo.update({"number_available": number_available})

                # Add review_rating to productInfo
                review_rating = utf8Format((scraper(7, "td", soup.find("table").find("tr"))))
                productInfo.update({"review_rating": review_rating})

                writer.writerow({"internal_id": productInfo["internal_id"],
                                 "title": productInfo["title"],
                                 "product_page_url": productInfo["product_page_url"],
                                 "product_description": productInfo["product_description"],
                                 "category": productInfo["category"],
                                 "image_url": productInfo["image_url"],
                                 "universal_product_code": productInfo["universal_product_code"],
                                 "price_excluding_tax": productInfo["price_excluding_tax"],
                                 "price_including_tax": productInfo["price_including_tax"],
                                 "number_available": productInfo["number_available"],
                                 "review_rating": productInfo["review_rating"]
                                 })
    csvfile.close()


#laisser scrap_write pour le moment
# probleme dictionnaire imbriques
#scrap_write(urls_store)


#write_csv(all_product_info)

                   # Saving book picture in image folder

                   #imageRequest = requests.get(image_url, allow_redirects=True)
                   #imageFileName =  universal_product_code + ".jpg"
                   #open(imageFileName, 'wb').write(imageRequest.content)

                   #print("Book n° " + productInfo["internal_id"] + " " + productInfo["title"] + " completed")

# marche impec
def scrap(url_list):
    productCount = 0
    for url in url_list:
        #print(url)
        response = requests.get(url)
        productCount = productCount + 1
        if response.ok:
            productInfo= {}
            soup = BeautifulSoup(response.text, "html.parser")
            # Add internal_id to productInfo
            internal_id = str(url_list.index(url))
            productInfo.update({ "internal_id" : internal_id})


            # Add product_page_url to productInfo
            product_page_url = url
            productInfo.update({"product_page_url" : url})

            # Add title to productInfo
            title = utf8Format(scraper(0, "title", soup.find("h1")))
            productInfo.update({"title": title})

            # Add product_description to productInfo
            product_description = utf8Format((scraper(1, "p", soup.find("h2"))))
            productInfo.update({"product_description": product_description})

            # Add category to productInfo
            category = utf8Format((scraper(3, "a", soup.find("ul"))))
            productInfo.update({"category": category})

            # Add image_url to productInfo
            incomplete_image_url = (soup.find("article").find("img")["src"])
            image_url = incomplete_image_url.replace("../..","http://books.toscrape.com")
            productInfo.update({"image_url": image_url})

            # Add universal_product_code to productInfo
            universal_product_code = (scraper(1, "td", soup.find("table").find("tr")))
            productInfo.update({"universal_product_code": universal_product_code})

            # Add price_excluding_tax to productInfo
            price_excluding_tax = utf8Format((scraper(3, "td", soup.find("table").find("tr"))))
            productInfo.update({"price_excluding_tax": price_excluding_tax})

            # Add price_including_tax to productInfo
            price_including_tax = utf8Format((scraper(4, "td", soup.find("table").find("tr"))))
            productInfo.update({"price_including_tax": price_including_tax})

            # Add number_available to productInfo
            number_available = utf8Format((scraper(6, "td", soup.find("table").find("tr"))))
            productInfo.update({"number_available": number_available})

            # Add review_rating to productInfo
            review_rating = utf8Format((scraper(7, "td", soup.find("table").find("tr"))))
            productInfo.update({"review_rating": review_rating})

            # Store product_info item in all_product_info
            all_product_info[internal_id] = productInfo

    return all_product_info

urls_store =[]
urls_store = generate_all_books_url(all_category_pages)
all_product_info = scrap(urls_store)





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

print("writing process started")
write_csv(all_product_info)

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
        print("Book n° " + all_product_info[index]["internal_id"] + " " + all_product_info[index]["title"] + " completed")

#write_csv(all_product_info)
save_pictures(all_product_info)
