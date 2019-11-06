#!/usr/bin/env python
#---------------------------------------------------------------------------------------------------
#
# Script to send a given file as email. There are a number of predefined tags that we will extract
# from the file header.
#
# Checkout the examples in directory ./default/spool:
#
#                                                           Written: March 05, 2016 (Christoph Paus)
#---------------------------------------------------------------------------------------------------
import sys,os,re,getopt
import ConfigParser

import smtplib
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders

#CLIENT = os.getenv('BULK_EMAIL_CLIENT','linux')
SMTP_CFG = os.getenv('BULK_EMAIL_SMTP','.smtp')

def readEmailFile(spoolFile,debug):
    # read the email template and find all relevant tags to make sure they are defined

    header = ''
    body = ''
    emailTags = {}

    if debug:
        print " --> Read file"
    isHeader = True
    cmd = 'cat "' + spoolFile + '"'
    if debug:
        print ' CMD: ' + cmd
    for line in os.popen(cmd).readlines():
        # here we find the header and its tags
        if (':' in line) and isHeader:
            if ':' in line:
                line = line[:-1]
                f = line.split(':')
                tag = (f[0]).lower()
                value = ":".join(f[1:])
                # remove leading blank space
                value = value.lstrip()
                if debug:
                    print ' Adding tag: %s -> %s'%(tag,value) 
                emailTags[tag] = value
        # here we make the body of the message
        else:
            isHeader = False
            body += line

    if debug:
        print " Done reading file"

    return emailTags,body

#===================================================================================================
# M A I N
#===================================================================================================
# Define string to explain usage of the script
usage  = "\nUsage: sendFileAsEmail.py  --file=<file>\n";
usage += "                         [ --exe  --help  --debug  --test ]\n\n"

# Define the valid options which can be specified and check out the command line
valid = ['file=','help','exe','debug','test']
try:
    opts, args = getopt.getopt(sys.argv[1:], "", valid)
except getopt.GetoptError, ex:
    print usage
    print str(ex)
    sys.exit(1)
    
# --------------------------------------------------------------------------------------------------
# Get all parameters for the production
# --------------------------------------------------------------------------------------------------
# Set defaults for each option
help = False
exe = False
debug = False
test  = False
spoolFile = ''

# Read new values from the command line
for opt, arg in opts:
    if opt == "--help":
        print usage
        sys.exit(0)
    if opt == "--exe":
        exe = True
    if opt == "--debug":
        debug = True
    if opt == "--test":
        test  = True
    if opt == "--file":
        spoolFile = arg

# Test whether file exists
if not os.path.isfile(spoolFile):
    print '\n ERROR - file does not exist (file: %s).'%(spoolFile)
    print '         EXIT.\n'
    sys.exit(1)


# Read the smtp configuration file
config = ConfigParser.RawConfigParser()
config.read(SMTP_CFG)
# SMTP config
email_server = config.get('smtp','server')
email_user = config.get('smtp','user')
email_password = config.get('smtp','password')

# First we need to decode the header and the body
(emailTags,body) = readEmailFile(spoolFile,debug)
    
# needed for smtp communication (all recipients go here)
email_send = [ emailTags['to'] ] # recipient list
for em in ("%s,%s"%(emailTags['cc'],emailTags['bcc'])).split(","):
    if debug:
        print ' APPEND: ' + em.strip()
    email_send.append(em.strip())

# generate the message
msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = emailTags['to']
if 'cc' in emailTags:
    msg['CC'] = emailTags['cc']
if 'subject' in emailTags:
    msg['Subject'] = emailTags['subject']
if 'replyto' in emailTags:
    msg.add_header('reply-to',emailTags['replyto'])
if 'attach-file' in emailTags:
    with open(emailTags['attach-file'],"rb") as f:
        part = MIMEApplication(f.read(),Name=os.path.basename(emailTags['attach-file']))
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(emailTags['attach-file'])
        msg.attach(part)

# finally add the message body
msg.attach(MIMEText(body,'plain'))
text = msg.as_string()

if debug:
    print " TAGS"
    print emailTags
    print " BODY"
    print body
    print " TEXT"
    print text
if exe:
    server = smtplib.SMTP(email_server,587)
    server.starttls()
    server.login(email_user,email_password)
    server.sendmail(email_user,email_send,text)
    server.quit()