# from ROOT import *
import ROOT
import glob 

ch = ROOT.TChain("mytree")
MyFileNames12 = glob.glob('../data/data.root')
for fName in MyFileNames12:
    ch.Add(fName)

print("Adding chain done", ch.GetNtrees(), 'files ')

hBmas_single = ROOT.TH1F('hBmas', 'B_mass', 150, 5.27963 - 0.19, 5.27963 + 0.18)
hB_mass = []
for i in range(1, 6):
    name = 'hB_mass' + str(i)
    hB_mass.append(ROOT.TH1F(name, 'B_mass_Cjp', 150, 5.27963 - 0.15, 5.27963 + 0.18))

cut_sign = 'B_pvdistsignif2_Cjp > 3 '

cut_cos = ['&& abs(B_pvcos2_Cjp - 1) < 0.01', '&& abs(B_pvcos2_Cjp - 1) < 0.005', '&& abs(B_pvcos2_Cjp - 1) < 0.001',
           '&& abs(B_pvcos2_Cjp - 1) < 0.0005', '&& abs(B_pvcos2_Cjp - 1) < 0.0001']

cuts = []

for cut in cut_cos:
    cuts.append(cut_sign + cut)

ff = ROOT.TFile("../data/B_cuts_many.root", "recreate")
# hB_mass = []
# for i in range(1, 6):
#     name = 'hB_mass' + str(i)
#     hB_mass.append(ROOT.TH1F(name, 'B_mass_Cjp', 150, 5.27963 - 0.15, 5.27963 + 0.18))

for i in range(0, 4):
    # print('For ' + str(hB_mass[i]) + ' cut is ' + str(cuts[i]))
    hist = 'hB_mass' + str(i + 1)
    ch.Draw('B_mass_Cjp >> ' + hist, cuts[i])
    hB_mass[i].Write()

ff.Close()
