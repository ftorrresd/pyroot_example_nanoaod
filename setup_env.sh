
export SCRAM_ARCH=slc7_amd64_gcc700 
cd /cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_10_6_20/ 
cmsenv
cd -

voms-proxy-init --rfc --voms cms -valid 192:00





# root -q -l root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/NANOAOD/UL2018_MiniAODv1_NanoAODv2-v1/280000/0BF2854F-C799-2F41-A0F4-0274DC311372.root