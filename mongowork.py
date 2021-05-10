import json
from pymongo import MongoClient
import pandas as pd

class Mongowork:
    def create_connection(self,database_name):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[database_name]

    def create_coll(self,collection_name,filename,validator):
        self.collection = self.db.create_collection(collection_name,validator=validator)
        with open(filename) as f:
            file_data = json.load(f)
        self.collection.insert_many(file_data)

    def read_collections(self,coll1,coll2):
        self.collection1 = self.db[coll1].find()
        self.collection2 = self.db[coll2].find()

    def transform_in_dataframe_and_concat(self):
        df1 = pd.DataFrame.from_records(self.collection1)
        df2 = pd.DataFrame.from_records(self.collection2)
        self.df_grouped = pd.concat([df1, df2], axis=1, join='inner')
        print(self.df_grouped)

    def close_connection(self):
        self.client.close()

if __name__ == '__main__':
    val1={
  '$jsonSchema': {
    'bsonType': 'object',
    'required': [
      'company_name',
      'source_url'
    ],
    'properties': {
      'company_name': {
        'bsonType': 'string',
        'description': 'must be a string and is required'
      },
      'source_url': {
        'bsonType': 'string',
        'description': 'must be a string and is required'
                }
             }
        }
    }
    val2={
    '$jsonSchema': {
    'bsonType': 'object',
    'required': [
      'company_name','company_location','company_website','company_webdomain','company_industry','company_employee_size','company_revenue','contact_details'
    ],
    'properties': {
      'company_name': {
        'bsonType': 'string',
        'description': 'must be a string and is required'
      },
      'company_location': {
        'bsonType': 'string',
        'description': 'must be a string and is required'
      },
      'company_website': {
        'bsonType': 'string',
        'pattern':'^[a-zA-Z0-9_.-:-]*(com|net|org)$',
        'description': 'must be a string and is required'
      },
      'company_webdomain': {
        'bsonType': 'string',
        'pattern':'^[a-zA-Z0-9_.-:-]*(com|net|org)$',
        'description': 'must be a string and is required'
      },
      'company_industry': {
        'bsonType': 'string',
        'description': 'must be a string and is required'
      },
      'company_employee_size': {
        'bsonType': 'string',
        'pattern':'^[0-9]+(\s* - \s*)[0-9]+$',
        'description': 'must be a string and is required'
      },
      'company_revenue': {
        'bsonType': 'string',
        'pattern':'^$|^[\$][\$ 0-9]+(\s* - \s*)[0-9]+(M)$',
        'description': 'must be a string and is required'
      },
      'contact_details': {
        'bsonType': 'array',
        'items': {
          'bsonType': ['object'],
          'required': ['contact_name', 'contact_email_domain','contact_jobtitle','contact_department']
                    }
                }
            }
        }
    }
    t=Mongowork()
    t.create_connection('LeadBook')
    t.create_coll('company_index', './data/company_index.json',val1)
    t.create_coll('company_profiles', './data/company_profiles.json',val2)
    t.close_connection()
    print("DataBase created...")
