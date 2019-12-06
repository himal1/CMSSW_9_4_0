ifeq ($(strip $(FourMuAnalysis/Upsilon)),)
src_FourMuAnalysis_Upsilon := self/FourMuAnalysis/Upsilon
FourMuAnalysis/Upsilon  := src_FourMuAnalysis_Upsilon
src_FourMuAnalysis_Upsilon_BuildFile    := $(WORKINGDIR)/cache/bf/src/FourMuAnalysis/Upsilon/BuildFile
src_FourMuAnalysis_Upsilon_LOC_USE := TrackingTools/TrajectoryState clhep Geometry/TrackerNumberingBuilder boost FWCore/Framework self DataFormats/VertexReco DataFormats/DetId TrackingTools/TrackFitters DataFormats/L1GlobalMuonTrigger DataFormats/SiStripDetId CondFormats/DataRecord FWCore/PluginManager DataFormats/TrajectorySeed Geometry/Records DataFormats/L1GlobalTrigger Alignment/OfflineValidation SimTracker/TrackerHitAssociation DataFormats/TrackerRecHit2D DataFormats/DTDigi DataFormats/FEDRawData DataFormats/L1Trigger TrackingTools/TransientTrack DataFormats/L1DTTrackFinder root CommonTools/RecoAlgos DataFormats/SiPixelDetId Geometry/TrackerGeometryBuilder DataFormats/LTCDigi DataFormats/TrackReco DataFormats/MuonDetId DataFormats/MuonReco CondFormats/L1TObjects DataFormats/TrackingRecHit DataFormats/SiStripCluster FWCore/ParameterSet
src_FourMuAnalysis_Upsilon_EX_USE   := $(foreach d,$(src_FourMuAnalysis_Upsilon_LOC_USE),$(if $($(d)_EX_FLAGS_NO_RECURSIVE_EXPORT),,$d))
ALL_EXTERNAL_PRODS += src_FourMuAnalysis_Upsilon
src_FourMuAnalysis_Upsilon_INIT_FUNC += $$(eval $$(call EmptyPackage,src_FourMuAnalysis_Upsilon,src/FourMuAnalysis/Upsilon))
endif

