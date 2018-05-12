# from ROOT import *
import ROOT
import glob
from math import sqrt
# from variables import *  # import vars
import variables as v
RAD = ROOT.RooAbsData
RAD.setDefaultStorageType(RAD.Tree)

REMUC = True

ch = ROOT.TChain("ds0")
MyFileNames1B = glob.glob('../data/data.root')
MyFileNames = MyFileNames1B

for fName in MyFileNames:
    ch.Add(fName)

print("Adding chain done", ch.GetNtrees(), 'files ')
# print('variables: ')
# for var in [a.GetName() for a in ch.GetListOfLeaves()]:
#     print(var)

varset = ROOT.RooArgSet(v.mbu)

datasets = []

for i in range(7):
    datasets.append(ROOT.RooDataSet("ds" + str(i), "Dataset", varset))

nEvt = ch.GetEntries()
print("entries:", nEvt)
par = 0.
par_0 = -1000.
Mass_B = 0.
Mass_Jpsi = 0.
BB = 0
flag_empty = 1

cuts_cos = [0.985, 0.99, 0.995, 0.999, 0.9995, 0.9999, 0.99995]
cuts_sign = [3, 5, 7, 10, 15, 20, 25]
cuts_prob = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
cuts_B_pt = [8, 10, 15, 20, 25, 30, 35]

for i in range(7):
    print(f'\n Starting {i} iteration')
    for evt in range(nEvt):
        if ch.GetEntry(evt) <= 0:
            break
        if evt % 10000 == 0:  # printout progress
            perc = str(int(100 * (evt - 0) / (nEvt - 0 + 0.0)))
            print("[" + perc + (' ' * (3 - len(perc))) + "%] evt", evt, ", saved", datasets[i].numEntries())
        #
        if (ch.SAMEEVENT < 1 or (not REMUC)) and flag_empty != 1:  # if new & !0, Write
            datasets[i].add(varset)
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
        if ch.B_vtxprob_Cjp < 0.01:
            continue #deaf 0.01
        if ch.B_pvcos2_Cjp < cuts_cos[i]:
            continue
        if ch.B_pvdistsignif2_Cjp < 3:
            continue  # deaf 3
        if ch.B_pt_Cjp < 8.:
            continue
        #
        # find best candidate in event: select the one closer to gen
        # par = ch.B_vtxprob_Cjp
        if (not REMUC) or ((ch.SAMEEVENT == 1 and par > par_0) or ch.SAMEEVENT == 0):
            #
            par_0 = par  # if better than was + flag non empty
            v.mbu.setVal(ch.B_mass_Cjp)
            flag_empty = 0

    if flag_empty != 1:
        datasets[i].add(varset)  # write last event if needed

    datasets[i].Print()


fileOUT = ROOT.TFile('../data/new.root', 'recreate')
for i in range(7):
    datasets[i].Write()
fileOUT.Close()
