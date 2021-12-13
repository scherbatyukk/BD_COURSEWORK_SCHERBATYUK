from selectorlib import Extractor
import requests
import random
import re
from datetime import datetime
from models.category import Category
from models.product import Product
from db import session
from models.links import links_products_categories


e = Extractor.from_yaml_file('./scrapping/search_results.yml')

def scrape(url):  

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    if r.status_code >= 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            raise Exception("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            raise Exception("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
    return e.extract(r.text)

def getProductsByCategory():
    category = input('Enter category for scrapping: ')
    data = scrape(f'https://www.amazon.com/s?k={category}')
    if not data['products']:
        raise Exception('Null')

    products_count = 0
    categories_count = 0
    links_count = 0
    for raw in data['products']:
        print(f"Get product from {raw['url']}")
        if raw['price'] != None: price = int(float(re.findall("\d+\.\d+", raw['price'])[0]))
        else: price = random.randint(200, 5000)

        new_product = Product(raw['title'],
                              '',
                              '',
                              datetime.today().strftime('%Y-%m-%d'),
                              price)
        session.add(new_product)
        session.commit()
        products_count += 1
        session.refresh(new_product)

        # Adding categories to database:

        checked_categories = session.query(Category).filter(Category.name == category).all()
        if len(checked_categories) == 0:
            new_category = Category(category, category)
            session.add(new_category)
            session.commit()
            categories_count += 1
            session.refresh(new_category)

            # Adding link:
            ins = links_products_categories.insert().values(product_id=new_product.id,
                                                            category_id=new_category.id)
            session.execute(ins)
        else:
            ins = links_products_categories.insert().values(product_id=new_product.id,
                                                            category_id=checked_categories[0].id)
            session.execute(ins)
        links_count += 1
    session.commit()
    print(f'\nAdded {products_count} products, {categories_count} categories and {links_count} links.')
    input('\nPress any key to continue...')
