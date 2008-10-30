#! /usr/bin/env python2.4

import os

# set path to WNS
import wnsrc

# ... because the module WNS unit test framework is located there.
import pywns.WNSUnit

testSuite = pywns.WNSUnit.TestSuite()

# create a system test
roadMapTest = pywns.WNSUnit.SystemTestSuite(sandboxPath = os.path.join('..', '..', '..', 'sandbox'),
                                            
                                            configFile = 'roadMapFromFile.py',
                                            shortDescription = 'Mobility components from RISE (Roadmap mobility)',
                                            disabled = False,
                                            disabledReason = "")

manhattanTest = pywns.WNSUnit.SystemTestSuite(sandboxPath = os.path.join('..', '..', '..', 'sandbox'),
                                              
                                              configFile = 'config.py',
                                              shortDescription = 'Mobility components from RISE (Manhattan mobility)',
                                              disabled = False,
                                              disabledReason = "")

ownRNGTest = pywns.WNSUnit.ProbesTestSuite(sandboxPath = os.path.join('..', '..', '..', 'sandbox'),
                                            
                                            configFile = 'configOwnRNG.py',
                                            shortDescription = 'Testing mobility RNGs',
                                            runSimulations = True,
                                            disabled = False,
                                            disabledReason = "")


testSuite.addTest(roadMapTest)
testSuite.addTest(manhattanTest)
testSuite.addTest(ownRNGTest)

if __name__ == '__main__':
    # This is only evaluated if the script is called by hand

    # if you need to change the verbosity do it here
    verbosity = 2

    pywns.WNSUnit.verbosity = verbosity

    # Create test runner
    testRunner = pywns.WNSUnit.TextTestRunner(verbosity=verbosity)

    # Finally, run the tests.
    testRunner.run(testSuite)
