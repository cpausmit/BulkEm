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
# Checkout the examples in directory (--base) ./default:
#
#   - (--template)     template.eml     -- a template email
#   - (--distributor ) distributor.csv  -- an example distributor file
#   - (--separator)    os.getenv('BULK_EMAIL_SEPARATOR', ':')
#
#                                                           Written: March 05, 2016 (Christoph Paus)
#---------------------------------------------------------------------------------------------------
import sys, os, re
import csv
from optparse import OptionParser

def brokenHeader(tags):
    print(f" brokenHeader: {tags}")
    return 'EMAIL' not in tags

def brokenLine(values):
    try:
        return '@' not in values['EMAIL']
    except:
        return True

def getTagsFromString(tags, line):
    while True:
        try:
            idx = line.index('XX-')
            line = line[idx:]
            jdx = line.index('-XX')
            tag = line[3:jdx]
            tags.append(tag)
            line = line[jdx+3:]
        except:
            break
    return tags

def makeDictionary(tags, columns):
    values = {}
    for i, tag in enumerate(tags):
        values[tag] = columns[i].strip()
    return values

def readDistributor(base,distributor,separator,debug):
    rc = 1
    values = []
    csvreader = None
    for s in separator:
        if debug:
            print(f" Trying separator: {s}")
            
        with open(f"{base}/{distributor}", 'r') as file:
            try:
                csvreader = csv.reader(file,delimiter=s)
                tags = next(csvreader)
                if brokenHeader(tags):
                    continue
                print(f'\n Found the following tags:\n{tags}')
                for row in csvreader:
                    values.append(row)
                    if debug:
                        print(f'\n Found the following values:\n{values[-1]}')
                rc = 0
                break
            except:
                continue
    return rc, tags, values

def readTemplate(base, template, tags, debug):
    text = ''
    usedTags = []
    cmd = f'cat {base}/{template}'
    for line in os.popen(cmd).readlines():
        text += line
        usedTags = getTagsFromString(usedTags, line)

    if not text:
        print(" ERROR - no email template text found. EXIT!")
        sys.exit(1)

    for tag in usedTags:
        if tag not in tags:
            print(f" Tag in template but NOT defined in distributor -- {tag}")
            sys.exit(1)
        elif debug:
            print(' defined:  ' + tag)

    if debug:
        print('\n Found the following text:\n')
        print(text)
    return usedTags, text

def generateEmail(text, values, debug):
    emailText = text
    for tag, value in values.items():
        if debug:
            print(" Tag: " + tag + ' >' + value + '<')
        emailText = emailText.replace('XX-' + tag + '-XX', value.replace('\\n', '\n'))
    return emailText

#===================================================================================================
# M A I N
#===================================================================================================
usage = "\nUsage: %prog --base=<dir> --template=<eml-file> --distributor=<csv-file> [options]\n"
parser = OptionParser(usage=usage)
parser.add_option("--base", dest="base", default="./default", help="Base directory")
parser.add_option("--template", dest="template", default="template.eml", help="Template file")
parser.add_option("--distributor", dest="distributor", default="distributor.csv", help="Distributor file")
parser.add_option("--separator", dest="separator", default=os.getenv('BULK_EMAIL_SEPARATOR', ':|,'), help="Column separator")
parser.add_option("--exe", action="store_true", dest="exe", default=False, help="Execute send")
parser.add_option("--debug", action="store_true", dest="debug", default=False, help="Debug mode")
parser.add_option("--test", action="store_true", dest="test", default=False, help="Test mode")

(options, args) = parser.parse_args()

base = options.base
template = options.template
distributor = options.distributor
separator = options.separator
exe = options.exe
debug = options.debug
test = options.test

(rc, tags, table) = readDistributor(base, distributor, separator, debug)
if rc != 0:
    print(f" ERROR - distributor file not correct: use --debug to see details")

(usedTags, text) = readTemplate(base, template, tags, debug)

os.system(f'mkdir -p {base}/spool')

for row in table:
    values = makeDictionary(tags, row)
    if brokenLine(values):
        if debug:
            print(f" Broken line:\n{values}")
        continue
    emailText = generateEmail(text, values, debug)
    spoolFile = f'{base}/spool/{values["EMAIL"]}_{template}'

    if debug:
        print('\n NEXT EMAIL\n ==========\n')
        print(' spool: ' + spoolFile + '\n')
        print(emailText)

    with open(spoolFile, 'w') as output:
        output.write(emailText)

    cmd = f'sendFile.py --exe --file="{spoolFile}"'
    if debug:
        cmd += ' --debug'
    print(' ' + cmd)
    if exe:
        print(' Sending')
        os.system(cmd)
