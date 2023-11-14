import os
from CRABClient.UserUtilities import config
config = config()

import datetime
timestamp = datetime.datetime.now().strftime('_%Y%m%d-%H%M%S')

config.General.requestName = '__requestName__' + timestamp
config.General.workArea = 'CrabJobs'
config.General.transferLogs = True
config.General.instance = 'prod'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '__psetName__'
config.JobType.maxMemoryMB = 5000 
config.JobType.numCores = 4

config.Data.inputDataset = '__inputDataset__'
config.Data.splitting = 'Automatic'
config.Data.totalUnits = __nEvents__
config.Data.outLFNDirBase = '__outLFNDirBase__'

config.Site.storageSite = '__storageSite__'