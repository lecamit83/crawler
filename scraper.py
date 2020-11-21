import bs4
import pandas
import requests
import json
import re

url = 'https://www.zunecustom.com'

def get_page_content(url):
   page = requests.get(url,headers={"Accept-Language":"en-US"})
   return bs4.BeautifulSoup(page.text,"html.parser")



def get_prod_info(product_link_pull_path):
    print(product_link_pull_path)
    product_soup = get_page_content(product_link_pull_path)
    # body_scripts = product_soup.select('body script')

    script = product_soup.find('script', text=re.compile('window\.__INITIAL_STATE__=', re.I|re.M))
    json_text = script.contents[0]
    json_text = re.search('__INITIAL_STATE__=({.*});', json_text, re.I|re.M)

    if json_text:
        json_text = json_text.group(1)
    data = json.loads(json_text)

    config_product_children_data = []
    if data:
        config_product_children_data = data['customProduct']['product']['configurable_children']

    product_prices = [config_product_item['price'] for config_product_item in config_product_children_data]




    title = product_soup.find('h1', class_="product__name").text

    product__images = product_soup.find_all('div', class_="product-slide-image")
    product__options = product_soup.find_all('button', class_="product__option")

    title = title.strip()
    product_images = [product__image.get('data-key') for product__image in product__images]
    product_sizes = [product__option.text.strip() for product__option in product__options]
    length = len(product_sizes)

    print(title)
    print(product_images)

    for i in range(length):
        print(product_prices[i], product_sizes[i])


soup = get_page_content(url)

product_container = soup.find('ul', class_="site-nav"); 

product_navs = product_container.find_all('a', class_="site-nav__link flex items-center")

link_navs = [product_nav.get('href') for product_nav in product_navs]


title_navs = [product_nav.text for product_nav in product_navs]

product_links = []

for link_nav in link_navs:
    current_nav_link = url + link_nav
    collection_soup = get_page_content(current_nav_link)
    products = collection_soup.find_all('a', class_=":hover-no-underline")
    for product in products:
        if product.get('href') != "https://www.zunecustom.com/admin/products/add":
            product_links.append(product.get('href'))
    

for i in range(len(product_links)):
    get_prod_info(url + product_links[i])