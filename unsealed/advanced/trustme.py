#!/usr/bin/env pythonw
#
# Python code to verify the legitamacy of this Opendime.
#
# You can run this with python2 or python3. Perhaps you can just
# double click it? If not, in a Terminal window, type this command:
#
#   python trustme.py
#
#
# Since this code is running from the Opendime in question, it is
# somewhat questionable to trust what it says. It's better to use
# code from a trusted source to verify an Opendime. Of course, that
# can be the code on another Opendime that you know is good. To
# test between two units, provide path to the *other* as the argument:
#
#   python trustme.py /Volumes/OPENDIME\ 2
#
#   python trustme.py G:
#
# IMPORTANT: An Internet connection is required, and your privacy
# may be impacted by these network connections, and/or third party
# services.
#
# You may inspect the code by unzipping support/pycode.zip 
# It makes heavy use of pycoin, which it downloads before running.
#
import os, sys; sys.path.insert(0, __file__ + '/../../support/pycode.zip'.replace('/', os.sep))
import pycode.trust_me; pycode.trust_me.main()
