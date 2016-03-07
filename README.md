# BulkEm -- Bulk Email Sending

BulkEm is a program to send customized emails in bulk. The most straight forward example is to start with the default setup, edit it and just send the first emails in bulk.

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

All parameters can be specified via command line just do:

* bulkEm.py --help
