adminUser = raw_input('Enter the admin username, without the domain (e.g. dhay):')
adminPassword = raw_input('Enter the admin password: ')
print "\n" * 80 #clear screen
csvFile = 'schoolDomains.csv'

import time
import csv
import gdata.apps.organization.client

totalRows = sum(1 for row in open(csvFile, 'rb')) #count how many rows there are in the CSV file
print 'There are ', totalRows, ' entries in ', csvFile
countDown = totalRows #a variable we'll decrement as a count down to completion
currentRow = 0 #for keeping track of where we are in the CSV file

importFile = open(csvFile, 'rb') #(re)open the CSV file that we want to parse (since totalRows already looped through it)
reader = csv.reader(importFile) #we'll read the CSV file with this

##outputFileName = 'customerIDs' + time.strftime('%Y-%m-%d_%H%M%S') + '.csv' #build a name for the log file
##outputFile = open(outputFileName, 'a') #create and/or open a log file that we'll append to

def checkDomain(domain, organizationName):
    domain = domain
    organizationName = organizationName
    adminEmail = adminUser + '@' + domain
    ##outputFile.write(domain)
    ##outputFile.write(',')
    ouclient = gdata.apps.organization.client.OrganizationUnitProvisioningClient(domain=domain)
    ouclient.ClientLogin(email=adminEmail, password=adminPassword, source ='apps')
    customerIdString = str(ouclient.RetrieveCustomerId())
    idStart = customerIdString.find('name="customerId" value="') + 25
    idEnd = customerIdString.find(' /><ns2:property name="customerOrgUnitName"') - 1 #even though they are all 9 digits long
    customer_id = customerIdString[idStart:idEnd]
    ##outputFile.write(customer_id)
    #orgs = ouclient.RetrieveAllOrgUnits(customer_id)
    #print ouclient.RetrieveOrgUnit(customer_id, 'Staff')
    #numberOfOrgUnits = str(orgs).count('description')
    #print numberOfOrgUnits
    #outputFile.write(numberOfOrgUnits) #gives a buffer error of some sort
    ##outputFile.write( '\n')
    ouclient.CreateOrgUnit(customer_id, organizationName, parent_org_unit_path='/', description=organizationName, block_inheritance=False) #create an organization
    return customer_id

for row in reader:
    print row[0], row[1]
    result = checkDomain(row[0], row[1])


#import xml.etree.ElementTree as et
#root = et.fromstring(str(orgs))


#client = gdata.apps.client.AppsClient(domain=domain)
#client.ClientLogin(email=adminUser+'@'+domain, password=adminPassword, source='apps')
#client.ssl = True

#print username #to the terminal, so we know who the script is looking at
#user = client.RetrieveUser("david.hay")
#outputFile.write(user.login.user_name)
#outputFile.write(',')
#outputFile.write(domain)
#outputFile.write(',')
#outputFile.write(user.name.given_name)
#outputFile.write(',')
#outputFile.write(user.name.family_name)
#outputFile.write(',')
#outputFile.write(user.login.admin)
#outputFile.write(',')
#outputFile.write(user.login.agreed_to_terms)
#outputFile.write(',')
#outputFile.write(user.login.change_password)
#outputFile.write(',')
#outputFile.write(user.login.suspended)
#outputFile.write( '\n') #write a new line to the log file



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

##outputFile.close() #close the file