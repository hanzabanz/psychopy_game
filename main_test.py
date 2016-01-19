import main
import os

__author__ = 'hannah'

"""
Testing can be continuously run for time-out or it can be manually clicked through.
"""

testdir = 'test_configs'

for subdir, dirs, files in os.walk(testdir):
    for filename in files:
        fullname = 'test_configs\%s' %filename
        print "\n\nbeginning test for: %s" %filename
        try:
            main.main(fullname, 1)
        except Exception as e:
            print e.message
            print '%s failed' %filename