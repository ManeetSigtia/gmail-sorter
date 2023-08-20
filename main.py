import re

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.auth.transport.requests import Request

from gmail_auth import get_authenticated_service
from gmail_sorter import SortGmail


def is_valid_email(email):
    # Regular expression pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)


if __name__ == '__main__':
    credentials = get_authenticated_service()

    # Check if the token is expired and refresh if there's a refresh token
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    try:
        gmail_service = build('gmail', 'v1', credentials=credentials)
        user_email = input("Enter the e-mail address for which you want to sort your email: ")

        if not is_valid_email(user_email):
            print("Invalid email address. Please enter a valid email.")
        else:
            query = 'in:inbox category:primary'

            sorter = SortGmail(gmail_service, user_email)
            sorter.populate_name_to_id_map()
            sorter.sort_inbox_efficient(query)

    except HttpError as error:
        print(error)
