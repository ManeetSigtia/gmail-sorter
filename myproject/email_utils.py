def read_emails_from_file(filename):
    email_set = set()
    with open(filename, 'r') as file:
        for line in file:
            email = line.strip()  # Remove newline characters and whitespace
            email_set.add(email)
    return email_set
