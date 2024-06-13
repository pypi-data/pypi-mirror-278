# NHNCloudSMS

This is a Python library for interacting with the NHN Cloud SMS service.

**Current version: 0.1.5**

## Installation

To use this library, you need to have Python installed. You can install the required dependencies using pip:

```bash
pip install nhncloud-sms
```

## Usage

### Initialization
First, you need to initialize the NHNCloudSMS class with your NHN Cloud app key, secret key, and sender phone number.

```python
from nhncloud_sms import NHNCloudSMS

sms_service = NHNCloudSMS(
    app_key='your_app_key',
    secret_key='your_secret_key',
    sender_phone_number='your_sender_phone_number'
)
```

### Sending SMS
To send a single SMS, use the send_sms method:

```python
response = sms_service.send_sms('recipient_phone_number', 'Your message here')
print(response)
```

### Sending Bulk SMS
To send bulk SMS, use the send_bulk_sms method:

```python
recipient_numbers = ['recipient1_phone_number', 'recipient2_phone_number']
response = sms_service.send_bulk_sms(recipient_numbers, 'Your bulk message here')
print(response)
```

### Scheduling SMS
To schedule an SMS, use the schedule_sms method:
```python
response = sms_service.schedule_sms('recipient_phone_number', 'Your scheduled message here', 'schedule_time')
print(response)
```

### Getting SMS Status
To get the status of a sent SMS, use the get_sms_status method:

```python
response = sms_service.get_sms_status('request_id')
print(response)
```

### Getting Sent SMS List
To get a list of sent SMS messages within a specific date range, use the get_sent_sms_list method:

```python
response = sms_service.get_sent_sms_list('start_date', 'end_date')
print(response)
```

Make sure to replace placeholders (like `'your_app_key'`, `'your_secret_key'`, etc.) with actual values before using the library.

## Contact
Please contact dev@runners.im