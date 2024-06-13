import requests
import base64

class NHNCloudEmail:
    def __init__(self, app_key, secret_key, sender_email):
        """
        Initializes the NHNCloudEmail class with the provided app key, secret key, and sender email address.

        :param app_key: Your NHN Cloud app key.
        :param secret_key: Your NHN Cloud secret key.
        :param sender_email: The email address that will send the emails.
        """
        self.api_url = f"https://api-mail.cloud.toast.com/email/v2.1/appKeys/{app_key}"
        self.app_key = app_key
        self.secret_key = secret_key
        self.sender_email = sender_email

    def send_email(self, recipient_email, subject, body, attachments=None):
        """
        Sends an email to a single recipient.

        :param recipient_email: The email address of the recipient.
        :param subject: The subject of the email.
        :param body: The body of the email.
        :param attachments: A list of file paths to attach to the email (optional).
        :return: The response from the API.
        """
        headers = self._get_headers()
        payload = {
            "senderAddress": self.sender_email,
            "title": subject,
            "body": body,
            "receiverList": [{"receiveMailAddr": recipient_email, "receiveType": "MRT0"}],
        }
        if attachments:
            payload["attachments"] = self._prepare_attachments(attachments)

        response = requests.post(f"{self.api_url}/sender/mail", json=payload, headers=headers)
        return self._handle_response(response)

    def send_bulk_email(self, recipient_emails, subject, body, attachments=None):
        """
        Sends an email to multiple recipients.

        :param recipient_emails: A list of email addresses of the recipients.
        :param subject: The subject of the email.
        :param body: The body of the email.
        :param attachments: A list of file paths to attach to the email (optional).
        :return: The response from the API.
        """
        headers = self._get_headers()
        receivers = [{"receiveMailAddr": email, "receiveType": "MRT0"} for email in recipient_emails]
        payload = {
            "senderAddress": self.sender_email,
            "title": subject,
            "body": body,
            "receiverList": receivers,
        }
        if attachments:
            payload["attachments"] = self._prepare_attachments(attachments)
        response = requests.post(f"{self.api_url}/sender/mail", json=payload, headers=headers)
        return self._handle_response(response)

    def schedule_email(self, recipient_email, subject, body, schedule_time, attachments=None):
        """
        Schedules an email to be sent at a specific time.

        :param recipient_email: The email address of the recipient.
        :param subject: The subject of the email.
        :param body: The body of the email.
        :param schedule_time: The time at which the email should be sent.
        :param attachments: A list of file paths to attach to the email (optional).
        :return: The response from the API.
        """
        headers = self._get_headers()
        payload = {
            "senderAddress": self.sender_email,
            "title": subject,
            "body": body,
            "receiverList": [{"receiveMailAddr": recipient_email, "receiveType": "MRT0"}],
            "sendTime": schedule_time,
        }
        if attachments:
            payload["attachments"] = self._prepare_attachments(attachments)
        response = requests.post(f"{self.api_url}/sender/eachMail", json=payload, headers=headers)
        return self._handle_response(response)

    def get_email_status(self, request_id):
        """
        Retrieves the status of a sent email.

        :param request_id: The ID of the email request.
        :return: The response from the API.
        """
        headers = self._get_headers()
        response = requests.get(f"{self.api_url}/sender/mail/{request_id}", headers=headers)
        return self._handle_response(response)

    def get_sent_email_list(self, start_date, end_date):
        """
        Retrieves a list of sent emails within a specific date range.

        :param start_date: The start date of the range (format: YYYY-MM-DD).
        :param end_date: The end date of the range (format: YYYY-MM-DD).
        :return: The response from the API.
        """
        headers = self._get_headers()
        params = {
            "startSendDate": start_date,
            "endSendDate": end_date
        }
        response = requests.get(f"{self.api_url}/sender/mails", headers=headers, params=params)
        return self._handle_response(response)

    def _get_headers(self):
        """
        Constructs the headers required for the API requests.

        :return: A dictionary of headers.
        """
        return {
            "Content-Type": "application/json;charset=UTF-8",
            "X-Secret-Key": self.secret_key,
        }

    def _handle_response(self, response):
        """
        Handles the API response.

        :param response: The response from the API.
        :return: The JSON response if the status code is 200, otherwise an error dictionary.
        """
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "status_code": response.status_code,
                "error": response.text
            }

    def _prepare_attachments(self, attachments):
        """
        Prepares the attachments for the email by encoding them in base64.

        :param attachments: A list of file paths to attach to the email.
        :return: A list of dictionaries containing the file name and base64 encoded file content.
        """
        prepared_attachments = []
        for attachment in attachments:
            with open(attachment, "rb") as file:
                encoded_file = base64.b64encode(file.read()).decode('utf-8')
                prepared_attachments.append({
                    "fileName": attachment.split("/")[-1],
                    "fileBody": encoded_file,
                })
        return prepared_attachments
