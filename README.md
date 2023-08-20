# Gmail Sorter Project
Welcome to the Gmail Sorter project! This tool helps you organize your Gmail inbox efficiently.

## Table of Contents
- [Introduction](#introduction)
- [Technologies Used](#technologies-used)
- [Project Set-up](#project-set-up)
  - [Clone Repository](#1-clone-the-repository)
  - [Necessary environments and dependencies](#2-set-up-the-necessary-environment-and-dependencies)
  - [Account Authentication](#3-authenticate-your-gmail-account)
  - [Configure Project](#4-configure-the-project-settings)
  - [Run Project](#5-run-the-project-to-sort-and-manage-your-gmail-inbox)
- [Project Status](#project-status)
- [Contributing](#contributing)
- [Contact](#contact)

## Introduction

Optimize your Gmail inbox management with the Gmail Sorter – a versatile tool designed to simplify your email organization process. Automatically create labels for emails, group them based on sender names, mark them as read, and enjoy a clutter-free inbox experience.

### Key Features
- Automated Label Creation: The Gmail Sorter intelligently generates labels from sender names extracted from email addresses. Emails from the same sender are grouped under a single label for seamless organization.

- Effortless Inbox Organization: Let the Gmail Sorter handle the heavy lifting of categorizing emails. With automated labeling, your inbox stays organized and clutter-free.

- Streamlined Labeling: Say goodbye to manual label assignments. The Gmail Sorter automatically adds labels, so you can focus on what matters most – your email content.

- Efficient Email Management: Sort, label, and manage emails effortlessly. The Gmail Sorter moves emails to the trash, marks them as read, and streamlines your inbox management.

## Technologies Used

### Languages
Python - version 3.10.8

### Libraries

#### os.path 
The application utilizes the os.path module to effectively handle file and directory paths, ensuring smooth interaction with the file system.

#### google.auth.transport.requests.Request
The Request module from the google.auth.transport.requests package enables the application to establish authenticated HTTP requests, facilitating secure communication with various Google services.

#### google.oauth2.credentials.Credentials
The Credentials module from the google.oauth2.credentials package handles the management of OAuth2 credentials, a pivotal component for ensuring secure authentication with Google APIs.

#### google_auth_oauthlib.flow.InstalledAppFlow
Leveraging this module from the google_auth_oauthlib.flow package, the application implements the OAuth 2.0 authorization flow tailored for desktop applications. This enhances security by enabling seamless and safe user authentication.

#### re 
The re module plays a crucial role in the application by providing powerful pattern matching and manipulation capabilities. It enables the extraction and processing of specific email information using regular expressions.

#### googleapiclient.discovery.build
By utilizing the build module from the googleapiclient.discovery package, the application constructs service objects that facilitate streamlined interactions with the Gmail API. These interactions include querying, labeling, and managing emails.

#### googleapiclient.errors.HttpError
The HttpError module from the googleapiclient.errors package enhances the robustness of the application by offering essential error handling mechanisms. This ensures graceful handling of HTTP requests made to Google APIs.

These carefully selected technologies and modules collectively empower the Gmail Sorter application to seamlessly interact with the Gmail API. They offer a user-friendly interface and effective email management capabilities, enhancing the overall user experience

## Project Set-Up

Follow these steps to set up and use the Gmail Sorter project:

### 1. Clone the repository

Clone the project repository to your local machine using the following command:

```
git clone https://github.com/ManeetSigtia/gmail-sorter.git
```

### 2. Set up the necessary environment and dependencies.
    
#### 1. Navigate to the project directory and create a virtual environment:

```
cd gmail-sorter
python3 -m venv venv
```

#### 2. Activate the virtual environment:
On macOS and Linux:
```
source venv/bin/activate
```

On Windows:
```
venv\Scripts\activate
```

#### 3. Install the required dependencies from the requirements.txt file:

```
pip install -r requirements.txt
```

If you encounter issues while installing modules, manually install the required modules:
```
pip install google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2
```

### 3. Authenticate Your Gmail Account
To access your Gmail account through the API, you need to set up credentials. Here's how you can do it:

#### 1. Go to the Google Cloud Console:
Navigate to the [Google Cloud Console](https://console.cloud.google.com/)
and sign in with your Google account.

#### 2. Create a New Project and Enable the Gmail API:
- Click on the project drop-down at the top of the page, then click "New Project."
- Enter a name for your project and click "Create."
- In the left sidebar, click on "APIs & Services" > "Library."
- Search for "Gmail API" and click on it.
- Click the "Enable" button to enable the Gmail API for your project.

#### 3. Create Credentials for a "Desktop App":
- In the left sidebar, click on "APIs & Services" > "Credentials."
- Click the "Create Credentials" button and select "OAuth client ID."
- Select "Desktop app" as the application type.
- Give your OAuth client a name (e.g., "Gmail Sorter Desktop App").
- Click the "Create" button.

#### 4. Download the JSON File containing your Credentials:
- Find the newly created OAuth client ID in the list of OAuth 2.0 Client IDs.
- Click the download icon (downward arrow) next to your client ID. This will download a JSON file containing your credentials.
- Save this JSON file to a safe location on your computer.

#### 5. Rename and Place the JSON File:
- Rename the downloaded JSON file to `credentials.json`.
- Move the `credentials.json` file into the `myproject` directory.

Now you have the credentials required to authenticate your Gmail account and access it through the Gmail API. This step allows the Gmail Sorter script to access your Gmail inbox for sorting.
Remember, these credentials are sensitive and should be kept secure. Do not share them or commit them to public repositories.` and place it in the directory called 'myproject'.

### 4. Configure the project settings
If you want to delete all emails from a particular sender, follow these steps:

1. Open the `emails_to_send_to_trash.txt` file in the project directory.
2. Type the email address of the sender you want to target. There's no need to enclose the email address in quotes.
3. Save the file.

After completing these steps, all emails from the specified sender will be automatically moved to the trash from your primary inbox when the program is executed.

Please note that this action is irreversible. Make sure to review the email addresses before adding them to the list.

### 5. Run the project to sort and manage your Gmail inbox.
- Change your directory to myprogram from the root directory:
```
cd myprogram
```

- Run the main script to start sorting your Gmail inbox:
```
python main.py
```
The script will execute and begin sorting your inbox.

## Project Status

Project is: _complete_

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please feel free to open an issue or submit a pull request.

## Contact

My email address is sigtiamaneet@gmail.com - feel free to contact me!
