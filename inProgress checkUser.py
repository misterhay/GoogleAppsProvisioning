adminUser = raw_input('Enter the admin username, without the domain (e.g. dhay):')
adminPassword = raw_input('Enter the admin password: ')
print "\n" * 80 #clear screen
userToCheck = raw_input('Enter the email address of the user you want to check. ')

import time
import csv
import gdata.apps.client

#totalRows = sum(1 for row in open(csvFile, 'rb')) #count how many rows there are in the CSV file
#print 'There are ', totalRows, ' entries in ', csvFile
#countDown = totalRows #a variable we'll decrement as a count down to completion
#currentRow = 0 #for keeping track of where we are in the CSV file

outputFileName = 'checkUsers' + time.strftime('%Y-%m-%d_%H%M%S') + '.csv' #build a name for the log file
outputFile = open(outputFileName, 'a') #create and/or open a log file that we'll append to

outputFile.write('username')
outputFile.write(',')
outputFile.write('domain')
outputFile.write(',')
outputFile.write('first name')
outputFile.write(',')
outputFile.write('last name')
outputFile.write(',')
outputFile.write('admin')
outputFile.write(',')
outputFile.write('agreed to terms')
outputFile.write(',')
outputFile.write('change password at next login')
outputFile.write(',')
outputFile.write('suspended')
outputFile.write( '\n') #write a new line to the log file

domainIndex = userToCheck.find('@') #where is the @ at?
username = userToCheck[:domainIndex] #the username is the stuff before the @
domain = userToCheck[domainIndex+1:] #the domain is the stuff after the @

client = gdata.apps.client.AppsClient(domain=domain)
client.ClientLogin(email=adminUser+'@'+domain, password=adminPassword, source='apps')
client.ssl = True

print username #to the terminal, so we know who the script is looking at
user = client.RetrieveUser("david.hay")
outputFile.write(user.login.user_name)
outputFile.write(',')
outputFile.write(domain)
outputFile.write(',')
outputFile.write(user.name.given_name)
outputFile.write(',')
outputFile.write(user.name.family_name)
outputFile.write(',')
outputFile.write(user.login.admin)
outputFile.write(',')
outputFile.write(user.login.agreed_to_terms)
outputFile.write(',')
outputFile.write(user.login.change_password)
outputFile.write(',')
outputFile.write(user.login.suspended)
outputFile.write( '\n') #write a new line to the log file



def checkUser(email): #a function for checking a user account
    domainIndex = email.find('@') #where is the @ at?
    username = email[:domainIndex] #the username is the stuff before the @
    domain = email[domainIndex+1:] #the domain is the stuff after the @

    #service = gdata.apps.service.AppsService(email=adminUser+'@'+domain, domain=domain, password=adminPassword)
    #service.ProgrammaticLogin() #log in to the Google Apps domain
    try: #as long as there are no errors
        #userObject = service.RetrieveUser(username) #retrieve user
        result = username
    except gdata.apps.service.AppsForYourDomainException , e: #if there is an error
        eString = str(e) #convert the error to a string
        errorStart = eString.find('reason="') + 8 #find the start of the error
        errorEnd = eString.find('" />') #find the end of the error, we'll do it this way rather than using ElementTree
        result = 'Error: ' + eString[errorStart:errorEnd] #return the error message
    return result #return the result back to the loop


#call check UserFunction
#print result


#for row in reader: #the loop that reads through the CSV file we mentioned earlier
#    email = row[0] #the first entry on this row is the email address
#    #firstname = row[1]
#    #lastname = row[2]
#    #userPassword = row[3]
#    #if currentRow > 0: #because we'll assume that the first row contains column titles, otherwise use >-1 or omit this line
#    result = checkUser(email) #call the function to check a User
#    rowString = str(currentRow) #convert that currentRow integer to a string so we can concatenate it
#    #print countDown + '(row number ' + rowString + ' parsed)' #print to the console, in case anyone is watching
#    print countDown, '(row number ', currentRow, ' parsed)'
#    logFile.write(rowString + time.strftime('%Y-%m-%d_%H:%M:%S') + ' ' + email + ' ') #log the date/time and email we tried to create
#    logFile.write(str(result)) #log the result of that function
#    logFile.write( '\n') #write a new line to the log file
#    currentRow += 1 #increment the currentRow variable
#    countDown -= 1 #decrement the countDown variable

outputFile.close() #close the file


