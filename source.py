import pymongo
from pymongo import MongoClient
import pandas as pd
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage
import re

##Changes to be made to the csv
# csv_file_path = 'C:/Users/cmbha/OneDrive/Desktop/AIQoD/sample_data.csv'
# df = pd.read_csv(csv_file_path)
# df['in_stock'] = df['Stock']>0
# df['Discount'] = df['Discount'].str.rstrip('%').astype('int')

## Load data to mongodb
connection_string = "mongodb+srv://cmbhatt99:HalaMadrid$14@cluster0.oq0eti9.mongodb.net/"
client = MongoClient(connection_string)
db = client['product_database']
collection = db['products']
# data = df.to_dict('records')
# collection.insert_many(data)
# print("Data inserted successfully!")



## Generate MongoDB query
llm = ChatOllama(
    model="llama3.1",
    temperature=0
)

messages = [
    (
        "system",
        "You are an expert in generating mongodb queries for python given a statement in natural language."
        "Respond ONLY with the Python code for the MongoDB query which must always be a string, without any explanation or additional text."
        "Ensure that logical operators are enclosed in quotations"
        "The name of the database is 'products_database' and the collection is 'products'. Following is the name of columns followed by the data type."
        "{'Brand': ['str'], 'Category': ['str'], 'Discount': ['int'], 'in_stock': ['bool'], LaunchDate': ['str'], 'Price': ['float'], 'ProductID': ['int'], 'ProductName': ['str'], 'Rating': ['float'], 'ReviewCount': ['int'], 'Stock': ['int'], '_id': ['ObjectId']}"
    ),
    ("human", "Find all products with a rating below 4.5 that have more than 200 reviews and are offered by the brand 'Nike' or 'Sony'."),
]
ai_msg = llm.invoke(messages)
content = ai_msg.content
    
start_index = content.index('{')
end_index = content.rindex('}') + 1
extracted_query = content[start_index:end_index]

if '$and' in extracted_query:
    print('yes')