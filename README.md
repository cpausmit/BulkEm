# BulkEm -- Bulk Email Sending

BulkEm is a program to send customized emails in bulk. The most straight forward example is to start with the default setup, edit it and just send the first emails in bulk. It is based on the command line mail program in linux/unix systems. Please, test whether you can send email from your computer like this:

* mail -c your_email@xy.com -S replyto=youremail@xy.com -s 'Testing BulkEm' your_email@xy.com

Setting up a proper mail client is for some easy for others it can be complicated. Using google usually get's you there. The email delivery can sometimes take some time, but should be done in minutes.



First install

* git clone git@github.com:cpausmit/BulkEm
* cd ./BulkEm
* ./install.sh

then setup

* source ./setup.sh

There are two files to consider, the distributor and the email template. In the default setup they are:

* _./default/distributor.csv_ (the default distributor)
* _./default/template.eml_ (the default email template)

WARNING: it is absolutely essential to carefully check these two files carefully. If there is something wrong you might be sending a ton of email to a ton of people. So, please, be careful. Once you are sure it is easy to send them off. First do a test run:

* bulkEm.py

Then when all looks good:

* bulkEm.py --exe

This is equivalent to:

* bulkEm.py --exe  --base=default  --distributor=distributor.csv  --template=template.eml

All parameters can be specified via command line just do:

* bulkEm.py --help

More complex examples

If you are more regularly doing bulk email you will want to setup a directory specific to the project and maintain a distributor and separate files for all messages you want to send. So, for my class Course77 I could do something like this:

* mkdir Course77
* edit  Course77/students.csv
* edit  Course77/welcome.eml
* edit  Course77/results-exam1.eml

and send out the welcome emails like this:

* bulkEm.py --exe  --base=Course77  --distributor=students.csv  --template=welcome.eml

In the distributor file you can freely add more tags they will be automatically searched and replaced in the text using the following pattern XX-<tag>-XX. So, if you define in the distributor a tag called LAST_NAME the template email should contain the string XX-LAST_NAME-XX, which will be replaced in the email that is sent.
