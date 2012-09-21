#!/usr/bin/python
#------------------------------------------------------------------
#Author: Anoop Jacob Thomas                                       |
#Email: anoopjt@gmail.com                                         |
#License: GNU GPL 3.0 or any later you choose                     |
#-----------------------------------------------------------------|
#This is part of email2sms using 160by2.com, this code checks for |
#email and calls send_sms()                                       |
#------------------------------------------------------------------

import imaplib
import os
from sendsms import send_sms
import time

def check_read_mails():
    if os.path.isfile('readmails.txt'):
        readmails = open('readmails.txt','r').read()
    else:
        tempfile = open('readmails.txt','w')
        tempfile.write('0')
        tempfile.close()

def check_email():

    check_read_mails()

    user = "example@example.com" #enter your gmail hosted email address
    host = "imap.gmail.com"
    port = 993
    password = '*********' #replace with your email address password

    check_read_mails()
        
    M = imaplib.IMAP4_SSL(host, port)
    M.login(user,password)
    M.select(readonly=True)
    typ, data = M.search(None, '(UNSEEN SUBJECT )')

    if data[0]:
        emails = data[0].split()
        emails.reverse()

        f = open('readmails.txt')
        readmails = f.read()
        f.close()    

        for num in emails:
            if num not in set(readmails.split()):
                typ, data = M.fetch(num,"(RFC822)")
                from_addr = data[0][1].split("From:")[1].split("\n")[0].strip().split('<')[0].strip()
                print "From:", from_addr
                sub = data[0][1].split("Subject:")[1].split("\n")[0].strip()
                print "Subject:", sub
                message = from_addr + '-' + sub
                f = open('readmails.txt','a')
                f.write(' '+num+' ')
                send_sms('8888888888','********','7777777777',message) #send_sms('160by2 login','160by2 password','destination number','your message')
                time.sleep(0.2)
    M.logout()

if __name__ == "__main__":
    #this is a testing code which will check for email every 5 minutes and nofity you if there is a new email
    count = 0
    while(True):
        check_email()#right now send_sms() is called from check_email(), has to move it outside for modularity
        count = count + 1
        print "Check",count
        time.sleep(300)
