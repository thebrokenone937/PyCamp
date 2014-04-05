import unittest
from project.tests.projects_test import *

testList = [ProjectsTest]
testLoad = unittest.TestLoader()
 
caseList = []
for testCase in testList:
    testSuite = testLoad.loadTestsFromTestCase(testCase)
    caseList.append(testSuite)
 
testSuite = unittest.TestSuite(caseList)

if __name__ == "__main__":
    testRunner = unittest.TextTestRunner()
    testResult = testRunner.run(testSuite)
    
    print
    print "---- START OF TEST RESULTS"
    print testResult
    print
    print "fooResult::errors"
    print testResult.errors
    print
    print "fooResult::failures"
    print testResult.failures
    print
    print "fooResult::skipped"
    print testResult.skipped
    print
    print "fooResult::successful"
    print testResult.wasSuccessful()
    print
    print "fooResult::test-run"
    print testResult.testsRun
    print "---- END OF TEST RESULTS"
    print