import unittest
from nhncloud_email.email import NHNCloudEmail
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class NHNCloudEmailTest(unittest.TestCase):
    def setUp(self):
        self.email_service = NHNCloudEmail(
            app_key=os.getenv('NHN_CLOUD_EMAIL_APP_KEY'),
            secret_key=os.getenv('NHN_CLOUD_EMAIL_SECRET_KEY'),
            sender_email=os.getenv('NHN_CLOUD_EMAIL_SENDER')
        )

    def test_send_email(self):
        response = self.email_service.send_email('sun@runners.im', 'Test Subject', 'Test body')
        print('test_send_email: ', response)
        self.assertEqual(response['header']['resultCode'], 0)
    #
    # def test_send_bulk_email(self):
    #     response = self.email_service.send_bulk_email(['sun@runners.im'], 'Test Subject', 'Test body')
    #     print('test_send_bulk_email: ', response)
    #     self.assertEqual(response['header']['resultCode'], 0)
    #
    # def test_schedule_email(self):
    #     response = self.email_service.schedule_email('sun@runners.im', 'Test Subject', 'Test body', '2024-12-31T23:59:59')
    #     print('test_schedule_email: ', response)
    #     self.assertEqual(response['header']['resultCode'], 0)
    #
    # def test_get_email_status(self):
    #     response = self.email_service.get_email_status('request_id_12345')  # 실제 request_id 사용 필요
    #     print('test_get_email_status: ', response)
    #     self.assertEqual(response['header']['resultCode'], 0)
    #
    # def test_get_sent_email_list(self):
    #     response = self.email_service.get_sent_email_list("2023-01-01", "2023-01-31")
    #     print('test_get_sent_email_list: ', response)
    #     self.assertEqual(response['header']['resultCode'], 0)

if __name__ == '__main__':
    unittest.main()
