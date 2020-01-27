#!/bin/bash
#---------------------------------------------------------------------------------------------------
# Install the BulkEmail package.
#---------------------------------------------------------------------------------------------------

# generate the setup file
rm -f setup.sh
touch setup.sh
echo "# CAREFUL THIS FILE IS GENERATED AT INSTALL"               >> setup.sh
echo "export BULK_EMAIL_CLIENT=linux"                            >> setup.sh
echo "export BULK_EMAIL_SEPARATOR=:"                             >> setup.sh
echo "export BULK_EMAIL_BASE="`pwd`                              >> setup.sh
echo "export PATH=\"\$PATH:\$BULK_EMAIL_BASE/bin\""              >> setup.sh
echo "export BULK_EMAIL_SMTP=\$BULK_EMAIL_BASE/default/smtp.cfg" >> setup.sh
echo ""                                                          >> setup.sh

# initialize
echo " "
echo " Initialize with:"
echo " "
echo "   source ./setup.sh"
echo " "

exit 0
