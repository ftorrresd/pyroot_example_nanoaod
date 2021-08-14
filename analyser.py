import tqdm 
import ROOT
#.....
# setup some ROOT stuff
ROOT.PyConfig.DisableRootLogon = True
ROOT.PyConfig.IgnoreCommandLineOptions = False
ROOT.gROOT.SetBatch(True)

# Config
max_events = 25000 # max number of events to be processed


#calculating weight of MC data
crosssection = 20508.9
luminosity = 1
W_mc = (crosssection*luminosity)/max_events
W_mc = 0.82

#weight for CMS data
W=1

# Declare histograms
# muons p_T
h_muon_pt_1 = ROOT.TH1F("h_muon_pt_1", "; Muon pT ; Muons", 50, 0, 200)
# force the storage and computation of the sum of the square of weights per bin
# REF: https://root.cern.ch/doc/master/classTH1.html#associated-errors
h_muon_pt_1.Sumw2()

h_muon_pt_2 = ROOT.TH1F("h_muon_pt_2", "; Muon pT ; Muons", 50, 0, 200)
# force the storage and computation of the sum of the square of weights per bin
# REF: https://root.cern.ch/doc/master/classTH1.html#associated-errors
h_muon_pt_2.Sumw2()

# muons phi
h_muon_phi_1 = ROOT.TH1F("h_muon_phi_1", "; Muon phi ; Muons", 50, -4, 4)
h_muon_phi_1.Sumw2()

h_muon_phi_2 = ROOT.TH1F("h_muon_phi_2", "; Muon phi ; Muons", 50, -4, 4)
h_muon_phi_2.Sumw2()

# MET Et
h_MET_phi_1 = ROOT.TH1F("h_MET_phi_1", "; MET phi ; Muons", 50, -5, 5)
h_MET_phi_1.Sumw2()

h_MET_phi_2 = ROOT.TH1F("h_MET_phi_2", "; MET phi ; Muons", 50, -5, 5)
h_MET_phi_2.Sumw2()

#MET pt
h_MET_pt_1 = ROOT.TH1F("h_MET_pt_1", "; MET pt ; Muons", 50, 0, 200)
h_MET_pt_1.Sumw2()

h_MET_pt_2 = ROOT.TH1F("h_MET_pt_2", "; MET pt ; Muons", 50, 0, 200)
h_MET_pt_2.Sumw2()

# number of muons per event
h_nmuon_1 = ROOT.TH1F("h_nmuon_1", "; Number of muons ; Events", 5, 0, 5)
h_nmuon_1.Sumw2() 

h_nmuon_2 = ROOT.TH1F("h_nmuon_2", "; Number of muons ; Events", 5, 0, 5)
h_nmuon_2.Sumw2() 

#invariant mass of muon and MET (CMS DATA)
h_MmM1 = ROOT.TH1F("h_MmM1","Transverse mass histogram (CMS DATA)", 50, 60, 200)
h_MmM1.Sumw2()

#invariant mass of muon and MET (Simulated DATA)
h_MmM2 = ROOT.TH1F("h_MmM2","Transverse mass histogram (MC DATA)", 50, 0, 200)
h_MmM2.Sumw2()

# invariant mass of two muons
h_Mmm = ROOT.TH1F("h_Mmm","Invariant mass of two muons", 50, 70, 100)
h_Mmm.Sumw2()

# Create a Chain of filles to analyze
data_chain = ROOT.TChain("Events")
data_chain.Add("/eos/cms/store/data/Run2018D/SingleMuon/NANOAOD/UL2018_MiniAODv1_NanoAODv2-v1/280000/0BF2854F-C799-2F41-A0F4-0274DC311372.root")

mc_chain = ROOT.TChain("Events")
mc_chain.Add("root://cms-xrd-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv2/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v15_L1v1-v1/00000/B81103CC-8168-3F46-AEC4-6CEF3012FC8A.root")

# # Load ROOT file g
# #data_file = ROOT.TFile.Open("root://cms-xrd-global.cern.ch///store/data/Run2018D/SingleMuon/NANOAOD/UL2018_MiniAODv1_NanoAODv2-v1/280000/0BF2854F-C799-2F41-A0F4-0274DC311372.root")
# data_file = ROOT.TFile.Open("/eos/cms/store/data/Run2018D/SingleMuon/NANOAOD/UL2018_MiniAODv1_NanoAODv2-v1/280000/0BF2854F-C799-2F41-A0F4-0274DC311372.root") #(REAL CMS DATA)

# #MC data file
# mc_file = ROOT.TFile.Open("root://cms-xrd-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv2/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v15_L1v1-v1/00000/B81103CC-8168-3F46-AEC4-6CEF3012FC8A.root")

# total number of events in the file
n_events1 = data_chain.GetEntries()  #(REAL CMS DATA)

n_events2 = mc_chain.GetEntries()

# Set the number of events for percentage calc
n_events1_for_tqdm = n_events1
if max_events >= 0:
    n_events1_for_tqdm = max_events
    
