#!/usr/bin/python

import httplib2

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

CLIENT_SECRET_FILE = 'client_secret_<YOUR-UNIQUE-ID-GOES-HERE>.apps.googleusercontent.com.json'
STORAGE = Storage('gmail.storage')

OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'

gmail_labels = ['UNREAD', 'INBOX', 'STARRED', 'SPAM', 'CATEGORY_PERSONAL', 'CATEGORY_SOCIAL', 'CATEGORY_PROMOTIONS', 'CATEGORY_UPDATES', 'CATEGORY_FORUMS']


def build_service():
  flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
  http = httplib2.Http()
  credentials = STORAGE.get()
  if credentials is None or credentials.invalid:
    credentials = run(flow, STORAGE, http=http)
  http = credentials.authorize(http)
  return build('gmail', 'v1', http=http)


# def get_list_of_labels(gmail_service):
#   list_of_labels = gmail_service.users().labels().list(userId='me').execute()
#   labels = list_of_labels['labels']
#   return labels


def main():
  gmail_service = build_service()
  # all_labels = get_list_of_labels(gmail_service)
  # print (json.dumps(all_labels, sort_keys=True, indent=2, separators=(',', ': ')))
  for label in gmail_labels:
    label_info = gmail_service.users().labels().get(userId='me', id=label).execute()
    # print (json.dumps(label_info, sort_keys=True, indent=2, separators=(',', ': ')))
    print label_info['id'] + ' ' + str(label_info['messagesTotal']) + '/' + str(label_info['messagesUnread'])

if __name__ == '__main__':
  main()
