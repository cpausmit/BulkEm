BulkEm -- Bulk Email Sending
============================

BulkEm is a program to send customized emails in bulk. The most straight forward example is to start with the default setup, edit it and just send the first emails in bulk. It is based on the command line mail program in linux/unix systems.


Test this can work for you
--------------------------

Please, test whether you can send email from your computer like this:

* _linux:_ mail -c your_email@xy.com -S replyto=your_email@xy.com -s 'Testing BulkEm' recipient@xy.com
* _mac_:   export REPLYTO=your_email@xy.com; mail -c your_email@xy.com -s 'Testing BulkEm' recipient@xy.com 

Setting up a proper mail client is for some easy for others it can be complicated. Using google usually get's you there. The email delivery can sometimes take some time, but should be done in minutes.

For the mac mail tools it looks like attachments cannot be sent, while the linux tools allow this.

Installation
------------

For installation please go to a place where you can find it back easily and proceed:

* git clone git@github.com:cpausmit/BulkEm

Make sure to adjust the $BULK_EMAIL_CLIENT ('linux' or 'mac') in the install.sh script before executing install:

* cd ./BulkEm
* ./install.sh

Important always before use to setup. This will make sure the tools get added to your program execution PATH.

* source BulkEm/setup.sh


Sending Emails
--------------

There are two files to consider, the distributor and the email template. In the default setup they are:

* _./default/distributor.csv_ (the default distributor)
* _./default/template.eml_ (the default email template)

WARNING: it is absolutely essential to carefully check these two files carefully. If there is something wrong you might be sending a ton of email to a ton of people. So, please, be careful. Once you are sure it is easy to send them off. First do a test run.

Find below two examples of how to send email.

Easy Way
_______

* source BulkEm/setup.sh
* cd BulkEm
* bulkEm.py

Then when all looks good:

* bulkEm.py --exe

This is equivalent to:

* bulkEm.py --exe  --base=default  --distributor=distributor.csv  --template=template.eml

All parameters can be specified via command line just do:

* bulkEm.py --help


More complex example
____________________

Always make sure bulkEm is setup:

* source BulkEm/setup.sh

If you are more regularly doing bulk email you will want to setup a directory specific to the project and maintain a distributor and separate files for all messages you want to send. So, for my class Course77, I have a supdirectories for my course emails that are kept in the directories of my course notes. I could do something like this:

* cd    Course77
* mkdir eml
* edit  eml/students.csv
* edit  eml/welcome.eml
* edit  eml/results-exam1.eml

and send out the welcome emails like this:

* cd Course77
* bulkEm.py --exe  --base=eml  --distributor=students.csv  --template=welcome.eml

In the distributor file you can freely add more tags they will be automatically searched and replaced in the text using the following pattern XX-_tag_-XX. So, if you define in the distributor a tag called LAST_NAME the template email should contain the string XX-LAST_NAME-XX, which will be replaced in the email that is sent.


Editing the distributor list
----------------------------

The distributor list is the heart of the bulk email submission. We choose this to be a ascii file for the easy of editing. It can be edited in excel or libreoffice as a spreadsheet but it is important to make sure the 'separator' if consistent with the definition of the separators used in BulkEm. The default field separator is a ":" but it can be adjusted using the environment variable defined in the install script: install.sh

The first row of that file defines the _tags_. A tag is a case sensitive sequence of characters, like: FIRST_NAME or last_name. You can define as many tags as you like. The program will for each person on the distribution list read all tag values and replace any of those occurrences in the template to generate the personal email text. In the template the tags are specially protected by framing them: XX-_tag_-XX.


Here is an example email template:

    To:          XX-EMAIL-XX
    Subject:     Corrections for Writeup 0 (XX-FIRST_NAME-XX XX-LAST_NAME-XX)
    CC:          paus@mit.edu
    replyto:     paus@mit.edu
    attach-file: XX-ATTACHMENT-XX
  
    Dear XX-FIRST_NAME-XX,
  
    please find attached my corrections to your writeups.
    Your overall grade is XX-GRADE-XX.
  
    I grade 4 categories:
  
      Theory (15%),
      Data (30%),
      Analysis (40%) and
      Presentation/Form (15%)
  
    If you have any questions about the grade please contact me.
  
    Cheers, Christoph
  
    ----
    Christoph Paus - (email: paus@mit.edu)

The corresponding distributor would be:

    EMAIL:LAST_NAME:FIRST_NAME:GRADE:ATTACHMENT
    paus@mit.edu:Paus:Christoph:A-:example/paper0-cp.pdf
    student-a@mit.edu:Doe:Al:A+:example/paper0-ad.pdf
    student-b@mit.edu:Doe:Bo:A+:example/paper0-bd.pdf
