# The inputfile should have emailaddress, organizationName
# where organizationName is Staff, EIPS Admin, or Grad 20xx (case insensitive)
# Staff and EIPS Admin can be added to the spreadsheet manually
# for students, organizationName is  ="Grad "&2015+12-C2  where C2 is current grade

adminUser = raw_input('Enter the admin username, without the domain (e.g. dhay): ')
adminPassword = raw_input('Enter the admin password: ')
print "\n" * 80 #clear screen
csvFile = 'userAccountsAndOrganizationsStudents.csv'

import time
import csv
import gdata.apps.organization.client

totalRows = sum(1 for row in open(csvFile, 'rb')) #count how many rows there are in the CSV file
print 'There are ', totalRows, ' entries in ', csvFile
countDown = totalRows #a variable we'll decrement as a count down to completion
#currentRow = 0 #for keeping track of where we are in the CSV file

importFile = open(csvFile, 'rb') #(re)open the CSV file that we want to parse (since totalRows already looped through it)
reader = csv.reader(importFile) #we'll read the CSV file with this

outputFileName = 'moveToOrganizationsLog' + time.strftime('%Y-%m-%d_%H%M%S') + '.csv' #build a name for the log file
outputFile = open(outputFileName, 'a') #create and/or open a log file that we'll append to

def moveToOrganization(email, organizationName):
    email = email
    organizationName = organizationName
    domainIndex = email.find('@') #where is the @ at?
    #username = email[:domainIndex] #the username is the stuff before the @
    domain = email[domainIndex+1:] #the domain is the stuff after the @
    adminEmail = adminUser + '@' + domain
    ouclient = gdata.apps.organization.client.OrganizationUnitProvisioningClient(domain=domain)
    ouclient.ClientLogin(email=adminEmail, password=adminPassword, source ='apps')
    customerIdString = str(ouclient.RetrieveCustomerId())
    idStart = customerIdString.find('name="customerId" value="') + 25
    idEnd = customerIdString.find(' /><ns2:property name="customerOrgUnitName"') - 1 #even though they are all 9 digits long
    customer_id = customerIdString[idStart:idEnd]
    #uclient.RetrieveOrgUser(customer_id, email)
    #ouclient.CreateOrgUnit(customer_id, organizationName, parent_org_unit_path='/', description=organizationName, block_inheritance=False) #create an organization
    try:
        ouclient.UpdateOrgUser(customer_id, email, organizationName) #move the user to the organization
        result = email + " " + organizationName
    except:
        result = email + " error"
    return result

for row in reader:
    email = row[0]
    organizationName = row[1]
    print countDown, email, organizationName
    result = moveToOrganization(email, organizationName)
    outputFile.write(result)
    outputFile.write('\n')
    countDown -= 1 #decrement the countDown variable


#for changing organization properties:
#ouclient.RetrieveOrgUnit(customer_id, org_unit_path)
#ouclient.UpdateOrgUnit(customer_id, org_unit_path, org_unit_entry)

#import xml.etree.ElementTree as et
#root = et.fromstring(str(orgs))


#client = gdata.apps.client.AppsClient(domain=domain)
#client.ClientLogin(email=adminUser+'@'+domain, password=adminPassword, source='apps')
#client.ssl = True



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