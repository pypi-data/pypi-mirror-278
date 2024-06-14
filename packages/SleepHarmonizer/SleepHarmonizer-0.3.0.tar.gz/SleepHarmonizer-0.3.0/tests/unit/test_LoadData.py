from unittest.mock import patch

from pyPhases.test import mockLogger
from pyPhases.test.Mocks import OverwriteConfig
from pyPhases.test.TestCase import TestCase

from SleepHarmonizer.phases.LoadData import LoadData


class TestLoadData(TestCase):
    phase = LoadData()

    def config(self):
        return {"dataversion": {"recordIds": None, "groupBy": None}}

    @OverwriteConfig({"dataversion": {"recordIds": ["id1", "id2", "id3"]}})
    def testMainFixedRecordIds(self):
        self.assertDataEqual("allDBRecordIds", {"id1": ["id1"], "id2": ["id2"], "id3": ["id3"]})

    @patch("pyPhasesRecordloader.RecordLoader.RecordLoader.getRecordList", return_value=["1", "2", "3"])
    @patch("pyPhasesRecordloaderSHHS.recordLoaders.RecordLoaderSHHS.RecordLoaderSHHS.getMetaData", return_value={})
    @patch("pyPhasesRecordloaderSHHS.recordLoaders.RecordLoaderSHHS.RecordLoaderSHHS.getSignalHeaders", return_value={})
    @patch("pathlib.Path.exists", return_value=True)
    @mockLogger
    def testMainRecordloader(self, mockerlog, pathexistMock, mock_getSignalHeaders, mock_getRecordList, mock_getMetData):
        self.assertDataEqual("allDBRecordIds", {"1": ["1"], "2": ["2"], "3": ["3"]})
