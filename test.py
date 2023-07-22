import openpyxl
from langchain.utilities import GoogleSerperAPIWrapper

import os


def search_product_to_excel(product, file_name):
    
    # Initialize API wrapper
    search = GoogleSerperAPIWrapper()
    
    # Get search results
    results = search.results(product)
    
    # Extract product info
    product_info = {}
    if 'knowledgeGraph' in results:
        knowledge_graph = results['knowledgeGraph']
        product_info['Title'] = knowledge_graph['title']
        product_info['Description'] = knowledge_graph['description']
        product_info['Description Source'] = knowledge_graph['descriptionSource']
        
    # Save to Excel        
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet['A1'] = 'Title'
    sheet['B1'] = 'Description' 
    sheet['C1'] = 'Description Source'
    sheet.append([product_info.get('Title'), 
                  product_info.get('Description'),
                  product_info.get('Description Source')])
    wb.save(file_name)

product = "iPhone 14" 
file_name = "iphone14_info.xlsx"

search_product_to_excel(product, file_name)