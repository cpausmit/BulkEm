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

* git clone git@github.com:cpausmit/BulkEm
* cd ./BulkEm

Make sure to adjust the $BULK_EMAIL_CLIENT ('linux' or 'mac') before executing install

* ./install.sh

Important always before use to setup

* source BulkEm/setup.sh


Sending Emails - Easy Way
-------------------------

There are two files to consider, the distributor and the email template. In the default setup they are:

* _./default/distributor.csv_ (the default distributor)
* _./default/template.eml_ (the default email template)

WARNING: it is absolutely essential to carefully check these two files carefully. If there is something wrong you might be sending a ton of email to a ton of people. So, please, be careful. Once you are sure it is easy to send them off. First do a test run:

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
--------------------

If you are more regularly doing bulk email you will want to setup a directory specific to the project and maintain a distributor and separate files for all messages you want to send. So, for my class Course77 I could do something like this:

* mkdir Course77
* edit  Course77/students.csv
* edit  Course77/welcome.eml
* edit  Course77/results-exam1.eml

and send out the welcome emails like this:

* bulkEm.py --exe  --base=Course77  --distributor=students.csv  --template=welcome.eml

In the distributor file you can freely add more tags they will be automatically searched and replaced in the text using the following pattern XX-_tag_-XX. So, if you define in the distributor a tag called LAST_NAME the template email should contain the string XX-LAST_NAME-XX, which will be replaced in the email that is sent.


Editing the distributor list
----------------------------

The distributor list is the heart of the bulk email submission. We choose this to be a ascii file for the easy of editing. It can be edited in excel or libreoffice as a spreadsheet but it is important to make sure the 'separator' if consistent with the definition of the separators used in BulkEm. The default field separator is a ":" but it can be adjusted using the environment variable defined in the install script: install.sh

The first row of that file defines the _tags_. A tag is a case sensitive sequence of characters, like: FIRST_NAME or last_name. You can define as many tags as you like. The program will for each person on the distribution list read all tag values and replace any of those occurrences in the template to generate the personal email text. In the template the tags are specially protected by framing them: XX-_tag_-XX.