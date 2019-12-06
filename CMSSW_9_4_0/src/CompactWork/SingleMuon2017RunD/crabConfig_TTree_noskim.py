from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'TTree_13TeV_SingleMuon2017D_JpsiZUps_NoTrigger_Compact1'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'makeRealPATEvents_cfg.py'
config.JobType.allowUndistributedCMSSW = True
config.JobType.outputFiles = ['SingleMuonDatasetEtab17Nov_2017D_JpsiUpsilonZ_NoTriggered_Compact.root']
config.Data.inputDBS = 'global'
config.Data.inputDataset = '/SingleMuon/Run2017D-17Nov2017-v1/AOD'
#config.Data.outputPrimaryDataset = 'DoubleJPsiToMuMu_RAWSIM_SPS_LO_may2016_largetest_FNAL'
config.Data.lumiMask = 'Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON_MuonPhys.txt'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 50
#NJOBS = 500  # This is not a configuration parameter, but an auxiliary variable that we use in the next line.
config.Data.totalUnits = -1
config.Data.outLFNDirBase = '/store/user/hacharya/DataFiles/'
config.Data.publication = False
config.Site.storageSite = 'T3_US_FNALLPC'
