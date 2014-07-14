adminUser = 'isthisanadminaccount'
adminPassword = 'thisisaweakpassword'

#for function debugging
#email = 'testaccount@eips.ca'
#firstname = 'Test'
#lastname = 'Account'
#userPassword = 'theirpassword'

import csv
#import gdata.apps.service

file = open('powerschoolexport.csv', 'rb')
reader = csv.reader(file)
rownumber = 0

for row in reader:
    #print row
    email = row[0]
    firstname = row[1]
    lastname = row[2]
    userPassword = row[3]
    if rownumber > 0:
        parseUser(email, firstname, lastname, userPassword)
    rownumber += 1

def parseUser(email, firstname, lastname, userPassword):
    print email

#def createUser(email, firstname, lastname, userPassword):
  #get the username and domain from the email string
#  domainIndex = email.find('@')
#  username = email[:domainIndex-1]
#  domain = email[domainIndex+1:]
#  service = gdata.apps.service.AppsService(email=adminUser+'@'+domain, domain=domain, password=adminPassword)
#  service.ProgrammaticLogin()
#  service.CreateUser(username, lastname, firstname, userPassword)
 #append to some sort of log that we created a user (or if there was an error)