n_events2_for_tqdm = n_events2
if max_events >= 0:
    n_events2_for_tqdm = max_events 

# loop over events and fill histograms
counterA = 0
counterB = 0
counterC = 0
counterD = 0
counter1 = 0
count1 = 0

print "Processing CMS Data events..."
for ievt, evt in tqdm.tqdm(enumerate(data_chain), desc ="Events", total= n_events1_for_tqdm):     #(REAL CMS DATA)
    if ievt+1 > max_events and max_events > 0:
        break
    # loop over muons
    if evt.nMuon>=1:
      if evt.HLT_IsoMu24==1:
        for i_muon in range(evt.nMuon):
          if evt.Muon_pt > 26:
            if evt.MET_pt > 40: 
              if evt.Muon_pfRelIso03_all[i_muon] < 0.35:
                if abs(evt.Muon_eta[i_muon]) < 2.5:
                  muon1 = ROOT.Math.PtEtaPhiMVector(evt.Muon_pt[0], evt.Muon_eta[0], evt.Muon_phi[0], evt.Muon_mass[0])
                  MET1 = ROOT.Math.PtEtaPhiMVector(evt.MET_pt, 0, evt.MET_phi, 0)
                  TM_mM1 = muon1 + MET1
                  m_mM1 = TM_mM1.M()
                  if evt.Muon_tightId[i_muon]==1:
                    if (m_mM1 > 60 and m_mM1 < 200):
                      h_muon_pt_1.Fill(evt.Muon_pt[i_muon],W)
                      h_muon_phi_1.Fill(evt.Muon_phi[i_muon],W) 
                      h_MmM1.Fill(m_mM1,W)
                      h_MET_phi_1.Fill(evt.MET_phi,W)
                      h_MET_pt_1.Fill(evt.MET_pt,W)
                      h_nmuon_1.Fill(evt.nMuon,W)   # per event info
                      counterA+=1
                    else:
                      counterD+=1
                  else:
                    if (m_mM1 > 60 and m_mM1 < 200):
                      counterB+=1
                    else:
                      counterC+=1
                    counter1+=1  
                  break
    
    count1+=1          
    
print(counterA)  
print(counterB)
print(counterC) 
print(counterD)
print(counter1)
print(count1) 


countera = 0
counterb = 0
counterc = 0
counterd = 0 
counter2 = 0
count2 = 0
     
print "Processing CMS MC events..."
for ievt, evt in tqdm.tqdm(enumerate(mc_chain), desc ="Events", total= n_events2_for_tqdm):
    # condition to stop event processing, when max_events is reached
    if ievt+1 > max_events and max_events > 0:
        break
    # loop over muons 
    if evt.nMuon>=1:
      if evt.HLT_IsoMu24==1:         
        for i_muon in range(evt.nMuon):
          if evt.Muon_pt > 26:
            if evt.MET_pt > 40:
              if evt.Muon_pfRelIso03_all[i_muon] < 0.35:
                if abs(evt.Muon_eta[i_muon]) < 2.5:     
                  muon2 = ROOT.Math.PtEtaPhiMVector(evt.Muon_pt[0], evt.Muon_eta[0], evt.Muon_phi[0], evt.Muon_mass[0])
                  MET2 = ROOT.Math.PtEtaPhiMVector(evt.MET_pt, 0, evt.MET_phi, 0)
                  TM_mM2 = muon2 + MET2
                  m_mM2 = TM_mM2.M()
                  if evt.Muon_tightId[i_muon]==1:
                    if (m_mM2 > 60 and m_mM2 < 200):
                      h_muon_pt_2.Fill(evt.Muon_pt[i_muon],W_mc)
                      h_muon_phi_2.Fill(evt.Muon_phi[i_muon],W_mc) 
                      h_MmM2.Fill(m_mM2,W_mc)
                      h_MET_phi_2.Fill(evt.MET_phi,W_mc)
                      h_MET_pt_2.Fill(evt.MET_pt,W_mc)
                      h_nmuon_2.Fill(evt.nMuon,W_mc)
                      countera+=1
                    else:
                      counterd+=1
                  else:
                    if (m_mM2 > 60 and m_mM2 < 200):
                      counterb+=1
                    else:
                      counterc+=1
                    counter2+=1  
                  break
                 
    count2+=1                    

print(countera)  
print(counterb)
print(counterc)
print(counterd)
print(counter2)
print(count2)     
    
          
# Save histogram to a file
# Open a ROOT file and save the formula, function and histogram
output_file = ROOT.TFile( 'output_file.root', 'RECREATE')

# Write histograms to file
h_muon_pt_1.Write()
h_muon_phi_1.Write()
h_MET_phi_1.Write()
h_MET_pt_1.Write()
h_nmuon_1.Write()
h_muon_pt_2.Write()
h_muon_phi_2.Write()
h_MET_phi_2.Write()
h_MET_pt_2.Write()
h_nmuon_2.Write()
h_MmM1.Write()
h_MmM2.Write()


# Close file
output_file.Close()

print "\nOutput histograms have been saved output_file.root"
