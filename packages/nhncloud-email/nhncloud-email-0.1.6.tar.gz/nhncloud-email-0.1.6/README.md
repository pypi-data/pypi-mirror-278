# NHNCloudEmail

This is a Python library for interacting with the NHN Cloud Email service.

**Current version: 0.1.6**

## Installation

To use this library, you need to have Python installed. You can install the required dependencies using pip:

```bash
pip install nhncloudemail
```

## Usage

### Initialization
First, you need to initialize the NHNCloudEmail class with your NHN Cloud app key, secret key, and sender email address.

```python
from nhncloud_email import NHNCloudEmail

email_service = NHNCloudEmail(
    app_key='your_app_key',
    secret_key='your_secret_key',
    sender_email='your_sender_email'
)
```

### Sending Email
To send a single email, use the send_email method:

```python
response = email_service.send_email('recipient_email', 'Your Subject', 'Your message body')
print(response)
```

### Sending Bulk Email
To send bulk emails, use the send_bulk_email method:

```python
recipient_emails = ['recipient1_email', 'recipient2_email']
response = email_service.send_bulk_email(recipient_emails, 'Your Subject', 'Your bulk message body')
print(response)
```

### Scheduling Email
To schedule an email, use the schedule_email method:

```python
response = email_service.schedule_email('recipient_email', 'Your Subject', 'Your scheduled message body', 'schedule_time')
print(response)
```

### Getting Email Status
To get the status of a sent email, use the get_email_status method:

```python
response = email_service.get_email_status('request_id')
print(response)
```

### Getting Sent Email List
To get a list of sent emails within a specific date range, use the get_sent_email_list method:

```python
response = email_service.get_sent_email_list('start_date', 'end_date')
print(response)
```

Make sure to replace placeholders (like `'your_app_key'`, `'your_secret_key'`, etc.) with actual values before using the library.

## Contact
Please contact dev@runners.im