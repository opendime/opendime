#!/usr/bin/env python
#
# Python code to check balance and send funds if unsealed.
#
#   python balance.py
#
# That will show the current balance for this Opendime by asking a
# number of blockchain servers on the public Internet. Then, if this
# Opendime is unsealed, it will also offer to move all funds to
# another bitcoin address.
#
# IMPORTANT: An Internet connection is required, and your privacy
# may be impacted by these network connections, and/or third party
# services.
#
import os, sys; sys.path.insert(0, os.path.normpath(__file__ + '/../../support/pycode.zip'))
import pycode.od_wallet; pycode.od_wallet.main()
