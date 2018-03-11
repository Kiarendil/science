# from ROOT import *
import ROOT
import glob
from math import sqrt

ch = ROOT.TChain("mytree")
MyFileNames12 = glob.glob('./data.root')
for fName in MyFileNames12:
    ch.Add(fName)

print("Adding chain done", ch.GetNtrees(), 'files ')
print('variables: ')

for v in [a.GetName() for a in ch.GetListOfLeaves()]:
    print(v)

hBmas = ROOT.TH1F('hBmas', 'B_mass', 150, 5.27963 - 0.19, 5.27963 + 0.18)

cut_cos = 'abs(B_pvcos2_Cjp - 1) < 0.00005'
cut_sign = '&& B_pvdistsignif2_Cjp > 25'

cut = cut_cos + cut_sign

ch.Draw('B_mass_Cjp >> hBmas', cut)

ff = ROOT.TFile("B_cut_.root", "recreate")

hBmas.Write()

ff.Close()
