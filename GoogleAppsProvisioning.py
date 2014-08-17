adminUser = 'david.hay'
adminPassword = 'badpassword' #obviously this is an insecure way to store your admin password
csvFile = 'powerschoolexport.csv'

import time
import csv
import gdata.apps.service

totalRows = sum(1 for row in open(csvFile, 'rb')) #count how many rows there are in the CSV file
print 'There are ', totalRows, ' entries in ', csvFile
countDown = totalRows #a variable we'll decrement as a count down to completion
currentRow = 0 #for keeping track of where we are in the CSV file
logFileName = 'GoogleAppsProvisioningScript' + time.strftime('%Y-%m-%d_%H%M%S') + '.txt' #build a name for the log file
logFile = open(logFileName, 'a') #create and open a log file that we'll append to

importFile = open(csvFile, 'rb') #(re)open the CSV file that we want to parse (since totalRows already looped through it)
reader = csv.reader(importFile) #we'll read the CSV file with this

def createUser(email, firstname, lastname, userPassword): #a function for creating a user account
    domainIndex = email.find('@') #where is the @ at?
    username = email[:domainIndex] #the username is the stuff before the @
    domain = email[domainIndex+1:] #the domain is the stuff after the @
    service = gdata.apps.service.AppsService(email=adminUser+'@'+domain, domain=domain, password=adminPassword)
    service.ProgrammaticLogin() #log in to the Google Apps domain
    try: #as long as there are no errors
#        result = service.CreateUser(username, lastname, firstname, userPassword) #create the user account
        service.RetrieveUser(username) #for testing we will check if user exists
        result = 'created successfully'
    except gdata.apps.service.AppsForYourDomainException , e: #if there is an error
        eString = str(e) #convert the error to a string
        errorStart = eString.find('reason="') + 8 #find the start of the error
        errorEnd = eString.find('" />') #find the end of the error, we'll do it this way rather than using ElementTree
        #logFile.write('check https://developers.google.com/google-apps/provisioning/reference#GDATA_error_codes\n')
        result = 'Error: ' + eString[errorStart:errorEnd] #return the error message, for logging purposes
    return result #return the result back to the loop

for row in reader: #the loop that reads through the CSV file we mentioned earlier
    email = row[0] #the first entry on this row is the email address
    firstname = row[1]
    lastname = row[2]
    userPassword = row[3]
    if currentRow > 0: #because we'll assume that the first row contains column titles, otherwise use >-1 or omit this line
        result = createUser(email, firstname, lastname, userPassword) #call the function to create a User
        rowString = str(rowNumber) #convert that rowNumber integer to a string so we can concatenate it
        #print countDown + '(row number ' + rowString + ' parsed)' #print to the console, in case anyone is watching
        print countDown, '(row number ', rowNumber, ' parsed)'
        logFile.write(rowString + time.strftime('%Y-%m-%d_%H:%M:%S') + ' ' + email + ' ') #log the date/time and email we tried to create
        logFile.write(str(result)) #log the result of that function
        logFile.write( '\n') #write a new line to the log file
    currentRow += 1 #increment the rowNumber variable

#close the files
importFile.close()
logFile.close()


