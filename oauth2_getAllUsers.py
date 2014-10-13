#import some things we need
import httplib2
from oauth2client.client import SignedJwtAssertionCredentials #included with the Google Apps Directory API
from apiclient.discovery import build
import csv

def downloadUsers(domain, account, customerId):
    superAdmin = 'is@' + domain
    serviceAccount = account + '@developer.gserviceaccount.com'
    p12File = domain + '.p12'
    scope = 'https://www.googleapis.com/auth/admin.directory.user https://www.googleapis.com/auth/admin.directory.orgunit https://www.googleapis.com/auth/admin.directory.group https://www.googleapis.com/auth/admin.directory.device.chromeos'
    
    #read then close the key file
    keyFile = file(p12File, 'rb')
    key = keyFile.read()
    keyFile.close()
    
    #build credentials
    credentials = SignedJwtAssertionCredentials(serviceAccount, key, scope, prn=superAdmin)
    
    #authenticate
    http = httplib2.Http()
    httplib2.debuglevel = False #change this to True if you want to see the output
    http = credentials.authorize(http=http)
    directoryService = build(serviceName='admin', version='directory_v1', http=http)
    
    #create and/or open a file that we'll append to
    outputFileName = domain + '_userList.csv'
    outputFile = open(outputFileName, 'a')
    outputFile.write('primaryEmail, lastLoginTime, name, isAdmin, orgUnitPath\n') #write the headers
    
    pageToken = None #this is the variable where we'll store the next page token
    while True:
        try:
            page = directoryService.users().list(domain=domain, customer=customerId, maxResults='500', pageToken=pageToken).execute()
            users = page['users']            
            for user in users: #parse the users from the page variable
                primaryEmail = user['primaryEmail']
                lastLoginTime = user['lastLoginTime']
                name = user['name']['fullName']
                isAdmin = user['isAdmin']
                orgUnitPath = user['orgUnitPath']
                #print primaryEmail, lastLoginTime, name, isAdmin, orgUnitPath
                #log to a file
                outputFile.write(primaryEmail + ',' + str(lastLoginTime) + ',' + name + ',' + str(isAdmin) + ',' + str(orgUnitPath))
                outputFile.write( '\n')
            pageToken = page['nextPageToken'] #this will error if there's no nextPageToken
        except:
            print 'We probably reached the end of ' + domain
            break
    outputFile.close()

#open and read the csv file that contains the list of domains, account numbers, and customer IDs
domainListFile = open('domainList.csv', 'rb')
domainList = csv.reader(domainListFile)

for row in domainList:
    domain = row[0] #the first entry in this row is the domain
    account = row[1]
    customerId = row[2]
    downloadUsers(domain, account, customerId)

'''
for user in page:
 primaryEmail = page.get(user['primaryEmail'])
 lastLoginTime = page.get('lastLoginTime')
 name = page.get('name')
 isAdmin = page.get('isAdmin')
 orgUnitPath = page.get('orgUnitPath')
 newPage = page.get('nextPageToken')
 print primaryEmail, lastLoginTime, name, isAdmin, orgUnitPath
'''

'''
#create a user
userinfo = {'primaryEmail': 'newTest@example.com',
            'name': { 'givenName': 'New', 'familyName': 'Test' },
            'password': 'passwordfornewuser1',
            'orgUnitPath':'/Archive'}
directoryService.users().insert(body=userinfo).execute()
'''

'''
#move a user to an org
userOrg = {'orgUnitPath':'/Archive'}
directoryService.users().patch(userKey='newTest@example.com', body=userOrg).execute()
'''

'''
user = directoryService.users().get(userKey = 'newTest@example.com')
pprint.pprint(user.execute())
'''
