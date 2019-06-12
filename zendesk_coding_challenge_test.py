import unittest
import pandas
from zendesk_coding_challenge import get_credentials
from zendesk_coding_challenge import get_from_api
from zendesk_coding_challenge import parse_json
from zendesk_coding_challenge import display_tickets
from zendesk_coding_challenge import display_single_ticket

print("The credentials for this test is provided separately for security reasons")
print("Please contact the repository maintainer to obtain a copy for testing")
print("This makes API calls, testing this too often may result in being temporarily blocked!")

class TestStringMethods(unittest.TestCase):
    def test_get_credentials(self):
        # positive case is not tested as credentials should remain private
        # therefore credential string will not be included in this file
        # only the base64 version is included (this function converts from ascii to b64)
        #self.assertEqual(get_credentials('credentials.txt'), my_credentials)

        # test that credential string is formatted as user:password
        # note that this assumes that username is an email address!
        self.assertIn('@', get_credentials('test_data/credentials.txt').split(':')[0])

        # test that credential string should not be empty
        self.assertNotEqual(get_credentials('test_data/credentials.txt'), '')

    def test_get_from_api(self):
        url = 'https://henrychin.zendesk.com/api/v2/tickets.json'
        user = 'henry.chinpc@gmail.com'

        # this password is already base64 encrypted so the original password is hidden
        user_password = 'aGVucnkuY2hpbnBjQGdtYWlsLmNvbTohYnc1ZDJLWg=='

        # read in the contents of a working http session to test
        with open('test_data/session.txt', mode='r') as infile:
             session_text = infile.readlines()[0]

        # http sessions should be identical no matter how we access it
        self.assertEqual(get_from_api(url, user=None, token=None, password=None, user_password=user_password, b64=True).text, session_text)

        # but these cases requiring password are not tested as credentials should remain private
        # example use cases for these tests however are listed below
        # should the credentials be available, substitute $my_password with credentials
        #my_user=henry.chinpc@gmail.com
        #my_password='foo bar'
        #self.assertEqual(get_from_api(url, user=my_user, token=None, password=my_password, user_password=None, b64=False).text, session_text)
        #self.assertEqual(get_from_api(url, user=None, token=None, password=None, user_password=my_user_password, b64=False).text, session_text)

        # method for obtaining http session should break if incorrect credentials are provided
        self.assertEqual(get_from_api(url, user=None, token=None, password=None, user_password='foo bar', b64=True).text, '{\"error\":\"Couldn\'t authenticate you\"}')
        self.assertNotEqual(get_from_api(url, user=None, token=None, password=None, user_password='foo bar', b64=True).text, session_text)

        # test for incorrect url provided
        self.assertEqual(get_from_api('http://foo.com/bar.json', user=None, token=None, password=None, user_password=user_password, b64=True).text, 'not found')
        self.assertNotEqual(get_from_api('http://foo.com/bar.json', user=None, token=None, password=None, user_password=user_password, b64=True).text, session_text)

    def test_parse_json(self):
        # transform the json data to tsv separately, then read in the contents to test
        url = 'https://henrychin.zendesk.com/api/v2/tickets.json'
        user_password = 'aGVucnkuY2hpbnBjQGdtYWlsLmNvbTohYnc1ZDJLWg=='
        session = get_from_api(url, user=None, token=None, password=None, user_password=user_password, b64=True)

        tsv_data_pass = pandas.read_csv("test_data/tickets_pass.tsv", sep="\t", index_col=0)
        tsv_data_fail = pandas.read_csv("test_data/tickets_fail.tsv", sep="\t", index_col=0)

        # test that json parsing works
        # we wont test the full dataframe for size constraints
        # but if we choose to do so we can use this to compare dataframes
        # from pandas.util.testing import assert_frame_equal
        self.assertEqual(parse_json(session).columns.all(), tsv_data_pass.columns.all())
        self.assertEqual(parse_json(session).shape, tsv_data_pass.shape)

        # test for cases where json parsing doesnt work (make misformatted table)
        self.assertNotEqual(parse_json(session).columns.all(), tsv_data_fail.columns.all())
        self.assertNotEqual(parse_json(session).shape, tsv_data_fail.shape)

    def test_display_tickets(self):
        url = 'https://henrychin.zendesk.com/api/v2/tickets.json'
        user_password = 'aGVucnkuY2hpbnBjQGdtYWlsLmNvbTohYnc1ZDJLWg=='
        chunk_size = 25

        session = get_from_api(url, user=None, token=None, password=None, user_password=user_password, b64=True)
        data = parse_json(session)

        # check that pager iterates and exits correctly
        self.assertEqual(display_tickets(data, 25), (100, 100, 125))
        self.assertEqual(display_tickets(data, 24), (100, 96, 120))

        self.assertNotEqual(display_tickets(data, 25), (1, 2, 3))


if __name__ == '__main__':
    unittest.main()
