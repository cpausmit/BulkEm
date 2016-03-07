#!/usr/bin/env python
#---------------------------------------------------------------------------------------------------
#
# Script for sending a mildly customized e-mail to a list of people, like referees, advisors,
# students, reviewers etc.
#
# Customization is possible by defining a list of tags that will be replaced in the email template
# that one can write. The tags will be the first row of a table. All following rows of the table are
# the specific specifiction of these tags for one email.
#
# Checkout the examples in directory ./default:
#
#   - template.eml     -- a template email
#   - distributor.csv  -- an example distributor file
#
#                                                           Written: March 05, 2016 (Christoph Paus)
#---------------------------------------------------------------------------------------------------
import sys,os,re,getopt

def getTagsFromString(tags,line):
    # read this line and find all tags

    while (True):
        try:
            idx = line.index('XX-')
            line = line[idx:]
            if line.index('-XX'):
                jdx = line.index('-XX')
                tag = line[3:jdx]
                tags.append(tag)
                line = line[jdx+3:]
        except:
            break

    return tags

def makeDictionary(tags,line):
    # make a dictionary out of a given set of column taks and a row from the table

    values = {}
    v = line.split(':')
    i = 0
    for tag in tags:
        value = v[i]
        values[tag] = value
        i += 1

    return values

def readDistributor(base,distributor,debug):
    # read the distributor and find all relevant tags for personalization
    
    tags = []
    values = []

    cmd = 'cat ' + base + '/' + distributor
    for line in os.popen(cmd).readlines():
        line = line[:-1]
        f = line.split(':')
        if len(tags) < 1:
            for tag in f:
                tags.append(tag)
        else:
            if len(tags) != len(f):
                print ''
                print ' ERROR - invalid line in distributor: ' + line
                print '         please correct distributor file before proceeding.'
                print '         EXIT now!' 
                print ''
                sys.exit(1)
            else:
                values.append(line)

    if debug:
        print '\n Found the following tags:\n'
        for tag in tags:
            print '  -> ' + tag

    return tags,values

def readTemplate(base,template,tags,debug):
    # read the email template and find all relevant tags to make sure they are defined

    text = ''
    usedTags = []
    cmd = 'cat ' + base + '/' + template
    for line in os.popen(cmd).readlines():
        text += line
        usedTags = getTagsFromString(usedTags,line)
                
    
    if debug:
        print '\n Found the following used tags:\n'
    for tag in usedTags:
        if tag in tags:
            if debug:
                print ' defined:  ' + tag
        else:
            print ' Tag in template but NOT defined in distributor -- ' + tag
            sys.exit(1)
            
    if debug:
        print '\n Found the following text:\n'
        print text

    return usedTags,text


def generateEmail(text,values,debug):
    # generate the specific email text

    emailText = text

    for tag, value in values.iteritems():
        if debug:
            print " Tag: " + tag + ' ' + value

        emailText = emailText.replace('XX-'+tag+'-XX',value)

    return emailText

#===================================================================================================
# M A I N
#===================================================================================================
# Define string to explain usage of the script
usage  = "\nUsage: email.py  --base=<dir>  --template=<eml-file>  --distributor=<csv-file>\n";
usage += "                 [ --help  -debug  --test ]\n\n"

# Define the valid options which can be specified and check out the command line
valid = ['base=','template=','distributor=','exe','help','debug','test']
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
exe = False
help = False
debug = False
test  = False
base = './default'
template = 'template.eml'
distributor = 'distributor.csv'

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
    if opt == "--base":
        base = arg
    if opt == "--template":
        template  = arg
    if opt == "--distributor":
        distributor = arg

# Read the distributor
(tags, table) = readDistributor(base,distributor,debug)

# Read the text template
(usedTags, text) = readTemplate(base,template,tags,debug)

# Make spool area
cmd = 'mkdir -p ' + base + '/spool'
os.system(cmd)

# Generate the corresponding emails
for line in table:
    values = makeDictionary(tags,line)
    emailText = generateEmail(text,values,debug)
    spoolFile = base + '/spool/' + values['EMAIL'] + '_' + template

    # Show what we are sending in debug mode
    if debug:
        print '\n NEXT EMAIL\n ==========\n'
        print ' spool: ' + spoolFile + '\n'
        print emailText

    # Create the spool file
    output = open(spoolFile,'w')
    output.write(emailText)
    output.close()
    
    # Send the spoolfile as email
    cmd = 'sendFileAsEmail.py --exe --file="' + spoolFile + '"'
    if debug:
        cmd += ' --debug'
    print ' CMD: ' + cmd
    if exe:
        print ' Sending'
        os.system(cmd)
