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

def readEmailFile(spoolFile,debug):
    # read the email template and find all relevant tags to make sure they are defined

    header = ''
    body = ''
    emailTags = {}

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
    print '\n ERROR - file does not exist (%s).'%(spoolFile)
    print '         EXIT.\n'
    sys.exit(1)

# First we need to decode the header and the body
(emailTags,body) = readEmailFile(spoolFile,debug)

cmd = "mail "
if 'attach-file' in emailTags:
    cmd += "-a " + emailTags['attach-file'] + " "
if 'bcc' in emailTags:
    cmd += "-b " + emailTags['bcc'] + " "
if 'cc' in emailTags:
    cmd += "-c " + emailTags['cc'] + " "
if 'replyto' in emailTags:
    cmd += "-S replyto=" + emailTags['replyto'] + " "
if 'subject' in emailTags:
    cmd += "-s '" + emailTags['subject'] + "' "

cmd += emailTags['to'] + " "
    
cmd += ' <<EOT \n' + body + '\nEOT'
    
if debug:
    print ' CMD: ' + cmd
if exe:
    os.system(cmd)
