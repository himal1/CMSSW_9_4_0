import FWCore.ParameterSet.Config as cms

process = cms.Process("PAT")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.cerr.FwkReport.reportEvery = -1
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False),
                    SkipEvent = cms.untracked.vstring('ProductNotFound')
)

## Source
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring('/store/data/Run2017D/SingleMuon/AOD/17Nov2017-v1/70001/FEC7C164-FFE3-E711-B7D2-BC305B3909FE.root')
                            #fileNames = cms.untracked.vstring('file:SourceFileH_To_ZJpsi_1.root')
                            )

## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )

## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = cms.string('94X_mc2017_realistic_v10')
## Standard PAT Configuration File
process.load("PhysicsTools.PatAlgos.patSequences_cff")

## Turn off MC matching for real data
from PhysicsTools.PatAlgos.tools.coreTools import *


from PhysicsTools.PatAlgos.tools.jetTools import *
switchJetCollection(process, 
                    jetSource = cms.InputTag('ak4PFJets'),   
                    jetCorrections     = ('AK4PF', ['L2Relative', 'L3Absolute'], '')
                    )

process.patJets.addTagInfos    = True
process.patJets.tagInfoSources  = cms.VInputTag(
  cms.InputTag("secondaryVertexTagInfosAOD") )
process.patJetCorrFactors.useRho    = False
process.patJetCorrFactors.rho       = cms.InputTag('')

## Add MET from particle flow
from PhysicsTools.PatAlgos.tools.metTools import *
addMETCollection(process, labelName='patMETPF', metSource='pfType1CorrectedMet')

## Add trigger information
process.JetMatch = cms.EDProducer("PATTriggerMatcherDRLessByR", # match by DeltaR only, best match by DeltaR
  src     = cms.InputTag( "cleanPatJets" ),
  matched = cms.InputTag( "patTrigger" ), # defined in PhysicsTools/PatAlgos/python/triggerLayer1/triggerProducer_cfi.py
  andOr                      = cms.bool( False ),  # AND
  filterIdsEnum              = cms.vstring( '*' ), # wildcard, overlaps with 'filterIds'
  filterIds                  = cms.vint32( 0 ),    # wildcard, overlaps with 'filterIdsEnum'
  filterLabels               = cms.vstring( '*' ), # wildcard
  matchedCuts                = cms.string('type("TriggerJet")'),
  pathNames                  = cms.vstring('HLT_Jet30U_v*','HLT_Jet60_v*','HLT_Jet80_v*','HLT_Jet110_v*','HLT_Jet150_v*','HLT_Jet190_v*','HLT_Jet240_v*','HLT_Jet370_v*'),
  pathLastFilterAcceptedOnly = cms.bool( False ),  # select only trigger objects used in last filters of succeeding paths
  collectionTags             = cms.vstring( '*' ), # wildcard
  maxDeltaR                  = cms.double( 0.5 ),
  resolveAmbiguities         = cms.bool( True ),   # only one match per trigger object
  resolveByMatchQuality      = cms.bool( True )    # take best match found per reco object: by DeltaR here (s. above)
)

from PhysicsTools.PatAlgos.tools.trigTools import *
switchOnTriggerStandAlone( process, None, 'patDefaultSequence', 'HLT', '' )
switchOnTriggerMatchEmbedding( process, ['JetMatch'], 'patTrigger', 'patDefaultSequence', 'HLT', '' )

## Make JPsi and Higgs candidates
process.goodMuons = cms.EDFilter("MuonRefSelector",
    src = cms.InputTag("muons"),
    cut = cms.string(""),
)
process.JPsiToMuMu = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string('goodMuons@+ goodMuons@-'),
    cut = cms.string(''),
)


