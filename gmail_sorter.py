# import re

class SortGmail:
    def __init__(self, service, user_id):
        self.service = service
        self.user_id = user_id

        self.MAX_RESULTS = 50

        self.email_to_label_map = {}

        self.trash_recipients_set = {
            'notifications@discord.com',
            'noreply-maps-timeline@google.com',
            'noreply-travel@google.com',
            'no-reply@revolut.com',
            'no-reply@e.udemymail.com',
            'thestudent@timeshighereducationemail.com',
            'no-reply@accounts.google.com',
            'no-reply@accounts.google.com',
            'no-reply@business.amazon.co.uk',
            'no-reply@comms.trainline.com',
            'no-reply@geeksforgeeks.org',
            'newsletter@qs.com',
            'no-reply@leetcode.com',
            'singapore@seao.crm.samsung.com',
            'stories-features@mail.ft.com',
            'team@hello.remove.bg',
            'team@mail.notion.so',
            'sarah@pdffiller.com',
            'no-reply@news.supercell.com',
            'no-reply@news.trading212.com',
            'no-reply@spotify.com',
            'no-reply@strava.com',
            'no-reply@todoist.com',
            'noreply@mail.chope.co',
            'noreply@qs.com',
            'notifications@calendly.com',
            'notifications@rumble.com',
            'promotions@newsletter.quizlet.com',
            'recommendations@explore.pinterest.com',
            'info@send.grammarly.com',
            'info@websummit.com',
            'qses.iss @ qs.com',
            'events@jovian.email',
            'Education@britishcouncil.org.sg',
            'hello@devfolio.co',
            'edX@news.edx.org',
            'undergraduate.info@hult.edu',
            'system@account.jobtoday.com',
            'codingcompetitions@google.com',
            'news@email-nus.org.uk',
            'summersession@uchicago.edu',
            'no-reply@albert.io',
        }

        self.name_to_id_map = {}

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

    """
    def get_email_ids(self, query):
        response = self.service.users().messages().list(userId=self.user_id, q=query).execute()
        messages = response.get('messages', [])
        return [message['id'] for message in messages]
    
    def trash_email(self, query):
        email_ids = self.get_email_ids(query)

        for email_id in email_ids:
            self.service.users().messages().trash(userId=self.user_id, id=email_id).execute()
    
    def modify_email_labels(self, query, label_name):
        new_label_id = self.get_label_id(label_name)
        old_label_id = self.get_label_id("INBOX")

        if not new_label_id:
            new_label_id = self.create_gmail_label(label_name)

        email_ids = self.get_email_ids(query)

        batch_request = {
            'ids': email_ids,
            'addLabelIds': [new_label_id],
            'removeLabelIds': [old_label_id]
        }

        self.service.users().messages().batchModify(userId=self.user_id, body=batch_request).execute()

    def sort_inbox(self):
        self.populate_name_to_id_map()

        response = self.service.users().messages().list(userId=self.user_id, q='in:inbox category:primary').execute()
        messages = response.get('messages', [])

        for message in messages:
            msg_id = message['id']
            msg = self.service.users().messages().get(userId=self.user_id, id=msg_id).execute()
            headers = msg.get('payload', {}).get('headers', [])
            sender_header = next((header['value'] for header in headers if header['name'] == 'From'), None)
            sender_email_match = re.search(r'<([^>]+)>', sender_header)

            if sender_email_match:
                sender_email = sender_email_match.group(1)
            else:
                continue

            if sender_email in self.trash_recipients_set:
                self.service.users().messages().trash(userId=self.user_id, id=message['id']).execute()
            else:
                new_label_name = sender_email

                if new_label_name in self.name_to_id_map:
                    new_label_id = self.name_to_id_map[new_label_name]
                else:
                    new_label_id = self.create_gmail_label(new_label_name)

                old_label_id = self.get_label_id("INBOX")

                request = {
                    'addLabelIds': [new_label_id],
                    'removeLabelIds': [old_label_id]
                }
                print(request)

                self.service.users().messages().modify(userId=self.user_id, id=message['id'], body=request).execute()
    """
