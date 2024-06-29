import unittest
from client import send_query_to_server

class TestStringSearchClient(unittest.TestCase):
    def test_send_query_existing_string(self):
        query = '3;0;1;28;0;7;5;0;'
        response = send_query_to_server('localhost', 44445, query='3;0;1;28;0;7;5;0;')
        print(f"Query: {query} | Server response: {response}")
        self.assertEqual(response, 'STRING EXISTS')

    def test_send_query_not_found_string(self):
        query = 'banana'
        response = send_query_to_server('localhost', 44445, query='potato')
        print(f"Query: {query} | Server response: {response}")
        self.assertEqual(response, 'STRING NOT FOUND')

if __name__ == '__main__':
    unittest.main()
