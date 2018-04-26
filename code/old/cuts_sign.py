# from ROOT import *
import ROOT
import glob

ch = ROOT.TChain("mytree")
MyFileNames12 = glob.glob('../../data/data.root')
for fName in MyFileNames12:
    ch.Add(fName)

print("Adding chain done", ch.GetNtrees(), 'files ')
print('variables: ')

for v in [a.GetName() for a in ch.GetListOfLeaves()]:
    print(v)

hBmass = []

hBmas1 = ROOT.TH1F('hBmas1', 'B_mass', 150, 5.27963 - 0.179, 5.27963 + 0.18)
hBmas2 = ROOT.TH1F('hBmas2', 'B_mass', 150, 5.27963 - 0.179, 5.27963 + 0.18)
hBmas3 = ROOT.TH1F('hBmas3', 'B_mass', 150, 5.27963 - 0.179, 5.27963 + 0.18)
hBmas4 = ROOT.TH1F('hBmas4', 'B_mass', 150, 5.27963 - 0.179, 5.27963 + 0.18)
hBmas5 = ROOT.TH1F('hBmas5', 'B_mass', 150, 5.27963 - 0.179, 5.27963 + 0.18)
hBmas6 = ROOT.TH1F('hBmas6', 'B_mass', 150, 5.27963 - 0.179, 5.27963 + 0.18)
hBmas7 = ROOT.TH1F('hBmas7', 'B_mass', 150, 5.27963 - 0.179, 5.27963 + 0.18)

for i in range(1, 8):
    name = 'hB_mass' + str(i)
    # print(name)
    hBmass.append(ROOT.TH1F(name, 'B_mass_Cjp', 150, 5.27963 - 0.179, 5.27963 + 0.18))

cut_cos = 'B_pvcos2_Cjp > 0.9995 '

cut_sign = []

cut_sign.append('&& B_pvdistsignif2_Cjp > 25')
cut_sign.append('&& B_pvdistsignif2_Cjp > 20')
cut_sign.append('&& B_pvdistsignif2_Cjp > 15')
cut_sign.append('&& B_pvdistsignif2_Cjp > 10')
cut_sign.append('&& B_pvdistsignif2_Cjp > 7')
cut_sign.append('&& B_pvdistsignif2_Cjp > 5')
cut_sign.append('&& B_pvdistsignif2_Cjp > 3')

cuts = []

for cut in cut_sign:
    cuts.append(cut_cos + cut)

# for i in range(0, 7):
#     print('For ' + str(hBmass[i]) + ' cut is ' + str(cuts[i]))

ch.Draw('B_mass_Cjp >> hBmas1', cuts[0])
ch.Draw('B_mass_Cjp >> hBmas2', cuts[1])
ch.Draw('B_mass_Cjp >> hBmas3', cuts[2])
ch.Draw('B_mass_Cjp >> hBmas4', cuts[3])
ch.Draw('B_mass_Cjp >> hBmas5', cuts[4])
ch.Draw('B_mass_Cjp >> hBmas6', cuts[5])
ch.Draw('B_mass_Cjp >> hBmas7', cuts[6])

ff = ROOT.TFile("../../data/B_cut_sign.root", "recreate")

hBmas1.Write()
hBmas2.Write()
hBmas3.Write()
hBmas4.Write()
hBmas5.Write()
hBmas6.Write()
hBmas7.Write()

ff.Close()
