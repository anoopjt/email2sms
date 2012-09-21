# coding: utf-8
#------------------------------------------------------------------
#Author: Anoop Jacob Thomas                                       |
#Email: anoopjt@gmail.com                                         |
#License: GNU GPL 3.0 or any later you choose                     |
#-----------------------------------------------------------------|
#This is part of email2sms using 160by2.com, send_sms() can be    |
#used to send sms through 160by2.com service                      |
#------------------------------------------------------------------

import mechanize
import cookielib

import sys
import getpass

def get_weburl(action,id160by2):
    weburl = "http://www.160by2.com/" + action + ".action?" + id160by2
    return weburl

def check_number(num):
    error = {'user':"User name/destination number should be 10 characters long and should contain only numbers starting with 7 or 8 or 9"}
    if len(num) == 10 and num[0] in ('7','8','9'):
        try:
            int(num)
        except:
            sys.exit(error['user'])
    else:
        sys.exit(error['user'])


def send_sms(user,password,destination,message):
    """
    send_sms(user,password,destination,message)

    This uses the 160by2.com account to send sms.
    Uses python-mechanize
    """
    check_number(user)
    check_number(destination)

    if message.strip() == "":
        sys.exit("Enter a valid message")

    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()

    br.set_cookiejar(cj)
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),max_time=10)

    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    r = br.open('http://www.160by2.com')
    
    br.select_form(nr=0)
    br.form['username'] = user
    br.form['password'] = password
    br.submit()

    id160by2 = br.response().read().split('SendSMS?')[2].split(';')[0].split("'")[0]
    sendsms = '/SendSMS?'+id160by2
    br.open('http://www.160by2.com'+sendsms)

    br.select_form(nr=0)
    br.form['mobile1'] = destination
    br.form['msg1'] = message[:140]
    s = get_weburl('SendSMSAction',id160by2)
    br.form.action = s
    br.submit()

if __name__ == "__main__":
    pass
