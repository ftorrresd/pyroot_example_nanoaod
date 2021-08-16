import ROOT

# Create a Chain of filles to analyze

## MC
mc_chain = ROOT.TChain("Events")
print "--> Adding MC files to chain..."
# Dataset: /WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM
# List all files:
# dasgoclient -query="file dataset=/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"

# mc_chain.Add("root://cms-xrd-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv2/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v15_L1v1-v1/00000/B81103CC-8168-3F46-AEC4-6CEF3012FC8A.root")
mc_chain.Add("/eos/cms//store/mc/RunIISummer20UL18NanoAODv2/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v15_L1v1-v1/00000/8B47D4A5-572B-C24D-848A-A2945D0E794D.root")


## Data
data_chain = ROOT.TChain("Events")
print "--> Adding Data files to chain..."
# Dataset: /SingleMuon/Run2018D-UL2018_MiniAODv1_NanoAODv2-v1/NANOAOD
# List all files.
# dasgoclient -query="file dataset=/SingleMuon/Run2018D-UL2018_MiniAODv1_NanoAODv2-v1/NANOAOD"

data_chain.Add("/eos/cms/store/data/Run2018D/SingleMuon/NANOAOD/UL2018_MiniAODv1_NanoAODv2-v1/280000/0BF2854F-C799-2F41-A0F4-0274DC311372.root")
