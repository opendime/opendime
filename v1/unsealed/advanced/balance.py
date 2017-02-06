#!/usr/bin/env pythonw
#
# Python code to check balance and send funds if unsealed.
#
# You can run this with python2 or python3. Perhaps you can just
# double click it? If not, in a Terminal window, type this command:
#
#
#   python balance.py
#
#
# That will show the current balance for this Opendime by asking a
# number of blockchain servers on the public Internet. Then,
# if this Opendime is unsealed, it will also offer to move all funds to
# another bitcoin address.
#
# IMPORTANT: An Internet connection is required, and your privacy
# may be impacted by these network connections, and/or third party
# services.
#
# You may inspect the code by unzipping support/pycode.zip 
# It makes heavy use of pycoin, which it downloads before running.
#
import os, sys; sys.path.insert(0, os.path.normpath(__file__ + '/../../support/pycode.zip'))
import pycode.od_wallet; pycode.od_wallet.main()
