import tqdm 
import json
import ROOT
#.....
# setup some ROOT stuff
ROOT.PyConfig.DisableRootLogon = True
ROOT.PyConfig.IgnoreCommandLineOptions = False
ROOT.gROOT.SetBatch(True)

# Load source files chains
from source_files import data_chain 
from source_files import mc_chain 

# Config
max_events = 25000 # max number of events to be processed -> set to -1 to proccess all events
# max_events = -1 # max number of events to be processed -> set to -1 to proccess all events



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



# total number of events in the file
n_events1 = data_chain.GetEntries()  #(REAL CMS DATA)

n_events2 = mc_chain.GetEntries()

# Set the number of events for percentage calc
n_events1_for_tqdm = n_events1
if max_events >= 0:
    n_events1_for_tqdm = max_events
    
n_events2_for_tqdm = int(n_events2*0.8/3.) # a correction factor applied in orther to not overflow the event list when running over all events
if max_events >= 0:
    n_events2_for_tqdm = max_events 


#calculating weight of MC data
# x-sec REF: 
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
# https://pdglive.lbl.gov/Particle.action?node=S043&init=0

W_crosssection = 20508.9*1E-3 # in fb
br_W_to_leptons = 0.10785 #this is the mean value of Branching Ratio to muon+nu and electron+nu
luminosity = 1 # in fb^-1
W_mc = (W_crosssection*br_W_to_leptons*luminosity)/n_events2_for_tqdm

#weight for CMS data
W = 1

print "--> Weights:"
print "----> MC: " + str(W_mc) 
print "----> Data: "+ str(W)


# loop over events and fill histograms
counterA = 0
counterB = 0
counterC = 0
counterD = 0
counter1 = 0
count1 = 0

print "Processing CMS Data events..."

# Golden JSON File 2018
# /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt
def good_event(run,lumi):
    # Check whether this a good event
    with open('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt') as json_file:
      JSONlist = json.load(json_file)

      if str(run) in JSONlist.keys():
          for rg in JSONlist[str(run)]:
              if len(rg) ==2:
                  if lumi>=rg[0] and lumi<=rg[1]:
                      return True
      
      return False

# Loop over Data events
for ievt, evt in tqdm.tqdm(enumerate(data_chain), desc ="Events"):     #(REAL CMS DATA)
    # only loop over good events - not even sure if it is needed...
    if good_event(evt.run, evt.luminosityBlock): 
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
                          counterA+=W
                        else:
                          counterD+=W
                      else:
                        if (m_mM1 > 60 and m_mM1 < 200):
                          counterB+=W
                        else:
                          counterC+=W
                        counter1+=W
                      break
        
        count1+=W        
    
print("-->> Event counts - DATA")
print("Counter A: " + str(counterA))  
print("Counter B: " + str(counterB))
print("Counter C: " + str(counterC)) 
print("Counter D: " + str(counterD))
print("Counter 1 ???: " + str(counter1))
print("Total number of processed events: " + str(count1)) 


countera = 0
counterb = 0
counterc = 0
counterd = 0 
counter2 = 0
count2 = 0
     
print "Processing CMS MC events..."

# load PU weights file
pu_weight_file = ROOT.TFile('data/pu_weights_2018_from_HZZ4L.root')
histo_pu_weight = pu_weight_file.Get('weights')
histo_pu_weight_up = pu_weight_file.Get('weights_varUp')
histo_pu_weight_down = pu_weight_file.Get('weights_varDn')

def get_pu_weight(pu_true):
  pu_weight_nominal = histo_pu_weight.GetBinContent(histo_pu_weight.FindBin(pu_true))
  pu_weight_up = histo_pu_weight_up.GetBinContent(histo_pu_weight_up.FindBin(pu_true))
  pu_weight_down = histo_pu_weight_down.GetBinContent(histo_pu_weight_down.FindBin(pu_true))

  return pu_weight_nominal, pu_weight_up, pu_weight_down

# Loop over Data events
for ievt, evt in tqdm.tqdm(enumerate(mc_chain), desc ="Events"):
    # get PU weight and correct MC one
    pu_weight_nominal, pu_weight_up, pu_weight_down = get_pu_weight(evt.Pileup_nTrueInt)
    w_mc_effective = W_mc * pu_weight_nominal

    # filter only MC for muon + nu decay channel
    is_muon_decay = False
    for lhe_part in range(evt.nLHEPart):
      if abs(evt.LHEPart_pdgId[lhe_part]) == 13: # MUON DECAY
      # if abs(evt.LHEPart_pdgId[lhe_part]) == 11: # ELECTRON DECAY
        is_muon_decay = True

    if is_muon_decay:
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
                        h_muon_pt_2.Fill(evt.Muon_pt[i_muon],w_mc_effective)
                        h_muon_phi_2.Fill(evt.Muon_phi[i_muon],w_mc_effective) 
                        h_MmM2.Fill(m_mM2,w_mc_effective)
                        h_MET_phi_2.Fill(evt.MET_phi,w_mc_effective)
                        h_MET_pt_2.Fill(evt.MET_pt,w_mc_effective)
                        h_nmuon_2.Fill(evt.nMuon,w_mc_effective)
                        countera+=w_mc_effective
                      else:
                        counterd+=w_mc_effective
                    else:
                      if (m_mM2 > 60 and m_mM2 < 200):
                        counterb+=w_mc_effective
                      else:
                        counterc+=w_mc_effective
                      counter2+=w_mc_effective
                    break
                  
      count2+=w_mc_effective                   

print("-->> Event counts (weighted) - MC")
print("Counter A: " + str(countera))  
print("Counter B: " + str(counterb))
print("Counter C: " + str(counterc)) 
print("Counter D: " + str(counterd))
print("Counter 2 ???: " + str(counter2))
print("Total number of processed events: " + str(count2)) 

    
          
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
