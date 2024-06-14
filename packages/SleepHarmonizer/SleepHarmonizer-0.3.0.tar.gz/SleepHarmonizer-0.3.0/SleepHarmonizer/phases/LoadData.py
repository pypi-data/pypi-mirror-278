from numpy import save
import pandas as pd
from pyPhases import Phase
from pyPhasesRecordloader import ChannelsNotPresent, RecordLoader
from tqdm import tqdm

class LoadData(Phase):
    """
    load record ids
    """

    def getMetadata(self, allRecordIds):
        recordLoader = RecordLoader.get()
        datasetConfig = self.getConfig("dataversion")

        # filter non existing annotations
        metaDates = []
        for r in tqdm(allRecordIds):
            metaData = {
                "recordId": r,
                "annotationExist": recordLoader.existAnnotation(r),
                "channelMissing": False,
                "samplingRateCheck": True,
            }
            metaDates.append(metaData)

            if metaData["annotationExist"]:
                recordMetadata = recordLoader.getMetaData(r)
                metaData.update(recordMetadata)
            else:
                self.logError(f"record id {r} does not exist")

            if metaData["annotationExist"] and "minimalSamplingRate" in datasetConfig and datasetConfig["minimalSamplingRate"] is not None:
                minimalSamplingRates = datasetConfig["minimalSamplingRate"]

                try:
                    headers = recordLoader.getSignalHeaders(r)

                    for header in headers:
                        typeStr = header["type"]
                        if typeStr in minimalSamplingRates and header["sample_rate"] < minimalSamplingRates[typeStr]:
                            self.logError(f"record id {r} exluded because of minimal sampling rate for {typeStr}")
                            metaData["samplingRateCheck"] = False
                            break
                except ChannelsNotPresent as e:
                    self.logError(f"record id {r} excluded because channels missinng {e.channels}")
                    metaData["channelMissing"] = e.channels

        return metaDates

    def loadRecordIds(self, metadata):
        df = pd.DataFrame(metadata)
        relevant = df.query("annotationExist == True and channelMissing == False and samplingRateCheck  == True")

        filterQuery = self.getConfig("dataversion.filterQuery", False)
        if filterQuery is not False:
            relevant = relevant.query(filterQuery)
        
        return relevant["recordId"].tolist()

    def generateData(self, dataName):
        recordLoader = RecordLoader.get()

        if dataName == "metadata":
            recordLoader.setupRemoteReadOrDownload()
            allRecordIds = recordLoader.getRecordList()
            if len(allRecordIds) == 0:
                raise Exception("No records found. Check your recordLoader config and your dataversion config.")
            metadata = self.getMetadata(allRecordIds)
            if not self.getConfig("dataIsFinal", False):
                self.logWarning("metadata is not final (flag dataIsFinal not set), so the metadata is not saved")
            self.project.registerData("metadata", metadata, save=self.getConfig("dataIsFinal", False))
        elif dataName == "allDBRecordIds":
            datasetConfig = self.getConfig("dataversion")

            if datasetConfig["recordIds"] is not None:
                recordIds = {r: [r] for r in datasetConfig["recordIds"]}
            else:
                metadata = self.getData("metadata", list)
                recordIdsFlat = self.loadRecordIds(metadata)
                recordIds = recordLoader.groupBy(datasetConfig["groupBy"], recordIdsFlat, metadata)

            if not bool(recordIds):
                raise Exception("No records found. Check your recordLoader config and your dataversion config.")

            self.project.registerData("allDBRecordIds", recordIds)

    def main(self):
        self.generateData("allDBRecordIds")
