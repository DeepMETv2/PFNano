#!/usr/bin/env python
"""
This is a small script that submits a config over datasets
"""
import os

mc_samples = [
    ('/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 1), #623 28876062 1.3T
    ('/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 1), #480, 22749608 1.2T
    ('/ZJetsToNuNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 1), #437, 19810491 1.1T
    ('/ZJetsToNuNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 1), # 139, 5968910 364.1GB
    ('/ZJetsToNuNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 1), #55 2129122 135.9GB
    ('/ZJetsToNuNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 1), #19 381695 26.6GB
    ('/ZJetsToNuNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 1), #8 268224 20.3GB

    ('/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v1/MINIAODSIM',1), #2482, 196039620 8.4T
    ('/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 1)#87 146058000 8.1T
]
run_samples = [
    ('/ZJetsToNuNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 1), #8 268224 20.3GB  -> 13G
]

config_dir = 'crab_configs'

if not os.path.isdir( config_dir ) :
    os.mkdir(config_dir )

submit_commands = []

for path, nfiles in run_samples:
    base_name = path.split('/')[1]

    fname = '%s/%s.py'%(config_dir, base_name)

    ofile = open(fname, 'w')

    file_entries = []

    file_entries.append('from CRABClient.UserUtilities import config')
    file_entries.append('config = config()')

    file_entries.append('')
    file_entries.append('config.section_("General")')
    file_entries.append('config.General.requestName = "production_v2_%s"' %(base_name))
    file_entries.append('config.General.workArea = "crab_projects"')
    file_entries.append('config.General.transferLogs = False')
    file_entries.append('config.General.transferOutputs = True')

    file_entries.append('')
    file_entries.append('config.section_("JobType")')
    file_entries.append('config.JobType.pluginName = "Analysis"')
    file_entries.append('config.JobType.psetName = "106X_2018_mc_NANO.py"')
    file_entries.append('config.JobType.maxMemoryMB = 4000 # Default is 2500 : Max I have used is 13000')
    file_entries.append('config.JobType.numCores = 8')
    file_entries.append('config.JobType.allowUndistributedCMSSW = True')

    file_entries.append('')
    file_entries.append('config.section_("Data")')
    file_entries.append('config.Data.inputDataset = "%s"'%path)
    # FileBased splitting
    #file_entries.append('config.Data.splitting = "FileBased"')
    #file_entries.append('config.Data.unitsPerJob = 1')
    #file_entries.append('config.Data.totalUnits = %d'%nfiles)

    # EventAwareLumiBased splitting
    file_entries.append('config.Data.splitting = "EventAwareLumiBased"')  
    file_entries.append('config.Data.unitsPerJob = 400000')  

    file_entries.append('config.Data.ignoreLocality = False')
    file_entries.append('config.Data.publication = False')
    file_entries.append('config.Data.outputDatasetTag= "NanoAOD_0916"')
    file_entries.append('config.Data.outLFNDirBase = "/store/user/yilai/GraphMET_Sep16/"')

    file_entries.append('')
    file_entries.append('config.section_("Site")')
    file_entries.append('config.Site.storageSite = "T3_US_FNALLPC"')

    for line in file_entries :
        ofile.write( line + '\n' )

    ofile.close()

    submit_commands.append( 'crab submit --config %s' %( fname ) )


submit_file = open('submit_crab.sh', 'w' )
submit_file.write( '#!/bin/bash\n' )

for cmd in submit_commands :
    submit_file.write(cmd + '\n' )


submit_file.close()
os.system('chmod +x submit_crab.sh')

