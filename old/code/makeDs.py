# from ROOT import *
import ROOT
import glob
from math import sqrt
# from variables import *  # import vars
import variables as v
RAD = ROOT.RooAbsData
RAD.setDefaultStorageType(RAD.Tree)

REMUC = True

ch = ROOT.TChain("mytree")
MyFileNames1B = glob.glob('../data/data.root')
MyFileNames = MyFileNames1B

for fName in MyFileNames:
    ch.Add(fName)

print("Adding chain done", ch.GetNtrees(), 'files ')

varset = ROOT.RooArgSet(v.mbu)
dataset = ROOT.RooDataSet("ds", "Dataset", varset)

nEvt = ch.GetEntries()
print("entries:", nEvt)
par = 0.
par_0 = -1000.
Mass_B = 0.
Mass_Jpsi = 0.
BB = 0
flag_empty = 1

for evt in range(nEvt):
    if ch.GetEntry(evt) <= 0:
        break
    if evt % 10000 == 0:  # printout progress
        perc = str(int(100 * (evt - 0) / (nEvt - 0 + 0.0)))
        print("[" + perc + (' ' * (3 - len(perc))) + "%] evt", evt, ", saved", dataset.numEntries())
    #
    if (ch.SAMEEVENT < 1 or (not REMUC)) and flag_empty != 1:  # if new & !0, Write
        dataset.add(varset)
        flag_empty = 1  # now empty and reset par
        par_0 = -1000
    #
    if ch.K1_pt < 1.0:
        continue  # deaf 0.8
    #
    if ch.B_mass_Cjp < v.mbu.getMin():
        continue
    if ch.B_mass_Cjp > v.mbu.getMax():
        continue
    #
    #
    if ch.JPSI_mass_Cmumu < 3.04:
        continue
    if ch.JPSI_mass_Cmumu > 3.15:
        continue
    #
    # if ch.B_vtxprob_Cjp    < 0.01      :continue #deaf 0.01
    if ch.B_pvcos2_Cjp < 0.999:
        continue
    if ch.B_pvdistsignif2_Cjp < 5.:
        continue  # deaf 3
    # if ch.B_pt_Cjp         < 10.0      :continue 
    #
    # find best candidate in event: select the one closer to gen
    # par = ch.B_vtxprob_Cjp
    if (not REMUC) or ((ch.SAMEEVENT == 1 and par > par_0) or ch.SAMEEVENT == 0):
        #
        par_0 = par  # if better than was + flag non empty
        v.mbu.setVal(ch.B_mass_Cjp)
        flag_empty = 0

if flag_empty != 1:
    dataset.add(varset)  # write last event if needed

dataset.Print()

fileOUT = ROOT.TFile('../data/new.root', 'recreate')
dataset.Write()
fileOUT.Close()
