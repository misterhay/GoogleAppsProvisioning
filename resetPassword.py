# this can run on a laptop for self-service password reset

adminUser = raw_input('Enter the admin username, without the domain (e.g. dhay):')
adminPassword = raw_input('Enter the admin password: ')

import gdata.apps.client

def updateUser(email): #a function for creating a user account
    #logFile = open(logFileName, 'a') #create and/or open a log file that we'll append to
    domainIndex = email.find('@') #where is the @ at?
    domain = email[domainIndex+1:] #the domain is the stuff after the @
    username = email[:domainIndex] #the username is the stuff before the @
    client = gdata.apps.client.AppsClient(domain=domain)
    client.ClientLogin(email=adminUser+'@'+domain, password=adminPassword, source='apps') #log in to the Google Apps domain
    client.ssl = True #because we need to use SSL
    try: #as long as there are no errors
        account = client.RetrieveUser(user_name=username) #get the user account
        account.login.password = 'welcometogoogleapps'
        updateResult = client.UpdateUser(username, account) #push the update
        print 'Your new password is   welcometogoogle'
        result = ' updated successfully'
        time.sleep(5)
        print "\n" * 80 #clear screen
    except: result =' error'
    return result #return the result back to the loop

while True:
    print 'This will reset your password.'
    print '\n' * 2
    email = raw_input('Please enter your Google Apps email address (e.g. dhay@uncas.ca or david.hay@uncas.ca): ')
    #ask for email address
    print '\n' * 80
    print 'Hello ' + email + ' we will reset your password for you.'
    updateUser(email) #call updateUser(email) function