### Description

This code defines a class `mongo_operation` that provides methods for interacting with a MongoDB database. The class allows you to create a MongoDB client, create collections, and insert data in bulk. It supports both single records and lists of records, as well as CSV and Excel file formats.

### How to Use

To use this class as a package on PyPI, you can follow these steps:

1. **Install the Package**:
   ```bash
   pip install pymongo-connector
   ```

2. **Import the Class**:
   ```python
   from pymongo_connector import mongo_crud
   ```

3. **Create an Instance of the Class**:
   ```python
   mongo = mongo_crud.mongo_operation(client_url='mongodb://localhost:27017/', database_name='mydatabase', collection_name='mycollection')
   ```

4. **Use the Methods**:
   ```python
   # Insert a single record
   mongo.insert_record({'name': 'John', 'age': 30})

   # Insert multiple records
   records = [{'name': 'Jane', 'age': 25}, {'name': 'Bob', 'age': 40}]
   mongo.insert_record(records)

   # Bulk insert data from a CSV file
   mongo.bulk_insert('data.csv')

   # Bulk insert data from an Excel file
   mongo.bulk_insert('data.xlsx')
   ```