# from ROOT import *
import ROOT
import glob 
from math import sqrt
 
ch = ROOT.TChain("mytree")
MyFileNames12 = glob.glob('data.root')
for fName in MyFileNames12:
    ch.Add(fName)

print("Adding chain done", ch.GetNtrees(), 'files ')
print('variables: ')

for v in [a.GetName() for a in ch.GetListOfLeaves()]:
    print(v)


ff = ROOT.TFile("B_cuts.root", "recreate")


cut_cos = []
cut_sign = []

for i in range(1, 10):
    v = str(i)
    cut_cos.append('abs(B_pvcos2_Cjp - 1) < 0.0000' + v)

for i in range(5, 40, 5):
    v = str(i)
    cut_sign.append('&& B_pvdistsignif2_Cjp > ' + v)

hBmas = []

for i in range(1, len(cut_cos) * len(cut_sign) + 2):
    name = 'hB_mass' + str(i)
    print(name)
    hBmas.append(ROOT.TH1F(name, 'B_mass_Cjp', 150, 5.27963 - 0.15, 5.27963 + 0.18))

i = 0

for cut1 in cut_cos:
    for cut2 in cut_sign:
        cut = cut1 + ' ' + cut2
        # print(cut)
        i += 1
        draw_name = 'B_mass_Cjp >> hB_mass' + str(i)
        ch.Draw(draw_name, cut)
        hBmas[i].Write()
        # print('Sucsess ' + str(i))

# ch.Draw('B_mass_Cjp >> hBmas', cut)
 
# ff = ROOT.TFile("B_cuts.root", "recreate")

# hBmas.Write()

ff.Close()
