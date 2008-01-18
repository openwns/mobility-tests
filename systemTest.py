#! /usr/bin/env python2.4

import os

# set path to WNS
import wnsrc

# ... because the module WNS unit test framework is located there.
import pywns.WNSUnit

testSuite = pywns.WNSUnit.TestSuite()

# create a system test
roadMapTest = pywns.WNSUnit.ProbesTestSuite(sandboxPath = os.path.join('..', '..', '..', 'sandbox'),
                                            executeable = "wns-core",
                                            configFile = 'roadMapFromFile.py',
                                            shortDescription = 'Mobility components from RISE (Roadmap mobility)',
                                            requireReferenceOutput = False,
                                            disabled = False,
                                            disabledReason = "")

manhattanTest = pywns.WNSUnit.ProbesTestSuite(sandboxPath = os.path.join('..', '..', '..', 'sandbox'),
                                              executeable = "wns-core",
                                              configFile = 'config.py',
                                              shortDescription = 'Mobility components from RISE (Manhattan mobility)',
                                              requireReferenceOutput = False,
                                              disabled = False,
                                              disabledReason = "")

testSuite.addTest(roadMapTest)
testSuite.addTest(manhattanTest)

if __name__ == '__main__':
    # This is only evaluated if the script is called by hand

    # if you need to change the verbosity do it here
    verbosity = 1

    pywns.WNSUnit.verbosity = verbosity

    # Create test runner
    testRunner = pywns.WNSUnit.TextTestRunner(verbosity=verbosity)

    # Finally, run the tests.
    testRunner.run(testSuite)
