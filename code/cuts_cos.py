# from ROOT import *
import ROOT
import glob

ch = ROOT.TChain("mytree")
MyFileNames12 = glob.glob('./data.root')
for fName in MyFileNames12:
    ch.Add(fName)

print("Adding chain done", ch.GetNtrees(), 'files ')
print('variables: ')

for v in [a.GetName() for a in ch.GetListOfLeaves()]:
    print(v)

hBmass = []

hBmas1 = ROOT.TH1F('hBmas1', 'B_mass', 150, 5.27963 - 0.19, 5.27963 + 0.18)
hBmas2 = ROOT.TH1F('hBmas2', 'B_mass', 150, 5.27963 - 0.19, 5.27963 + 0.18)
hBmas3 = ROOT.TH1F('hBmas3', 'B_mass', 150, 5.27963 - 0.19, 5.27963 + 0.18)
hBmas4 = ROOT.TH1F('hBmas4', 'B_mass', 150, 5.27963 - 0.19, 5.27963 + 0.18)
hBmas5 = ROOT.TH1F('hBmas5', 'B_mass', 150, 5.27963 - 0.19, 5.27963 + 0.18)

for i in range(1, 8):
    name = 'hB_mass' + str(i)
    # print(name)
    hBmass.append(ROOT.TH1F(name, 'B_mass_Cjp', 150, 5.27963 - 0.19, 5.27963 + 0.18))

cut_sign = 'B_pvdistsignif2_Cjp > 3'

cut_cos = []

cut_cos.append('&& abs(B_pvcos2_Cjp - 1) < 0.01')
cut_cos.append('&& abs(B_pvcos2_Cjp - 1) < 0.005')
cut_cos.append('&& abs(B_pvcos2_Cjp - 1) < 0.001')
cut_cos.append('&& abs(B_pvcos2_Cjp - 1) < 0.0005')
cut_cos.append('&& abs(B_pvcos2_Cjp - 1) < 0.0001')

cuts = []

for cut in cut_cos:
    cuts.append(cut_sign + cut)

# for i in range(0, 7):
#     print('For ' + str(hBmass[i]) + ' cut is ' + str(cuts[i]))

ch.Draw('B_mass_Cjp >> hBmas1', cuts[0])
ch.Draw('B_mass_Cjp >> hBmas2', cuts[1])
ch.Draw('B_mass_Cjp >> hBmas3', cuts[2])
ch.Draw('B_mass_Cjp >> hBmas4', cuts[3])
ch.Draw('B_mass_Cjp >> hBmas5', cuts[4])

ff = ROOT.TFile("B_cut_cos.root", "recreate")

hBmas1.Write()
hBmas2.Write()
hBmas3.Write()
hBmas4.Write()
hBmas5.Write()

ff.Close()
