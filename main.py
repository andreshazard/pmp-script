import email
import getpass
import imaplib
import os
import re

try:
    file = open('credentials.txt')
    user = str(file.readline().split()[0])
    pwd = str(file.readline().split()[0])
    pmp_pwd = str(file.readline().split()[0])
except:
    print "It seems that credentials file has not been created"

# connecting to the gmail imap server
m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(user, pwd)
m.select("INBOX")  # mail box where you get the pmp email
resp, items = m.search(None, "SUBJECT", "Second factor password for Password Manager Pro")
items = items[0].split()
if items == []:
    print "Secondary email password has not been find, try again later"

for emailid in items:
    resp, data = m.fetch(emailid, "(RFC822)")  # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
    email_body = data[0][1]  # getting the mail content
    mail = email.message_from_string(email_body)  # parsing the mail content to get a mail object
    m.store(emailid, '+FLAGS', '\\Deleted')
    m.expunge()  # Delete message once we have the content

    # Getting only the password and not the hole message
    for line in email_body.splitlines():
        if "Password Manager Pro is:" in line:
            pmp_secondary_pwd = re.sub('[^0-9]', '', line)  # Get only the numbers of that line
            print "Password = " + pmp_pwd
            print "Secondary Password = " + pmp_secondary_pwd
            break
    break
m.logout()
