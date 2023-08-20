from email_utils import read_emails_from_file


class SortGmail:
    def __init__(self, service, user_id):
        self.service = service
        self.user_id = user_id

        self.email_to_label_map = {}
        self.name_to_id_map = {}

        self.MAX_RESULTS = 50

        self.trash_recipients_set = read_emails_from_file('emails_to_send_to_trash.txt')

    # create a new label given the label name
    def create_gmail_label(self, label_name):
        label_object = {'name': label_name}
        created_label = self.service.users().labels().create(userId=self.user_id, body=label_object).execute()
        self.name_to_id_map[label_name] = created_label['id']
        return created_label['id']

    # given the name of an existing label, return its id
    def get_label_id(self, label_name):
        if label_name in self.name_to_id_map:
            return self.name_to_id_map[label_name]

        response = self.service.users().labels().list(userId=self.user_id).execute()
        labels = response.get('labels', [])

        for label in labels:
            if label_name == label['name']:
                return label['id']
        return None

    # sort gmail inbox efficiently
    def sort_inbox_efficient(self, query):
        # the label that would be removed from all new emails
        inbox_label_id = self.get_label_id("INBOX")

        # retrieving unsorted emails from inbox
        response = self.service.users().messages().list(userId=self.user_id,
                                                        q=query,
                                                        maxResults=self.MAX_RESULTS).execute()
        messages = response.get('messages', [])

        while messages:
            # creating a batch for which all api calls will be executed together
            # to increase efficiency
            batch = self.service.new_batch_http_request()

            for message in messages:
                msg_id = message['id']
                msg = self.service.users().messages().get(userId=self.user_id, id=msg_id, format='metadata',
                                                          fields='payload/headers').execute()
                headers = msg.get('payload', {}).get('headers', [])
                sender_header = next((header['value'] for header in headers if header['name'] == 'From'), None)

                # finding the name and email of the sender of the email
                if sender_header:
                    sender_parts = sender_header.rsplit(' ', 1)
                    sender_name = sender_parts[0].strip('""')

                    if len(sender_parts) > 1:
                        sender_email = sender_parts[1].strip('<>')
                    else:
                        sender_email = sender_name.strip('<>')

                else:
                    continue

                # deleting an email
                if sender_email in self.trash_recipients_set:
                    print(f"Email deleted: {sender_email}")
                    batch.add(self.service.users().messages().trash(userId=self.user_id, id=msg_id))

                # sorting the email
                else:
                    new_label_name = sender_name.upper()

                    if new_label_name in self.name_to_id_map:
                        new_label_id = self.name_to_id_map[new_label_name]
                    else:
                        new_label_id = self.create_gmail_label(new_label_name)

                    request = {
                        'addLabelIds': [new_label_id],
                        'removeLabelIds': [inbox_label_id, 'UNREAD']
                    }

                    batch.add(self.service.users().messages().modify(userId=self.user_id, id=msg_id, body=request))
                    print(f"Sorted into label: {new_label_name}")

                # determining the date the email was sent
                email_date = next((header['value'] for header in headers if header['name'] == 'Date'), None)
                print(email_date)

            batch.execute()

            # fetch next page of messages
            response = self.service.users().messages().list(userId=self.user_id,
                                                            q=query,
                                                            maxResults=self.MAX_RESULTS,
                                                            pageToken=response.get('nextPageToken')).execute()
            messages = response.get('messages', [])

    # creating a dictionary that stores all label names
    # and their corresponding ids as key value pairs
    def populate_name_to_id_map(self):
        response = self.service.users().labels().list(userId=self.user_id).execute()
        labels = response.get('labels', [])

        for label in labels:
            self.name_to_id_map[label['name']] = label['id']
