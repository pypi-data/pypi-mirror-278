import unittest
from nhncloud_sms.sms import NHNCloudSMS
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class NHNCloudSMSTest(unittest.TestCase):
    def setUp(self):
        self.sms_service = NHNCloudSMS(
            app_key=os.getenv('NHN_CLOUD_APP_KEY'),
            secret_key=os.getenv('NHN_CLOUD_SECRET_KEY'),
            sender_phone_number=os.getenv('NHN_CLOUD_SENDER_PHONE_NUMBER')
        )

    def test_send_sms(self):
        response = self.sms_service.send_sms("01040840660", "Hello, this is a test message.")
        print('test_send_sms: ', response)
        self.assertEqual(response['header']['isSuccessful'], True)
    #
    # def test_send_bulk_sms(self):
    #     recipient_numbers = ["01040840660"]
    #     response = self.sms_service.send_bulk_sms(recipient_numbers, "Hello, this is a test bulk message.")
    #     print('test_send_bulk_sms: ', response)
    #     self.assertEqual(response['header']['isSuccessful'], True)
    #
    # def test_schedule_sms(self):
    #     response = self.sms_service.schedule_sms("01040840660", "Hello, this is a scheduled message.",
    #                                              "2024-12-31T23:59:59")
    #     print('test_schedule_sms: ', response)
    #     self.assertEqual(response['header']['isSuccessful'], True)
    #
    # def test_get_sms_status(self):
    #     response = self.sms_service.get_sms_status("request_id_12345")  # 적절한 request_id를 사용하세요
    #     print('test_get_sms_status: ', response)
    #     self.assertEqual(response['header']['isSuccessful'], True)
    #
    #
