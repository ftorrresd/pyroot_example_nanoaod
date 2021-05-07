import tqdm 
import ROOT

# setup some ROOT stuff
ROOT.PyConfig.DisableRootLogon = True
ROOT.PyConfig.IgnoreCommandLineOptions = False
ROOT.gROOT.SetBatch(True)

# Config
max_events = 25000 # max number of events to be processed

# Declare histograms
# muons p_T
h_muon_pt = ROOT.TH1F("h_muon_pt", "; Muon pT ; Muons", 50, 0, 200)
# force the storage and computation of the sum of the square of weights per bin
# REF: https://root.cern.ch/doc/master/classTH1.html#associated-errors
h_muon_pt.Sumw2() 

# number of muons per event
h_nmuon = ROOT.TH1F("h_nmuon", "; Number of muons ; Events", 5, 0, 5)
h_nmuon.Sumw2() 

# Load ROOT file 
data_file = ROOT.TFile.Open("root://cms-xrd-global.cern.ch///store/data/Run2018D/SingleMuon/NANOAOD/UL2018_MiniAODv1_NanoAODv2-v1/280000/0BF2854F-C799-2F41-A0F4-0274DC311372.root")
# data_file = ROOT.TFile.Open("/eos/cms/store/data/Run2018D/SingleMuon/NANOAOD/UL2018_MiniAODv1_NanoAODv2-v1/280000/0BF2854F-C799-2F41-A0F4-0274DC311372.root")

# total number of events in the file
n_events = data_file.Events.GetEntries() 

# Set the number of events for percentage calc
n_events_for_tqdm = n_events
if max_events >= 0:
    n_events_for_tqdm = max_events

# loop over events and fill histograms
for ievt, evt in tqdm.tqdm(enumerate(data_file.Events), desc ="Events", total= n_events_for_tqdm):
    # condition to stop event processing, when max_events is reached
    if ievt+1 > max_events and max_events > 0:
        break

    # per event info
    h_nmuon.Fill(evt.nMuon)

    # loop over muons
    for i_muon in range(evt.nMuon):
        h_muon_pt.Fill(evt.Muon_pt[i_muon])


# Save histogram to a file
# Open a ROOT file and save the formula, function and histogram
output_file = ROOT.TFile( 'output_file.root', 'RECREATE')

# Write histograms to file
h_muon_pt.Write()
h_nmuon.Write()

# Close file
output_file.Close()

print "\nOutput histograms have been saved output_file.root"
    
