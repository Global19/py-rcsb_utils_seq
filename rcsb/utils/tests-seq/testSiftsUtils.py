##
# File:    SiftsUtilsTests.py
# Author:  J. Westbrook
# Date:    11-Dec-2018
#
# Update:
#
#
##
"""
Various utilities for processing SIFTS  correspondence data.

"""

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"

import logging
import os
import time
import unittest

from rcsb.utils.seq.SiftsUtils import SiftsUtils

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class SiftsUtilsTests(unittest.TestCase):
    def setUp(self):
        self.__dirPath = os.path.join(os.path.dirname(TOPDIR), "rcsb", "mock-data")
        self.__siftsSummaryPath = os.path.join(self.__dirPath, "sifts-summary")
        #
        self.__siftsCacheFile = os.path.join(HERE, "test-output", "sifts_consolidated_mapping.pic")
        self.__siftsCacheJsonFile = os.path.join(HERE, "test-output", "sifts_consolidated_mapping.json")
        #
        self.__startTime = time.time()
        logger.debug("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

    def tearDown(self):
        endTime = time.time()
        logger.info("Completed %s at %s (%.4f seconds)\n", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

    def testWriteSiftsSummaryCache(self):
        su = SiftsUtils(siftsSummaryDirPath=self.__siftsSummaryPath, saveCachePath=self.__siftsCacheFile, useCache=False)
        eCount = su.getEntryCount()
        logger.info("SIFTS entry count %d", eCount)
        self.assertGreaterEqual(eCount, 140000)

    def testWriteSiftsSummaryCacheJson(self):
        entrySaveLimit = 50
        su = SiftsUtils(
            siftsSummaryDirPath=self.__siftsSummaryPath,
            saveCachePath=self.__siftsCacheJsonFile,
            saveCacheKwargs={"fmt": "json", "indent": 3},
            useCache=False,
            entrySaveLimit=entrySaveLimit,
        )
        eCount = su.getEntryCount()
        logger.info("SIFTS entry count %d", eCount)
        self.assertGreaterEqual(eCount, entrySaveLimit)

    def testReadSiftsSummaryCache(self):
        su = SiftsUtils(saveCachePath=self.__siftsCacheFile, useCache=True)
        eCount = su.getEntryCount()
        logger.info("SIFTS entry count %d", eCount)


def readSiftsInfo():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(SiftsUtilsTests("testWriteSiftsSummaryCacheJson"))
    suiteSelect.addTest(SiftsUtilsTests("testWriteSiftsSummaryCache"))
    suiteSelect.addTest(SiftsUtilsTests("testReadSiftsSummaryCache"))
    return suiteSelect


if __name__ == "__main__":
    mySuite = readSiftsInfo()
    unittest.TextTestRunner(verbosity=2).run(mySuite)