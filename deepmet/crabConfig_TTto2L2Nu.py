import os
from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'TTto2L2Nu_Run3Summer22_NanoAODv12_fromMiniAODv4'
config.General.workArea = 'CrabJobs'
config.General.transferLogs = True
config.General.instance = 'prod'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'deepmet_Run3Summer22_NanoAODv12_NANO.py'
config.JobType.maxMemoryMB = 5000 
config.JobType.numCores = 4

config.Data.inputDataset = '/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM'
config.Data.splitting = 'Automatic'
config.Data.totalUnits = 1200000
config.Data.outLFNDirBase = '/store/user/alejands/DeepMET/'

config.Site.storageSite = 'T3_US_CMU'
