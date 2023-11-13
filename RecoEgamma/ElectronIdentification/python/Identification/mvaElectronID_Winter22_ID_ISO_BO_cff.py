import FWCore.ParameterSet.Config as cms
from RecoEgamma.ElectronIdentification.Identification.mvaElectronID_tools import *
from os import path

mvaTag = "Winter22IdIsoBo"

#weightFileDir = "RecoEgamma/ElectronIdentification/data/MVAWeightFiles/Winter_22_ID_ISO"
weightFileDir="~/CMSSW_13_0_0/src/RecoEgamma/ElectronIdentification/data/MVAWeightFiles/Winter_22_ID_ISO"

mvaWeightFiles = cms.vstring(
     path.join(weightFileDir, "EB1_5.weights.xml.gz"), # EB1_5
     path.join(weightFileDir, "EB2_5.weights.xml.gz"), # EB2_5
     path.join(weightFileDir, "EE_5.weights.xml.gz"), # EE_5
     path.join(weightFileDir, "EB1_10.weights.xml.gz"), # EB1_10
     path.join(weightFileDir, "EB2_10.weights.xml.gz"), # EB2_10
     path.join(weightFileDir, "EE_10.weights.xml.gz"), # EE_10
     )
'''
categoryCuts = cms.vstring(
     "EleMVACats == 0", # EB1_5
     "EleMVACats == 1", # EB2_5
     "EleMVACats == 2", # EE_5
     "EleMVACats == 3", # EB1_10
     "EleMVACats == 4", # EB2_10
     "EleMVACats == 5", # EE_10
     )
'''
categoryCuts = cms.vstring(
    "pt < 10. && abs(superCluster.eta) < 0.800",
    "pt < 10. && abs(superCluster.eta) >= 0.800 && abs(superCluster.eta) < 1.479",
    "pt < 10. && abs(superCluster.eta) >= 1.479",
    "pt >= 10. && abs(superCluster.eta) < 0.800",
    "pt >= 10. && abs(superCluster.eta) >= 0.800 && abs(superCluster.eta) < 1.479",
    "pt >= 10. && abs(superCluster.eta) >= 1.479",
)

mvaEleID_Winter22_ID_ISO_HZZ_container = EleMVARaw_WP(
    idName = "mvaEleID-Winter22-ID-ISO-HZZ", mvaTag = mvaTag,
    cutCategory0 = "1.633973689084034", # EB1_5
    cutCategory1 = "1.5499076306249353", # EB2_5
    cutCategory2 = "2.0629564440753247", # EE_5
    cutCategory3 = "0.3685228146685872", # EB1_10
    cutCategory4 = "0.2662407818935475", # EB2_10
    cutCategory5 = "-0.5444837363886459", # EE_10
    )


mvaEleID_Winter22_ID_ISO_BO_producer_config = cms.PSet(
    mvaName             = cms.string(mvaClassName),
    mvaTag              = cms.string(mvaTag),
    nCategories         = cms.int32(6),
    categoryCuts        = categoryCuts,
    weightFileNames     = mvaWeightFiles,
    variableDefinition  = cms.string(mvaVariablesFileRun3)
    )

mvaEleID_Winter22_ID_ISO_HZZ = configureVIDMVAEleID( mvaEleID_Winter22_ID_ISO_HZZ_container )

mvaEleID_Winter22_ID_ISO_HZZ.isPOGApproved = cms.untracked.bool(True)
