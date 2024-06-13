import requests


class NHNCloudSMS:
    def __init__(self, app_key, secret_key, sender_phone_number):
        """
        Initializes the NHNCloudSMS class with app key, secret key, and sender phone number.

        :param app_key: Your NHN Cloud app key.
        :param secret_key: Your NHN Cloud secret key.
        :param sender_phone_number: The phone number that will send the SMS.
        """
        self.api_url = f"https://api-sms.cloud.toast.com/sms/v3.0/appKeys/{app_key}"
        self.app_key = app_key
        self.secret_key = secret_key
        self.sender_phone_number = sender_phone_number

    def send_sms(self, recipient_number, message):
        """
        Sends an SMS to a single recipient.

        :param recipient_number: The phone number of the recipient.
        :param message: The message to be sent.
        :return: The response from the API.
        """
        headers = self._get_headers()
        payload = {
            "body": message,
            "sendNo": self.sender_phone_number,
            "recipientList": [{"recipientNo": recipient_number}],
        }
        response = requests.post(f"{self.api_url}/sender/sms", json=payload, headers=headers)
        return response.json()

    def send_bulk_sms(self, recipient_numbers, message):
        """
        Sends an SMS to multiple recipients.

        :param recipient_numbers: A list of phone numbers of the recipients.
        :param message: The message to be sent.
        :return: The response from the API.
        """
        headers = self._get_headers()
        recipient_list = [{"recipientNo": number} for number in recipient_numbers]
        payload = {
            "body": message,
            "sendNo": self.sender_phone_number,
            "recipientList": recipient_list,
        }
        response = requests.post(f"{self.api_url}/sender/sms", json=payload, headers=headers)
        return response.json()

    def schedule_sms(self, recipient_number, message, schedule_time):
        """
        Schedules an SMS to be sent at a specific time.

        :param recipient_number: The phone number of the recipient.
        :param message: The message to be sent.
        :param schedule_time: The time at which the SMS should be sent.
        :return: The response from the API.
        """
        headers = self._get_headers()
        payload = {
            "body": message,
            "sendNo": self.sender_phone_number,
            "recipientList": [{"recipientNo": recipient_number}],
            "scheduleCode": schedule_time
        }
        response = requests.post(f"{self.api_url}/sender/sms", json=payload, headers=headers)
        return response.json()

    def get_sms_status(self, request_id):
        """
        Retrieves the status of a sent SMS.

        :param request_id: The ID of the SMS request.
        :return: The response from the API.
        """
        headers = self._get_headers()
        response = requests.get(f"{self.api_url}/sender/sms/{request_id}", headers=headers)
        return response.json()

    def get_sent_sms_list(self, start_date, end_date):
        """
        Retrieves a list of sent SMS messages within a specific date range.

        :param start_date: The start date of the range (format: YYYY-MM-DD).
        :param end_date: The end date of the range (format: YYYY-MM-DD).
        :return: The response from the API.
        """
        headers = self._get_headers()
        params = {
            "startCreateDate": start_date,
            "endCreateDate": end_date
        }
        response = requests.get(f"{self.api_url}/sender/sms", headers=headers, params=params)
        return response.json()

    def _get_headers(self):
        """
        Constructs the headers required for the API requests.

        :return: A dictionary of headers.
        """
        return {
            "Content-Type": "application/json;charset=UTF-8",
            "X-Secret-Key": self.secret_key,
        }
