import csv
import random
from db import session

from models.category import Category
from models.product import Product
from models.links import links_products_categories

def parseCsv(path: str, keys: [], filterKey):
    with open(path, 'r', encoding='Latin1') as csv_data:
        reader = csv.DictReader(csv_data)

        entities = []
        prev_product = ''
        for row in reader:
            if prev_product != row[filterKey]:
                entities.append(row)
                if len(entities) % 100 == 0:
                    print(f'Detected {str(len(entities))} new Entities with filter key [{filterKey}]')

            prev_product = row[filterKey]
        print(f'Detected {str(len(entities))} new Entities with filter key [{filterKey}]')

        filteredEntities = []
        for entity in entities:
            item = {}
            for key in keys:
                item[key] = entity[key]
            filteredEntities.append(item)

        return filteredEntities

def parse1():
    data_dict = parseCsv('../data/csv/DatafinitiElectronicsProductData.csv',
                         ['name', 'brand', 'categories', 'dateAdded', 'manufacturer', 'primaryCategories'],
                         'name')

    # Adding Products to database:
    products_count = 0
    categories_count = 0
    links_count = 0
    for row in data_dict:
        new_product = Product(row['name'],
                              row['brand'],
                              row['manufacturer'],
                              row['dateAdded'],
                              random.randint(200, 5000))
        session.add(new_product)
        session.commit()
        products_count += 1
        session.refresh(new_product)

        # Adding categories to database:
        category_names = row['categories'].split(',')

        for category_name in category_names:
            checked_categories = session.query(Category).filter(Category.name == category_name).all()
            if len(checked_categories) == 0:
                new_category = Category(category_name, row['primaryCategories'])
                session.add(new_category)
                session.commit()
                categories_count += 1
                session.refresh(new_category)

                #Adding link:
                ins = links_products_categories.insert().values(product_id=new_product.id,
                                                                category_id=new_category.id)
                session.execute(ins)
            else:
                ins = links_products_categories.insert().values(product_id=new_product.id,
                                                                category_id=checked_categories[0].id)
                session.execute(ins)
            links_count += 1
        session.commit()

    print(f'Added {products_count} products, {categories_count} categories and {links_count} links.')
    input('\nPress any key to continue...')

def parse2():
    data_dict = parseCsv('../data/csv/DatafinitiElectronicsProductsPricingData.csv',
                         ['name', 'brand', 'categories', 'dateAdded', 'manufacturer', 'primaryCategories', 'prices.amountMin'],
                         'name')
    # Adding Products to database:
    products_count = 0
    categories_count = 0
    links_count = 0
    for row in data_dict:
        new_product = Product(row['name'],
                              row['brand'],
                              row['manufacturer'],
                              row['dateAdded'],
                              int(float(row['prices.amountMin'])))
        session.add(new_product)
        session.commit()
        products_count += 1
        session.refresh(new_product)

        # Adding categories to database:
        category_names = row['categories'].split(',')

        for category_name in category_names:
            checked_categories = session.query(Category).filter(Category.name == category_name).all()
            if len(checked_categories) == 0:
                new_category = Category(category_name, row['primaryCategories'])
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

    print(
        f'Added {products_count} products, {categories_count} categories and {links_count} links.')
    input('\nPress any key to continue...')