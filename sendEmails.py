# approved senders: https://support.google.com/a/answer/2368132

password = raw_input('Enter the admin password: ')

import smtplib
import csv
import time

csvFile = 'userAccountsToEmail2.csv'
logFile = open('userAccountsThatHaveBeenEmailed.csv', 'a') #open a log file that we'll append to

totalRows = sum(1 for row in open(csvFile, 'rb')) #count how many rows there are in the CSV file
print 'There are ', totalRows, ' entries in ', csvFile
countDown = totalRows #a variable we'll decrement as a count down to completion
currentRow = 0 #for keeping track of where we are in the CSV file

def buildEmail(recipient, firstName):
    subject = firstName + ', your account will soon be archived'
    paragraph1 = 'In case you have not already heard at school, this account (' + recipient + ') will be archived (and no longer available) on October 31st.<p>'
    paragraph2 = 'For information on how to move your data to your new account, see <a href="http://is.eips.ca/about/school-news/post/transferring-data-to-a-new-google-account">http://is.eips.ca/about/school-news/post/transferring-data-to-a-new-google-account</a>.<p>'
    paragraph3 = 'Please start using your new account as soon as possible. New student accounts follow the pattern firstname lastinitial and two-digit grad year (e.g. davidh26).<p>'
    paragraph4 = 'For more information, contact your school Google Administrator.'
    body = paragraph1 + paragraph2 + paragraph3 + paragraph4
    headers = "\r\n".join(["from: " + adminEmail, "subject: " + subject, "to: " + recipient, "mime-version: 1.0", "content-type: text/html"])
    content = headers + "\r\n\r\n" + body #join everything together in to a single variable
    return content

def sendEmail(adminEmail, password, recipient, content):
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.ehlo()
    session.starttls()
    session.login(adminEmail, password) #log in to the session
    session.sendmail(adminEmail, recipient, content) #send the email
    return 'email sent to ' + recipient

importFile = open(csvFile, 'rb') #(re)open the CSV file that we want to parse (since totalRows already looped through it)
reader = csv.reader(importFile) #we'll read the CSV file with this
for row in reader: #the loop that reads through the CSV file we mentioned earlier
    recipient = row[0] #the first entry on this row is the email address
    domain = row[1]
    firstName = row[2]
    if domain != 'Domain': #meaning that we are not looking at the header row
        adminEmail = 'is@' + domain
        content = buildEmail(recipient, firstName)
        print sendEmail(adminEmail, password, recipient, content)
    print countDown, '(row number ', currentRow, ' completed)'
    logFile.write(time.strftime('%Y-%m-%d_%H%M%S'))
    logFile.write(',')
    logFile.write(recipient)
    logFile.write('\n')
    currentRow += 1 #increment the currentRow variable
    countDown -= 1 #decrement the countDown variable

#close the file(s)
importFile.close()