import FWCore.ParameterSet.Config as cms
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
from Configuration.AlCa.GlobalTag import GlobalTag

process = cms.Process("ElectronMVANtuplizer")

process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

process.GlobalTag = GlobalTag(process.GlobalTag, '122X_mcRun3_2021_realistic_v9', '')

# File with the ID variables to include in the Ntuplizer
mvaVariablesFile = "RecoEgamma/ElectronIdentification/data/ElectronIDVariablesRun3.txt"

outputFile = "electron_ntuple.root"

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
         #'/store/mc/Run3Winter22MiniAOD/DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8/MINIAODSIM/122X_mcRun3_2021_realistic_v9_ext1-v1/2830000/009dec29-88c9-4721-bb6f-135a7005e281.root',
        'file:9b7a1d54-d03c-4632-a95e-20fe877ac34f.root'
    )
)

useAOD = False

from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
# turn on VID producer, indicate data format  to be
# DataFormat.AOD or DataFormat.MiniAOD, as appropriate
if useAOD == True :
    dataFormat = DataFormat.AOD
    input_tags = dict(
        src = cms.InputTag("gedGsfElectrons"),
        vertices = cms.InputTag("offlinePrimaryVertices"),
        pileup = cms.InputTag("addPileupInfo"),
        genParticles = cms.InputTag("genParticles"),
        ebReducedRecHitCollection = cms.InputTag("reducedEcalRecHitsEB"),
        eeReducedRecHitCollection = cms.InputTag("reducedEcalRecHitsEE"),
    )
else :
    dataFormat = DataFormat.MiniAOD
    input_tags = dict()

switchOnVIDElectronIdProducer(process, dataFormat)

# define which IDs we want to produce
my_id_modules = [
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Winter22_ID_ISO_BO_cff'
                 ]

#add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)

process.ntuplizer = cms.EDAnalyzer('ElectronMVANtuplizer',
        #
        eleMVAs             = cms.vstring(
                                          "egmGsfElectronIDs:mvaEleID-Winter22-ID-ISO-HZZ",
                                          ),
        eleMVALabels        = cms.vstring(
                                          "Winter22IDISOHZZ",
                                          ),
        eleMVAValMaps        = cms.vstring(
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Winter22IdIsoBoValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Winter22IdIsoBoRawValues",
                                           ),
        eleMVAValMapLabels   = cms.vstring(
                                           "Winter22IdIsoBoVals",
                                           "Winter22IdIsoBoRawVals",
                                           ),
        eleMVACats           = cms.vstring(
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2RunIIIWinter22NoIsoV1Categories",
                                           ),
        eleMVACatLabels      = cms.vstring(
                                           "EleMVACats",
                                           ),
        #
        variableDefinition   = cms.string(mvaVariablesFile),
        ptThreshold = cms.double(5.0),
        #
        doEnergyMatrix = cms.bool(False), # disabled by default due to large size
        energyMatrixSize = cms.int32(2), # corresponding to 5x5
        #
        **input_tags
        )
"""
The energy matrix is for ecal driven electrons the n x n of raw
rec-hit energies around the seed crystal.

The size of the energy matrix is controlled with the parameter
"energyMatrixSize", which controlls the extension of crystals in each
direction away from the seed, in other words n = 2 * energyMatrixSize + 1.

The energy matrix gets saved as a vector but you can easily unroll it
to a two dimensional numpy array later, for example like that:

>>> import uproot
>>> import numpy as np
>>> import matplotlib.pyplot as plt

>>> tree = uproot.open("electron_ntuple.root")["ntuplizer/tree"]
>>> n = 5

>>> for a in tree.array("ele_energyMatrix"):
>>>     a = a.reshape((n,n))
>>>     plt.imshow(np.log10(a))
>>>     plt.colorbar()
>>>     plt.show()
"""

process.TFileService = cms.Service("TFileService", fileName = cms.string(outputFile))

process.p = cms.Path(process.egmGsfElectronIDSequence * process.ntuplizer)