## Analyzer package
process.PATEventTree = cms.EDAnalyzer("PATEventTree",
    rootFileName                 = cms.untracked.string("SingleMuonDatasetEtab17Nov_2017F_JpsiUpsilonZ_NoTriggered_Compact.root"),
    isJPsiMuMu                   = cms.untracked.bool(False),
    isHBB                        = cms.untracked.bool(False),
    isMC                         = cms.untracked.bool(False),
    useFatJets                   = cms.untracked.bool(False),
    HLT_Skim                     = cms.untracked.bool(False),
    PrimaryVertexCollectionLabel = cms.untracked.InputTag('offlinePrimaryVertices'),
    HLTCollectionLabel           = cms.untracked.InputTag('patTrigger'),
    MuonCollectionLabel          = cms.untracked.InputTag('cleanPatMuons'),
    ElectronCollectionLabel      = cms.untracked.InputTag('cleanPatElectrons'),
    PhotonCollectionLabel        = cms.untracked.InputTag('cleanPatPhotons'),
#    ParticleCollectionLabel      = cms.untracked.InputTag('cleanPatTrackCands'),
    TrackCollectionLabel         = cms.untracked.InputTag('generalTracks'),
    JetCollectionLabel           = cms.untracked.InputTag('cleanPatJets'),
    FatJetCollectionLabel        = cms.untracked.VInputTag(['cleanPatJetsPFFAT','cleanPatJetsPFSUB','cleanPatJetsPFFILTER']),
    METCollectionLabel           = cms.untracked.InputTag('pfMetT1'),
    JPsiInputLabel               = cms.untracked.InputTag('goodMuons'),
    JPsiCandLabel                = cms.untracked.InputTag('JPsiToMuMu'),
    GenCollectionLabel           = cms.untracked.InputTag('genParticles')
    )


from RecoTauTag.Configuration.HPSPFTaus_cff import *

process.goodHPSPFTaus = cms.Sequence(process.hpsPFTauChargedIsoPtSum*
				     process.hpsPFTauNeutralIsoPtSum*
                                     process.hpsPFTauPUcorrPtSum*
       	      	      	      	     process.hpsPFTauNeutralIsoPtSumWeight*
                                     process.hpsPFTauFootprintCorrection*
                                     process.hpsPFTauPhotonPtSumOutsideSignalCone*
                                     process.hpsPFTauDiscriminationByRawCombinedIsolationDBSumPtCorr3Hits*
                                     process.hpsPFTauDiscriminationByLoosePileupWeightedIsolation3Hits*
                                     process.hpsPFTauDiscriminationByMediumPileupWeightedIsolation3Hits*
                                     process.hpsPFTauDiscriminationByTightPileupWeightedIsolation3Hits*
                                     process.hpsPFTauDiscriminationByPhotonPtSumOutsideSignalCone*
                                     process.hpsPFTauDiscriminationByRawPileupWeightedIsolation3Hits
)

process.patDefaultSequence.replace(process.updateHPSPFTaus, process.goodHPSPFTaus)


process.patDefaultSequence.remove(process.electronMatch)
process.patDefaultSequence.remove(process.muonMatch)
process.patDefaultSequence.remove(process.photonMatch)
process.patDefaultSequence.remove(process.tauMatch)
process.patDefaultSequence.remove(process.tauGenJets)
process.patDefaultSequence.remove(process.tauGenJetsSelectorAllHadrons)
process.patDefaultSequence.remove(process.tauGenJetMatch)
process.patDefaultSequence.remove(process.patJetGenJetMatch)
# process.patDefaultSequence.remove(process.patTaus)
# process.patDefaultSequence.remove(process.cleanPatTaus)
# process.patDefaultSequence.remove(process.countPatTaus)
process.patDefaultSequence.remove(process.patJetPartonMatch)
process.patDefaultSequence.remove(process.patJetPartonsLegacy)
process.patDefaultSequence.remove(process.patJetPartonAssociationLegacy)
process.patDefaultSequence.remove(process.patJetFlavourAssociationLegacy)
process.patDefaultSequence.remove(process.patJetPartons)
process.patDefaultSequence.remove(process.patJetFlavourAssociation)
# process.patDefaultSequence.remove(process.selectedPatTaus)

runOnData(process, ['All'], '', [])


## Run the actual sequence
process.p = cms.Path(
    process.patDefaultSequence*
#    patMuonsWithTriggerSequence*
    process.goodMuons*
    process.JPsiToMuMu*
    process.PATEventTree
    )

process.out = cms.OutputModule('PoolOutputModule',
				outputCommands = cms.untracked.vstring('keep *'),
				fileName = cms.untracked.string('checkContent.root'))

runOnData(process, ['All'], '', [])

from PhysicsTools.PatAlgos.tools.trigTools import *
switchOnTriggerMatchEmbedding( process )

# process.outpath = cms.EndPath(process.out)
