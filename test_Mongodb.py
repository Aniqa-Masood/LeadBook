import unittest
from mongowork import Mongowork

class test_Mongodb(unittest.TestCase):

    def test_mongo(self):
        #build connection
        Mongowork.create_connection(self,'LeadBook')

        #Read collections from existing database
        Mongowork.read_collections(self, 'company_index', 'company_profiles')

        #Transform collections into dataframe and concat it
        Mongowork.transform_in_dataframe_and_concat(self)

        #Close connection
        Mongowork.close_connection(self)

if __name__ == '__main__':
    unittest.main()
