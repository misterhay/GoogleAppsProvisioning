# This is a script for changing/updating usernames

adminUser = raw_input('Enter the admin username, without the domain (e.g. dhay):')
adminPassword = raw_input('Enter the admin password: ')
print "\n" * 80 #clear screen
#csvFile = raw_input("Enter the name of the CSV file to parse, but don't include the .CSV part.")
csvFile = 'addingDotsToAccounts.csv'

import time
import csv
import gdata.apps.client

totalRows = sum(1 for row in open(csvFile, 'rb')) #count how many rows there are in the CSV file
print 'There are ', totalRows, ' entries in ', csvFile
countDown = totalRows #a variable we'll decrement as a count down to completion
currentRow = 0 #for keeping track of where we are in the CSV file

logFileName = 'addingDotsToAccountsLog' + time.strftime('%Y-%m-%d_%H%M%S') + '.txt' #build a name for the log file
logFile = open(logFileName, 'a') #create and/or open a log file that we'll append to

importFile = open(csvFile, 'rb') #(re)open the CSV file that we want to parse (since totalRows already looped through it)
reader = csv.reader(importFile) #we'll read the CSV file with this

def updateUser(oldEmail, newEmail): #a function for creating a user account
    domainIndex = oldEmail.find('@') #where is the @ at?
    domain = oldEmail[domainIndex+1:] #the domain is the stuff after the @
    oldUsername = oldEmail[:domainIndex] #the username is the stuff before the @
    newEmailIndex = newEmail.find('@')
    newUsername = newEmail[:newEmailIndex]
    client = gdata.apps.client.AppsClient(domain=domain)
    client.ClientLogin(email=adminUser+'@'+domain, password=adminPassword, source='apps') #log in to the Google Apps domain
    client.ssl = True #because we need to use SSL
    try: #as long as there are no errors
        account = client.RetrieveUser(user_name=oldUsername) #get the old user account
        account.login.user_name = newUsername #update it to the new user account
        updateResult = client.UpdateUser(oldUsername, account) #push the update
        result = 'updated successfully'
    except: result ='error'
    return result #return the result back to the loop

for row in reader: #the loop that reads through the CSV file we mentioned earlier
    oldEmail = row[0] #the first entry on this row is the old email address
    newEmail = row[1] #the second entry on this row is the new email address
    result = updateUser(oldEmail, newEmail) #call the function to update the User
    rowString = str(currentRow) #convert that currentRow integer to a string so we can concatenate it
    print countDown, '(row number ', currentRow, ' parsed)' #print to the console, in case anyone is watching
    logFile.write(rowString + time.strftime('%Y-%m-%d_%H:%M:%S') + ' ' + newEmail + ' ') #log the date/time and email we tried this
    logFile.write(str(result)) #log the result of that function
    logFile.write( '\n') #write a new line to the log file
    currentRow += 1 #increment the currentRow variable
    countDown -= 1 #decrement the countDown variable

#close the files
importFile.close()
logFile.close()